import base64
import pytest
from playwright.sync_api import sync_playwright
from config import settings
from drivers.events import EventListenerManager
from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Default environment")
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser type: chromium, firefox, or webkit",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode",
    )
    parser.addoption(
        "--devtools",
        action="store_true",
        default=False,
        help="Open browser with devtools",
    )
    parser.addoption(
        "--proxy",
        action="store",
        default=None,
        help="Proxy server address (e.g., http://proxy-server:port)",
    )
    parser.addoption(
        "--listeners",
        action="store",
        default="",
        help="Comma-separated event listeners (console, request, response, click)",
    )
    parser.addoption(
        "--slow-mo",
        action="store",
        default="0",
        help="Slow down operations by this amount of milliseconds",
    )


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(request, playwright):
    browser_type = request.config.getoption("--browser-type")

    launch_options = get_browser_options(request)

    if browser_type == "chromium":
        args = ["--start-maximized"]
        browser_instance = playwright.chromium.launch(
            headless=launch_options["headless"],
            args=args,
            slow_mo=launch_options["slow_mo"],
            devtools=launch_options["devtools"],
        )
    else:
        browser_launch_func = {
            "firefox": playwright.firefox.launch,
            "webkit": playwright.webkit.launch,
        }.get(browser_type)

        browser_instance = browser_launch_func(**launch_options)

    yield browser_instance
    browser_instance.close()


@pytest.fixture
def page(browser, request):
    # Retrieve timeout options
    navigation_timeout = request.config.getoption("--navigation-timeout", default=12000)
    default_timeout = request.config.getoption("--default-timeout", default=6000)

    log.annotate(
        f"Creating a new browser context with timeouts: "
        f"{navigation_timeout}, {default_timeout}"
    )

    # Create a new browser context
    browser_context = browser.new_context(no_viewport=True)
    browser_context.set_default_navigation_timeout(navigation_timeout)
    browser_context.set_default_timeout(default_timeout)

    # Create a new page
    page = browser_context.new_page()
    selected_listeners = request.config.getoption("--listeners").strip().split(",")
    EventListenerManager(page, selected_listeners, log)

    yield page

    page.close()
    # browser_context.close()  # Optional: Close the context if you want to free resources # noqa


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook to capture and embed screenshots in the HTML report when a test fails.
    This works for both failed tests and expected failures (xfail).
    """
    # Retrieve the HTML plugin for embedding screenshots
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()

    # If the pytest-html plugin is not active, skip embedding screenshots
    if not pytest_html:
        return

    # Add screenshots for failed tests or expected failures (xfail)
    if report.when in ("call", "setup"):
        xfail = hasattr(report, "wasxfail")
        if (report.failed or xfail) and "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                # Capture screenshot as base64
                screenshot_bytes = page.screenshot()
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode()
                # Embed screenshot in the HTML report
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_base64, "Screenshot"))
                report.extra = extra
            except Exception as e:
                print(f"Error capturing screenshot: {e}")


def get_browser_options(request):
    """
    Returns browser launch options based on pytest command-line options.
    """
    return {
        "headless": request.config.getoption("--headless"),
        "devtools": request.config.getoption("--devtools"),
        "slow_mo": float(request.config.getoption("--slow-mo")),
        "proxy": {"server": request.config.getoption("--proxy")}
        if request.config.getoption("--proxy")
        else None,
    }

import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Default environment"
    )
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser type: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--devtools",
        action="store_true",
        default=False,
        help="Open browser with devtools"
    )
    parser.addoption(
        "--proxy",
        action="store",
        default=None,
        help="Proxy server address (e.g., http://proxy-server:port)"
    )


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(request, playwright):
    browser_type = request.config.getoption("--browser-type")
    launch_options = get_browser_options(request)

    browser = {
        "chromium": playwright.chromium.launch,
        "firefox": playwright.firefox.launch,
        "webkit": playwright.webkit.launch
    }.get(browser_type)

    if browser is None:
        raise ValueError(f"Unsupported browser type: {browser_type}")

    yield browser(**launch_options)
    browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def get_browser_options(request):
    """
    Returns browser launch options based on pytest command-line options.
    """
    headless = request.config.getoption("--headless")
    devtools = request.config.getoption("--devtools")
    proxy = request.config.getoption("--proxy")

    launch_options = {
        "headless": headless,
        "devtools": devtools,
    }

    if proxy:
        launch_options["proxy"] = {"server": proxy}

    return launch_options

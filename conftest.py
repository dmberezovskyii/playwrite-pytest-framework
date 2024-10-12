import pytest
from playwright.sync_api import sync_playwright
from drivers.events import EventListenerManager
from utils.logger import Logger, LogLevel

log = Logger(log_lvl=LogLevel.INFO)


# Registering pytest options for command-line argument parsing
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
    parser.addoption(
        "--listeners",
        action="store",
        default="",
        help="Comma-separated event listeners (options: console, request, response, click)"
    )

# Initialize Playwright instance for the test session
@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


# Browser fixture to create a browser instance with dynamic options
@pytest.fixture(scope="session")
def browser(request, playwright):
    browser_type = request.config.getoption("--browser-type")
    launch_options = get_browser_options(request)

    if browser_type == "chromium":
        args = ["--start-maximized"]
        browser_instance = playwright.chromium.launch(
            headless=launch_options.get("headless"),
            args=args,
            devtools=launch_options.get("devtools")
        )
    else:
        # For other browsers, launch normally
        browser_launch_func = {
            "firefox": playwright.firefox.launch,
            "webkit": playwright.webkit.launch
        }.get(browser_type)

        browser_instance = browser_launch_func(**launch_options)

    yield browser_instance
    browser_instance.close()


# Page fixture to open a new page and attach listeners dynamically
@pytest.fixture
def page(browser, request):
    page = browser.new_page(no_viewport=True)  # no_viewport ensures no fixed size

    # Fetching and attaching event listeners
    selected_listeners = request.config.getoption("--listeners").strip().split(',')
    EventListenerManager(page, selected_listeners, log)

    yield page
    page.close()


# Helper function to get browser launch options
def get_browser_options(request):
    """
    Returns browser launch options based on pytest command-line options.
    """
    return {
        "headless": request.config.getoption("--headless"),
        "devtools": request.config.getoption("--devtools"),
        "proxy": {
            "server": request.config.getoption("--proxy")
        } if request.config.getoption("--proxy") else None
    }

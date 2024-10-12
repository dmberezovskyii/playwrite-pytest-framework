import pytest
from playwright.sync_api import sync_playwright

from drivers.events import EventListenerManager


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
    # New option to select event listeners
    parser.addoption(
        "--listeners",
        action="store",
        default="",
        help="Comma-separated event listeners (options: console, request, response, click)"
    )


@pytest.fixture(scope="session")
def playwright():
    """Initialize Playwright for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(request, playwright):
    """Create and return a browser instance based on command-line options."""
    browser_type = request.config.getoption("--browser-type")
    launch_options = get_browser_options(request)

    # Map the browser types to their launch functions
    browser_launch_func = {
        "chromium": playwright.chromium.launch,
        "firefox": playwright.firefox.launch,
        "webkit": playwright.webkit.launch
    }.get(browser_type)

    if not browser_launch_func:
        raise ValueError(f"Unsupported browser type: {browser_type}. Please choose from 'chromium', 'firefox', or 'webkit'.")

    instance = browser_launch_func(**launch_options)

    yield instance
    instance.close()


@pytest.fixture
def page(browser, request):
    """Create and return a new page in the browser context with dynamic event listeners."""
    context = browser.new_context()
    page = context.new_page()

    # Fetch selected event listeners from command-line options
    selected_listeners = request.config.getoption("--listeners").strip().split(',')

    # Create an EventListenerManager to handle the event listeners
    EventListenerManager(page, selected_listeners)

    yield page
    context.close()


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

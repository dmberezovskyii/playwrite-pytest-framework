from playwright.sync_api import Page
from utils.logger import log


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @log()
    def navigate_to(self, url: str):
        """Navigate to a specified URL."""
        self.page.goto(url)

    @log()
    def click(self, selector: str):
        """Click an element by selector."""
        self.wait_for_selector(selector)
        self.page.locator(selector).click()

    @log()
    def fill(self, selector: str, value: str):
        """Fill an input field with a specified value."""
        self.wait_for_selector(selector)
        self.page.locator(selector).fill(value)

    @log()
    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """Wait for a specific selector to be visible."""
        self.page.wait_for_selector(selector, timeout=timeout)

    @log()
    def wait_for_clickable(self, selector: str, timeout: int = 10000):
        """Wait for a specific selector to be clickable."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.locator(selector).wait_for(state="attached", timeout=timeout)

    @log()
    def is_visible(self, selector: str) -> bool:
        """Assert that an element is visible on the page."""
        return self.page.is_visible(selector)

    @log()
    def close(self):
        """Close the page."""
        self.page.close()

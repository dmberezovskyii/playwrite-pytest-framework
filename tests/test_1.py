from playwright.sync_api import Page


class Test1:

    def test_has_title(self, page: Page):
        """Test that the page has the correct title."""
        page.goto('https://playwright.dev/')
        assert page.title() == "Playwright"

    def test_get_started_link(self, page: Page):
        """Test that the 'Get Started' link is present."""
        page.goto('https://playwright.dev/')
        assert page.query_selector('text=Get Started') is not None

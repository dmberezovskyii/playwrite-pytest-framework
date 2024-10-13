from playwright.sync_api import sync_playwright


class BrowserFactory:
    def __init__(self, browser_type="chromium", headless=True):
        self.browser_type = browser_type
        self.headless = headless

    def create_browser(self, launch_options):
        with sync_playwright() as p:
            match self.browser_type:
                case "chromium":
                    return p.chromium.launch(
                        headless=self.headless, **launch_options
                    )
                case "firefox":
                    return p.firefox.launch(headless=self.headless, **launch_options)
                case "webkit":
                    return p.webkit.launch(headless=self.headless, **launch_options)
                case _:
                    raise ValueError(
                        f"Unsupported browser type: {self.browser_type}"
                    )

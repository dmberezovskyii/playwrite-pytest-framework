class EventListenerManager:
    def __init__(self, page, selected_listeners, logger):
        self.page = page
        self.selected_listeners = selected_listeners
        self.logger = logger
        self.attach_listeners()

    def attach_listeners(self):
        """Attach event listeners based on selected options."""
        if "console" in self.selected_listeners:
            self.page.on("console", self.handle_console_log)
            self.logger.annotate("Attached console log listener", "info")

        if "request" in self.selected_listeners:
            self.page.on("request", self.handle_request)
            self.logger.annotate("Attached request listener", "info")

        if "response" in self.selected_listeners:
            self.page.on("response", self.handle_response)
            self.logger.annotate("Attached response listener", "info")

        if "events" in self.selected_listeners:
            self.page.on("load", self.handle_page_load)
            self.page.on("close", self.handle_page_close)
            self.logger.annotate("Attached page load and close listeners", "info")

    def handle_console_log(self, msg):
        """Handle console log events."""
        self.logger.annotate(f"Console log: {msg.text()}", "info")

    def handle_request(self, req):
        """Handle request events."""
        self.logger.annotate(f"Request: {req.url}", "info")

    def handle_response(self, res):
        """Handle response events."""
        self.logger.annotate(f"Response: {res.url} - {res.status()}", "info")

    def handle_page_load(self):
        """Handle page load events."""
        self.logger.annotate(f"Page loaded: {self.page.url}", "info")

    def handle_page_close(self):
        """Handle page close events."""
        self.logger.annotate(f"Page closed: {self.page.url}", "info")

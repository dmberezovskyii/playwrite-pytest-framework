class EventListenerManager:
    def __init__(self, page, selected_listeners):
        self.page = page
        self.selected_listeners = selected_listeners
        self.attach_listeners()

    def attach_listeners(self):
        """Attach event listeners based on selected options."""
        if 'console' in self.selected_listeners:
            self.page.on("console", lambda msg: print(f"Console log: {msg.text()}"))
        if 'request' in self.selected_listeners:
            self.page.on("request", lambda req: print(f"Request: {req.url}"))
        if 'response' in self.selected_listeners:
            self.page.on("response", lambda res: print(f"Response: {res.url} - {res.status()}"))
        if 'events' in self.selected_listeners:
            self.page.on('load', lambda res: print(f"Page loaded: {self.page.url}"))
            self.page.on('close', lambda res: print(f"Page loaded: {self.page.url}"))

from playwright.sync_api import Page

from base_page import BasePage
from locators.input_locators import InputLocators
from utils.logger import log


class InputForm(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = InputLocators()

    def fill_full_name(self, name: str):
        """Fill user full name"""
        self.fill(self.locators.FULL_NAME_SELECTOR, name)

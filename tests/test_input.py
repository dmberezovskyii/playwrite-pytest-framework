from config import settings
from pages.input_form import InputForm


class TestFillForm:

    def test_fill_full_name(self, page):
        """Test filling in the full name in the input form."""
        input_form = InputForm(page)

        # Navigate to the input form page
        input_form.navigate_to(settings.base_url)

        # Fill in the full name
        input_form.fill_full_name("John Doe")

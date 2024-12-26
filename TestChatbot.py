from playwright.sync_api import sync_playwright
import pytest
from abc import ABC, abstractmethod

class TestChatbot(ABC):

    @classmethod
    def setup_class(cls): # per class
        cls.playright = sync_playwright().start()
        cls.browser = cls.playright.chromium.launch(headless=False)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()

    @classmethod
    def teardown_class(cls): # per class
        cls.context.close()
        cls.browser.close()
        cls.playright.stop()


    def setup_method(self): # per test case
        self.login()
        self.gotoChatbotPage()

    def teardown_method(self): # per test case
        self.logout()

    def login(self):
        self.page.goto("https://dashboard.cohere.com/welcome/login")
        self.page.fill("input[id='email']", "")
        self.page.fill("input[id='password']", '')
        with self.page.expect_navigation():
            self.page.click("button[type='submit']")
        self.page.wait_for_load_state()

        # confirm successfull login
        try:
           self.page.wait_for_selector("div[data-element='Popover']", state="visible")
        except Exception as e:
            pytest.fail(f"Login failed {e}")

    def gotoChatbotPage(self):
        self.page.goto("https://coral.cohere.com/")
        self.page.wait_for_load_state()

        # close the splash screen
        try:
            self.page.wait_for_selector("div[id='headlessui-dialog-panel-:ra:']", state="visible")
            self.page.locator("div[id='headlessui-dialog-panel-:ra:']").locator("button").nth(1).click(force=True)
        except Exception as e:
            pytest.fail(f"Failed to close splash screen{e}")

        # accept cookies
        try:
            self.page.wait_for_selector("button:has-text('Accept All')", state="visible")
            self.page.locator("button:has-text('Accept All')").nth(0).click(force=True)
        except Exception as e:
            pytest.fail(f"Failed to close accept cookies dialog{e}")

    @abstractmethod
    def action(self):
        pass

    def logout(self):
        self.page.locator("div[data-element='Popover']").locator("button").click()
        self.page.wait_for_selector("a[id='auth-link']", state="visible")
        self.page.locator("a[id='auth-link']").nth(0).click()
        self.page.wait_for_load_state()
        #confirm successfull logout
        if self.page.title() != "Login | Cohere":
            pytest.fail("Logout failed")

    def test_action(self):
        self.action()

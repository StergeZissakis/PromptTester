import time
from TestChatbot import TestChatbot
import pytest

class TestTextPrompt(TestChatbot):
    prompt = "Hi"
    expectedText = "Hello!"

    def setup_method(self): # per test case
        super().setup_method()
        self.send(self.prompt)

    def teardown_method(self): # per test case
        super().teardown_method()

    def send(self, msg):
        # send a "Hi" prompt
        textarea = self.page.locator("textarea[id='composer']")
        self.page.fill("textarea[id='composer']", msg)
        submitButton= textarea.locator("xpath=following-sibling::*[1]")
        submitButton.click()

    def waitForResponse(self):
        # wait for response to be rendered
        self.page.wait_for_function("document.querySelectorAll('div[class=\"message flex\"]').length > 1")




    def expect(self):
        # expect a "Hello!" int the response text
        responseContainers = self.page.locator("div[class='message flex']")
        responseDiv = responseContainers.nth(responseContainers.count() - 1) #get the last from the list of responses
        responseText = responseDiv.locator('p').text_content()
        if self.expectedText not in responseText:
            pytest.fail(f"Prompt response is wrong {responseText}")

    def action(self):
        self.waitForResponse()
        self.expect()
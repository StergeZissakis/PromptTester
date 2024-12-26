from TestChatbot import TestChatbot
import pytest

class TestUploadPrompt(TestChatbot):
    fileName = "Text.txt"
    prompt = "What language is the file @Text.txt in?"
    expctedWord = "Latin"

    def setup_method(self):  # per test case
        super().setup_method()
        self.uploadTextFile()
        self.waitForUpload()

    def teardown_method(self):  # per test case
        self.cleanUpUplodedFile()
        super().teardown_method()

    def uploadTextFile(self):
        #upload the text file
        self.toolbar = self.page.locator("div[data-component='ComposerToolbar']")

        self.uploadButton = self.toolbar.locator("button").nth(0)

        with self.page.expect_file_chooser() as fc_info:
            self.uploadButton.click()
        file_chooser = fc_info.value
        file_chooser.set_files(self.fileName)

    def waitForUpload(self):
        # wait for the upload to finish
        try:
            self.toolbar.locator(f"p:has-text('{self.fileName}')").wait_for(state="visible")
        except Exception as e:
            pytest.fail(f"File upload failed {e}")


    def send(self):
        # send a "wWhat language is the file in?" prompt
        textarea = self.page.locator("textarea[id='composer']")
        self.page.fill("textarea[id='composer']", self.prompt)
        submitButton= textarea.locator("xpath=following-sibling::*[1]")
        submitButton.click()

    def expect(self):
        # expect a "Latin" int the response text
        responseContainers = self.page.locator("div[class='message flex']")
        responseDiv = responseContainers.nth(responseContainers.count() - 1) #get the last from the list of responses
        responseText = responseDiv.locator('p').text_content()
        if self.expctedWord not in responseText:
            pytest.fail(f"Prompt response is wrong: {responseText} instead of {self.expctedWord}")


    def cleanUpUplodedFile(self):
        # clean up the uploaded file
        topToolbar = self.page.locator("div[data-component='Header']")
        topToolbar.locator("button").click() # click on the kebab menu icon
        dropDownMenu = topToolbar.locator("button + div")
        dropDownMenu.locator('li').nth(0).click() # click on the settings menu item
        self.page.wait_for_selector("section[id='configuration']", state="visible")
        settingsDrawer = self.page.locator("section[id='configuration']")
        settingsDrawer.locator("button:has-text('Files')").click()  # click on the Files tab
        mostRecentLabel = settingsDrawer.locator("p:has-text('Most recent')")
        textFileDiv = mostRecentLabel.locator("xpath=..").locator("div[data-component='UploadedFile']") # get the top file
        textFileDiv.hover()  # enable the delete icon
        textFileDiv.locator("button").nth(1).click() # delete the file


    def action(self):
        self.send()
        self.expect()

# PromptTester
This is a set of two test cases for the Cohere chatbot.<br>
The implementation is based on a class hierarchy utilising the Template Method design pattern.
This means that by inheriting from the base class and implementing the action abstract method, you can implement any 
test case for the chatbot very quickly.


# How to set up and run
`git clone https://github.com/StergeZissakis/PromptTester.git`<br>
`python -m venv venv`<br>
Load the virtual environment `venv\Scripts\activate` or `source venv/bin/active` depending on the OS<br>
`python -m pip install --upgrade pip`<br>
`pip install -r Requirements.txt`<br>
`playwright install`<br>
`pytest TestUploadPrompt.py TestTextPrompt.py`



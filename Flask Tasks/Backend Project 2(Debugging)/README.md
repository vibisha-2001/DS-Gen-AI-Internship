# Note Taking Application
## Bug Identification & Resolution Report
### Project Overview
This project focused on debugging and improving a Flask-based Note Taking Application.
The objective was to identify existing issues in the application, understand their root causes,
and resolve them so the app functions correctly by allowing users to add and display
multiple notes without errors.
## Bug 1: Missing GET method in Flask route
The Flask route did not include the GET method, which caused issues when loading the
page directly in the browser.
The route was updated to support both GET and POST methods.
## Bug 2: Incorrect use of request.args instead of form data
- request.args is used only for GET requests
- The form was submitting data using POST
## Bug 3: Missing method attribute in HTML form
The HTML form did not specify a submission method
- Without a method, HTML forms default to GET
- This caused a mismatch with the Flask route expecting POST requests
## Bug 4: None value appearing before any note submission
A None value appeared as a bullet point when the page loaded for the first time.
## Bug 5: Empty notes being added to the list
Submitting the form without entering text resulted in empty notes being added.
# Approach to Debugging and Resolution
- Carefully tested the application to observe unexpected behavior
- Analyzed the interaction between HTML forms and Flask request handling
- Identified mismatches between frontend and backend logic
- Applied input validation to prevent invalid data
• Identified mismatches between frontend and backend logic
• Applied input validation to prevent invalid data

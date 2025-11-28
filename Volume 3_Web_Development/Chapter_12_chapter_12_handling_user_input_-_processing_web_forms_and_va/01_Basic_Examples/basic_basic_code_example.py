
#
# These sources are part of the "PyThon Programming Series" by Edgar Milvus, 
# you can find it on Amazon: https://www.amazon.com/dp/B0FTTQNXKG or
# https://tinyurl.com/PythonProgrammingSeries 
# New books info: https://linktr.ee/edgarmilvus 
#
# MIT License
# Copyright (c) 2025 Edgar Milvus
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

# app.py - Simple Form Handler Example

from flask import Flask, request, render_template_string

# 1. Define the HTML template for the form
# We use a single string to keep the example self-contained, avoiding external template files.
FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Form Input</title>
</head>
<body>
    <h1>User Greeting Service</h1>
    
    {# Check if a greeting message exists (this is filled after a successful POST request) #}
    {% if greeting %}
        <p style="color: green; font-weight: bold;">{{ greeting }}</p>
    {% endif %}

    <h2>Please Enter Your Name:</h2>
    
    {# The form is configured to submit data back to the same URL ('/') 
       using the critical POST method. #}
    <form method="POST" action="/">
        <label for="username">Name:</label>
        
        {# The 'name' attribute is vital; this is the key the server uses to retrieve the data. #}
        <input type="text" id="username" name="username" required>
        
        <button type="submit">Submit Name</button>
    </form>
</body>
</html>
"""

# Initialize the Flask application
app = Flask(__name__)

# 2. Define the main route to handle both GET (display form) and POST (process data)
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize a variable to hold the greeting message. It is None initially.
    greeting_message = None

    # 3. Check the HTTP Request Method
    # This conditional logic is the core of form handling.
    if request.method == 'POST':
        # This block executes ONLY when the user submits the form via POST

        # 4. Access the submitted form data
        # request.form is a dictionary-like object containing key/value pairs from the form.
        # We use .get('username') to safely retrieve the value associated with the input field named 'username'.
        user_name = request.form.get('username')

        # 5. Process the data (Basic validation and generation of response)
        if user_name:
            # Simple sanitization: strip whitespace from beginning/end
            clean_name = user_name.strip()
            greeting_message = f"Hello, {clean_name}! Your input has been successfully processed."
        else:
            # Handle case where input was empty
            greeting_message = "Error: Name field cannot be empty. Please try again."

    # 6. Render the template
    # render_template_string takes the HTML template and injects the variables (like 'greeting') 
    # using the Jinja templating engine.
    return render_template_string(FORM_HTML, greeting=greeting_message)

if __name__ == '__main__':
    # Run the application. debug=True allows for automatic reloading and helpful error messages.
    app.run(debug=True)

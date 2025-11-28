
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

from flask import Flask, request, render_template_string, redirect, url_for

# 1. Initialize the Flask application
app = Flask(__name__)

# 2. Define the HTML structure for the form.
# This is served during a GET request.
FORM_HTML = """
<!doctype html>
<html>
<head>
    <title>Method Handling Example</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        form { background: #f4f4f4; padding: 20px; border-radius: 8px; max-width: 400px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 95%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px; }
        input[type="submit"] { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>User Name Submission</h1>
    <!-- CRITICAL: method="POST" ensures data is sent via the POST method -->
    <!-- CRITICAL: action="/" sends the data back to the same route handler -->
    <form method="POST" action="/">
        <label for="user_name">Enter Your Name:</label>
        <!-- CRITICAL: The 'name' attribute ('user_name') is the key used to retrieve data in Flask -->
        <input type="text" id="user_name" name="user_name" required>
        <input type="submit" value="Submit Name">
    </form>
</body>
</html>
"""

# 3. Define the route handler, specifying both methods
@app.route('/', methods=['GET', 'POST'])
def handle_submission():
    # 4. Check the HTTP method used by the client
    if request.method == 'POST':
        # 5. Logic executed only if the request is POST (form submitted)
        
        # request.form is a dictionary-like object holding submitted form data
        user_name = request.form.get('user_name')
        
        # 6. Validation and Response
        if user_name:
            # Successful submission response
            return f"<h1>Success! Hello, {user_name}.</h1><p>We processed your data via the HTTP POST method.</p>"
        else:
            # Handle case where form data was empty (optional: redirect for simplicity)
            # In a real app, we would show an error message on the form.
            return redirect(url_for('handle_submission'))

    # 7. Logic executed if the request is NOT POST (i.e., GET)
    # This serves the initial page/form display.
    return render_template_string(FORM_HTML)

# 8. Standard execution block
if __name__ == '__main__':
    # Running the development server
    print("Starting Flask server on http://127.0.0.1:5000/")
    app.run(debug=True)

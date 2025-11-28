
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

from flask import Flask, request, render_template_string

# 1. Setup the Flask Application
# We instantiate the Flask object, which is the core of our web application.
app = Flask(__name__)

# 2. Define the vulnerable HTML template inline
# NOTE: The '| safe' filter is explicitly used here to demonstrate the vulnerability. 
# It tells Jinja2 to bypass its default, secure auto-escaping mechanism.
VULNERABLE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Greeting App - XSS Vulnerability Demo</title>
</head>
<body>
    <h1>Personalized Greeting Service</h1>
    
    <!-- 
    *** VULNERABLE LINE ***
    The '{{ name | safe }}' instruction renders the input literally, 
    allowing malicious HTML/scripts to execute.
    -->
    <p>Hello, dear user: <strong>{{ name | safe }}</strong></p>
    
    <p>Try accessing this endpoint with a malicious payload in the URL:</p>
    <p><code>/greet?name=&lt;script&gt;alert('XSS Attack Successful!')&lt;/script&gt;</code></p>
</body>
</html>
"""

# 3. Define the route handler
@app.route('/greet')
def greet_user():
    # Get user input from the URL query parameters (e.g., /greet?name=Alice)
    # If 'name' is not provided, it defaults to 'Guest'.
    user_name = request.args.get('name', 'Guest')
    
    # Render the vulnerable template, passing the user input directly.
    return render_template_string(VULNERABLE_TEMPLATE, name=user_name)

# 4. Run the application
if __name__ == '__main__':
    # Setting debug=True is useful for development, but never for production.
    app.run(debug=True)

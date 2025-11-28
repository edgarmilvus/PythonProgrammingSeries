
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

# basic_routing_app.py

# 1. Import the necessary Flask class from the flask package.
from flask import Flask

# 2. Initialize the Flask application object.
# The variable 'app' is the central object that manages all routes and configurations.
# '__name__' tells Flask where to look for resources like templates and static files.
app = Flask(__name__)

# 3. Define the Root Endpoint (The Homepage)
# The @app.route('/') decorator maps the URL path '/' to the function immediately below it.
@app.route('/')
def index():
    # 4. This is the 'View Function'. It executes when a user visits the root URL.
    # Returning a simple string automatically wraps it into an HTTP response (Status 200 OK).
    return "Welcome to the Root Endpoint! This is the primary landing page."

# 5. Define a Secondary Endpoint
# This decorator maps the URL path '/about' to the 'about_page' function.
@app.route('/about')
def about_page():
    # 6. This view function handles requests specifically for the /about URL.
    return "This is the About page. Flask applications are structured around endpoints."

# 7. Standard Python entry point check.
# This ensures the server only runs when the script is executed directly (not imported).
if __name__ == '__main__':
    # 8. Run the development server.
    # debug=True enables automatic reloading upon code changes and provides useful error messages.
    app.run(debug=True)

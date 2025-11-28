
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

# app.py

# 1. Import necessary components from the Flask library
from flask import Flask, render_template

# 2. Initialize the Flask application instance
# __name__ tells Flask where to look for resources like templates and static files
app = Flask(__name__)

# 3. Define the route for the homepage (the root URL '/')
@app.route('/')
def index():
    # render_template looks inside the 'templates' folder.
    # It loads 'index.html', which will inherit from base.html.
    # We pass a variable 'page_title' to be used in the base template's <title> tag.
    return render_template('index.html', page_title="Home Page")

# 4. Define the route for the 'About Us' page
@app.route('/about')
def about():
    # This loads 'about.html', demonstrating that multiple child templates
    # can inherit from the same parent structure (base.html).
    return render_template('about.html', page_title="About Our Company")

# 5. Standard boilerplate to run the application locally
if __name__ == '__main__':
    # debug=True allows the server to automatically reload upon code changes
    app.run(debug=True)

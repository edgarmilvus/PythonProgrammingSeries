
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

# app.py: Minimal Flask application designed for WSGI deployment

# 1. Import the necessary Flask class
from flask import Flask

# 2. Initialize the Flask application instance (the WSGI callable)
# The variable name 'app' is critical for standard WSGI servers like Gunicorn.
app = Flask(__name__)

# 3. Define a route: The URL path that triggers the function
@app.route('/')
def hello_world_page():
    # 4. Return the content that the browser will display
    return "Status: OK. This message is served by a WSGI-compliant Flask application."

# 5. Boilerplate for local development testing (Gunicorn ignores this block)
if __name__ == '__main__':
    # Running directly uses Flask's built-in development server
    print("WARNING: Running in development mode. Use 'gunicorn' for production.")
    app.run(debug=True, port=5000)

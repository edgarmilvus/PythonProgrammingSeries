
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

# Source File: solution_exercise_6.py
# Description: Solution for Exercise 6
# ==========================================

from flask import abort, jsonify

# Custom Error Handler implementation
@app.errorhandler(400)
def handle_csrf_error(e):
    """
    Handles 400 Bad Request errors, specifically targeting CSRF failures 
    which often manifest this way in Flask extensions.
    """
    # In a real application, you might check e.description 
    # for specific messages from Flask-WTF/CSRF extensions.
    
    # Return a user-friendly JSON response or rendered template
    response = jsonify({
        'error': 'Bad Request',
        'message': 'Security token missing or invalid. Please refresh the page and try again.'
    })
    response.status_code = 400
    return response

# Note: This handler needs to be defined within the scope of the Flask app instance.
app.register_error_handler(400, handle_csrf_error)

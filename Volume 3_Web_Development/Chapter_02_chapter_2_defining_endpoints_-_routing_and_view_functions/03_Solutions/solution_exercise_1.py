
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

from flask import Flask, request

# Initialize the application
app = Flask(__name__)

# --- Exercise 1: The Welcome Mat and the About Page (Static Routing) ---

@app.route('/')
def home_page():
    """
    Handles the root URL path.
    Returns: A welcome message.
    """
    return "Welcome to the Python Web Series Hub!"

@app.route('/about')
def about_page():
    """
    Handles the static /about URL path.
    Returns: Informational text.
    """
    return "This application demonstrates basic routing principles from Book 3, Chapter 2."

# --- Exercise 2: The Simple Task Manager (Specifying HTTP Methods) ---

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    """
    Handles both GET (viewing) and POST (creating) requests on the same URL.
    Requires the 'request' object from Flask.
    """
    if request.method == 'POST':
        # Simulated logic for task creation
        return "Success! New task added and database updated."
    else:
        # Default behavior for GET requests (viewing status)
        return "Current Status: 3 tasks pending."

# --- Exercise 3: The Profile Viewer and Calculator (Dynamic Routing) ---

@app.route('/profile/<username>')
def user_profile(username):
    """
    Handles dynamic profile URLs, capturing the username as a string.
    """
    # Flask automatically passes the captured URL segment as the argument
    return f"Hello, {username}. Welcome to your personalized dashboard."

@app.route('/add/<int:num1>/<int:num2>')
def add_numbers(num1, num2):
    """
    Handles dynamic calculation URLs, explicitly requiring integer types.
    Performs addition on the captured integers.
    """
    # Flask converts num1 and num2 to integers before execution
    result = num1 + num2
    return f"{num1} + {num2} = {result}"

# --- Exercise 4: Interactive Challenge - API Endpoint Refinement ---

@app.route('/api/<version>/products/category/<int:category_id>')
def get_filtered_products(version, category_id):
    """
    Handles a complex, versioned API route with dynamic filtering parameters.
    """
    if version != 'v1':
        # Handles unsupported API versions
        return f"Error: Version {version} is not supported."
    else:
        # Handles supported v1 API calls
        return f"API Version v1: Displaying products for category ID {category_id}."

# --- Exercise 5: Method Conflict Resolution (Advanced Debugging) ---

# 1. Setup Function 1 (GET)
@app.route('/data', methods=['GET'])
def view_data_get():
    """Handles GET requests for /data."""
    return "Data retrieved successfully (GET)."

# 2. Setup Function 2 (POST)
@app.route('/data', methods=['POST'])
def view_data_post():
    """Handles POST requests for /data."""
    return "Data updated successfully (POST)."

# 3. Setup Function 3 (PUT)
@app.route('/data', methods=['PUT'])
def view_data_put():
    """Handles PUT requests for /data."""
    return "Data replaced successfully (PUT)."

# 4. Conflict Introduction and Documentation:
# The following code block, if uncommented, will cause the application to crash
# upon startup because Flask detects a conflict in the routing table.

"""
# @app.route('/data', methods=['GET'])
# def view_data_get_conflict():
#     return "This will never run."

# Observation and Documentation:
# When attempting to run the application with the conflicting route uncommented,
# Flask raises an AssertionError similar to:
# "AssertionError: View function mapping is overwriting an existing endpoint function: view_data_get"
# This confirms that Flask prevents two different functions (view_data_get and view_data_get_conflict)
# from being mapped to the exact same URL path ('/data') and the exact same HTTP method (GET).
"""

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True)

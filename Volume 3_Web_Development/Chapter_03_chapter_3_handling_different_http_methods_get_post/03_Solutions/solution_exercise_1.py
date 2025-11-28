
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

from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key 
app.config['SECRET_KEY'] = 'a_very_secure_secret_key_for_book_3'

# --- Exercise 1: The Query Parameter Calculator (GET) ---
@app.route('/calculate', methods=['GET'])
def calculate():
    """
    Handles arithmetic calculations based on URL query parameters (GET).
    Example: /calculate?num1=10&num2=5&op=add
    """
    try:
        # Retrieve parameters using request.args
        num1_str = request.args.get('num1')
        num2_str = request.args.get('num2')
        op = request.args.get('op')

        # 1. Check for missing required parameters
        if not num1_str or not num2_str or not op:
            return "Error: Missing one or more parameters (num1, num2, op).", 400

        # 2. Type conversion and error handling (must be numbers)
        try:
            num1 = float(num1_str)
            num2 = float(num2_str)
        except ValueError:
            return "Error: num1 and num2 must be valid numbers.", 400

        result = None
        
        # 3. Operation handling
        if op == 'add':
            result = num1 + num2
        elif op == 'subtract':
            result = num1 - num2
        elif op == 'multiply':
            result = num1 * num2
        elif op == 'divide':
            # 4. Division by zero handling
            if num2 == 0:
                return "Error: Cannot divide by zero.", 400
            result = num1 / num2
        else:
            return f"Error: Unsupported operation '{op}'. Supported: add, subtract, multiply, divide.", 400

        # Success return
        return f"The result of {num1} {op} {num2} is: {result}", 200

    except Exception as e:
        # Generic catch-all for unexpected server errors
        return f"Internal Server Error: {e}", 500

# --- Exercise 2: Simple Feedback Submission (GET/POST) ---
@app.route('/feedback', methods=['GET', 'POST'])
def feedback_handler():
    """
    Displays a form on GET and processes form data on POST.
    """
    # 1. Handle GET request: Display the form
    if request.method == 'GET':
        html_form = """
        <!doctype html>
        <title>Submit Feedback</title>
        <h1>Submit Your Feedback</h1>
        <form method="POST" action="/feedback">
            <label for="name">Your Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>
            
            <label for="message">Your Message:</label><br>
            <textarea id="message" name="message" rows="4" cols="50" required></textarea><br><br>
            
            <input type="submit" value="Send Feedback">
        </form>
        """
        return html_form

    # 2. Handle POST request: Process form data
    elif request.method == 'POST':
        # Retrieve data using request.form
        name = request.form.get('name')
        message = request.form.get('message')

        # Basic Validation: Check if fields are present
        if not name or not message:
            return "Error: Name and Message fields are required.", 400

        # Confirmation
        return f"Thank you, {name}, your feedback has been successfully recorded."

# --- Exercise 3: The Restricted Access Gate (Combined Logic) ---
@app.route('/gate', methods=['GET', 'POST'])
def access_gate():
    """
    Requires a specific password submitted via POST to grant access.
    """
    SECRET_PASSWORD = "OpenSesame123"
    
    # HTML form structure (used for both GET display and POST failure return)
    # The {message} placeholder is used to inject an error or success message.
    gate_form_html = """
    <!doctype html>
    <title>Access Gate</title>
    <h1 style="color: black;">Restricted Access Gate</h1>
    <p style="color: red;">{message}</p>
    <form method="POST" action="/gate">
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Attempt Access">
    </form>
    """
    
    if request.method == 'GET':
        # GET Behavior: Display form with no initial message
        return gate_form_html.format(message="")

    elif request.method == 'POST':
        submitted_password = request.form.get('password')

        if submitted_password == SECRET_PASSWORD:
            # POST Behavior (Success)
            return "ACCESS GRANTED: Welcome to the Secret Vault.", 200
        else:
            # POST Behavior (Failure)
            error_message = "ACCESS DENIED. Incorrect password."
            # Return the failure message and the form (401 Unauthorized status)
            return gate_form_html.format(message=error_message), 401

# --- Exercise 4: Interactive Challenge: Enhancing the User Profile Editor ---
@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    """
    Handles profile updates, enforces validation, and returns JSON responses.
    """
    # Retrieve data from form submission, stripping whitespace
    email = request.form.get('email', '').strip()
    bio = request.form.get('bio', '').strip()
    
    # 1. Email Presence Validation
    if not email:
        return jsonify({
            "status": "error", 
            "message": "Email field cannot be empty."
        }), 400 # Return JSON with 400 Bad Request

    # 2. Email Format Validation (must contain @)
    if '@' not in email:
        return jsonify({
            "status": "error", 
            "message": "Invalid email format. Must contain '@' symbol."
        }), 400 # Return JSON with 400 Bad Request

    # If validation passes (simulated database update)
    # [Placeholder for actual database update logic]
    
    # 3. Success Response Modification (JSON with 200 status)
    return jsonify({
        "status": "success", 
        "message": f"Profile updated successfully for: {email}"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)

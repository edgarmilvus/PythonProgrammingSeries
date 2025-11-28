
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import os
from flask import Flask, session, redirect, url_for, request, escape
from werkzeug.security import generate_password_hash, check_password_hash

# --- 1. CONFIGURATION AND SETUP ---
# Initialize Flask app
app = Flask(__name__)
# CRITICAL: Set a strong, randomly generated secret key. 
# This key is used to cryptographically sign the session cookie data, 
# preventing tampering by the client.
app.secret_key = os.urandom(24) 

# --- 2. SIMULATED DATABASE ---
# In a production environment, this data would persist in a secure database.
# Structure: {'username': {'password_hash': '...', 'notes': [...]}}
USERS_DB = {}

# --- 3. UTILITY FUNCTIONS ---

def get_user_data(username):
    """Retrieves user data safely from the simulated database."""
    return USERS_DB.get(username)

def get_current_user_id():
    """Checks the secure session dictionary for the currently logged-in user ID."""
    # The session object is a proxy for the data stored in the signed cookie.
    return session.get('user_id')

# --- 4. AUTHENTICATION ROUTES ---

@app.route('/')
def index():
    """The main dashboard view. Serves as the protected resource."""
    user_id = get_current_user_id()
    
    if user_id:
        # User is logged in. Fetch personalized data.
        user_data = get_user_data(user_id)
        
        # Simple HTML simulation for displaying notes
        notes_list = "\n".join([f"<li>{n}</li>" for n in user_data['notes']])
        
        # Display the dashboard with secure, escaped user data
        return (f"<h1>Welcome back, {escape(user_id)}!</h1>"
                f"<p>Your secure notes:</p><ul>{notes_list}</ul>"
                f"<p><a href='{url_for('add_note')}'>Add Note</a> | "
                f"<a href='{url_for('logout')}'>Logout</a></p>")
    else:
        # User is not logged in. Prompt for action.
        return (f"<h1>Welcome to the Secure Note Tracker</h1>"
                f"<p>Please <a href='{url_for('login')}'>Login</a> or "
                f"<a href='{url_for('register')}'>Register</a> to view your content.</p>")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration and secure password storage."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Missing username or password.", 400
        
        if get_user_data(username):
            return "User already exists. Try logging in.", 409

        # Hash the password using a secure, salted algorithm (provided by Werkzeug)
        hashed_password = generate_password_hash(password)
        
        # Store new user data
        USERS_DB[username] = {
            'password_hash': hashed_password,
            'notes': [f"Initial note for {username}"]
        }
        
        # Immediately establish the session state upon successful registration
        session['user_id'] = username
        return redirect(url_for('index'))
    
    # GET request: Show registration form
    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login, verifying credentials and establishing the session."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = get_user_data(username)

        # 1. Check if user exists. 2. Verify the submitted password against the hash.
        if user_data and check_password_hash(user_data['password_hash'], password):
            # Authentication successful. This line establishes the user's state.
            session['user_id'] = username 
            return redirect(url_for('index'))
        else:
            # Crucial: Use a generic message to avoid leaking information (e.g., "user not found")
            return "Invalid username or password.", 401
    
    # GET request: Show login form
    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """

@app.route('/logout')
def logout():
    """Handles user logout by clearing the session state."""
    # Safely remove the user identifier from the session dictionary
    session.pop('user_id', None) 
    return redirect(url_for('index'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    """A secure resource that requires explicit session authorization."""
    user_id = get_current_user_id()
    
    # Authorization check: If no session ID, redirect to login
    if not user_id:
        return redirect(url_for('login')) 

    if request.method == 'POST':
        note_content = request.form.get('note')
        if note_content:
            # Store the new note under the logged-in user's data
            USERS_DB[user_id]['notes'].append(escape(note_content))
        return redirect(url_for('index'))

    # GET request: Show note form
    return """
        <h2>Add a New Note</h2>
        <form method="post">
            Note Content: <textarea name="note"></textarea><br>
            <input type="submit" value="Save Note">
        </form>
    """

if __name__ == '__main__':
    # Note: Flask sessions rely on the secret key being set.
    app.run(debug=True)

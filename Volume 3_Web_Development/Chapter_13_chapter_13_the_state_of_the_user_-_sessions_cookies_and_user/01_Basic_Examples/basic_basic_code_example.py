
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

from flask import Flask, session, redirect, url_for, escape, render_template_string

# --- 1. Application Setup and Configuration ---

# Initialize the Flask application instance
app = Flask(__name__)

# CRITICAL SECURITY REQUIREMENT:
# Flask sessions are stored on the client side (in a cookie) but are signed
# by the server using this secret key. This prevents users from tampering
# with the session data, as the server can verify the signature.
app.secret_key = 'a_very_long_and_complex_secret_key_9876543210_do_not_use_in_production'

# Simple HTML template for displaying the results
HTML_TEMPLATE = """
<!doctype html>
<title>Session Visitor Counter</title>
<style>
    body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
    strong { color: #007bff; font-size: 1.2em; }
    .note { font-size: 0.8em; color: #6c757d; margin-top: 20px; }
</style>
<h1>Welcome Back!</h1>
<p>You have refreshed this page <strong>{{ count }}</strong> times during your current session.</p>
<p class="note">The server uses a session cookie to remember this count.</p>
<p><a href="{{ url_for('reset_session') }}">Reset Counter and Start New Session</a></p>
"""

# --- 2. Main Route: Tracking the Visits ---

@app.route('/')
def track_visits():
    """
    Handles the main page view, increments the visit counter stored in the session.
    """
    
    # 2a. Check if the 'visit_count' key already exists in the session dictionary.
    # This is how we determine if the user is visiting for the first time
    # during this specific session.
    if 'visit_count' in session:
        
        # 2b. Existing user: Retrieve the current count and increment it.
        # session.get('key') is safer than session['key'] if key might be missing,
        # but since we checked with 'in session', direct access is fine here.
        current_count = session['visit_count']
        session['visit_count'] = current_count + 1
        
    else:
        
        # 2c. New session: Initialize the counter to 1.
        # This key-value pair is immediately stored in the session object,
        # which Flask will serialize, sign, and send back to the client as a cookie.
        session['visit_count'] = 1

    # 2d. Render the template, passing the final count.
    return render_template_string(HTML_TEMPLATE, 
                                  count=session['visit_count'])

# --- 3. Utility Route: Session Reset ---

@app.route('/reset')
def reset_session():
    """
    Clears the 'visit_count' data from the session and redirects the user
    back to the main page to demonstrate a fresh start.
    """
    
    # Removes the specified key from the session dictionary.
    # The second argument (None) prevents an error if the key doesn't exist.
    session.pop('visit_count', None)
    
    # Redirect the user to the index page. This forces a new request,
    # and since 'visit_count' is now gone, the index route will re-initialize it to 1.
    return redirect(url_for('track_visits'))

# --- 4. Execution Block ---

if __name__ == '__main__':
    # Running the application.
    app.run(debug=True)


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

import time
from datetime import datetime, timedelta
from flask import Flask, request, session, redirect, url_for, render_template, make_response, flash

# --- Mock Data for Exercises 2 and 4 ---

# Mock Database for User 
MOCK_USERS = {
    "alice": {"id": 1, "password_hash": "$2b$12$4Lp5p.g8O.T1p.L5y.T1.O.T1p.L5y.T1.O.T1p.L5y.T1.O"}, # Mock hash
    "bob": {"id": 2, "password_hash": "..."}
}

# Mock Products for Exercise 2
MOCK_PRODUCTS = [
    {'id': 101, 'name': 'The Theory of Everything'},
    {'id': 102, 'name': 'Quantum Computing Mug'},
    {'id': 103, 'name': 'Python Developer Sticker'}
]

# --- Application Setup ---

app = Flask(__name__)
# Set a strong secret key for session signing
app.secret_key = 'super_secret_key_for_signing_sessions_12345'
# Set session to be permanent (required for permanent_session_lifetime to work, though we override the logic in E3)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60) 

# --- Exercise 1: Persistent User Preference Management via Cookies ---

@app.route('/')
def index():
    # 1. Read the cookie
    user_lang = request.cookies.get('user_language', 'en')
    
    greetings = {
        'en': "Hello, Welcome to the Python Web Series!",
        'es': "Hola, Bienvenido a la Serie Web Python!",
        'fr': "Bonjour, Bienvenue dans la Série Web Python!"
    }
    
    greeting = greetings.get(user_lang, greetings['en'])
    
    # Placeholder for rendering
    return f"""
    <h1>{greeting}</h1>
    <p>Your current language preference is: <strong>{user_lang}</strong></p>
    <p><a href="{url_for('settings')}">Change Language Settings</a></p>
    <hr>
    <h3>Navigation</h3>
    <p>E2: <a href="{url_for('product_list')}">Shopping Cart Demo</a></p>
    <p>E3: <a href="{url_for('login_e3')}">Inactivity Timeout Demo</a></p>
    <p>E4: <a href="{url_for('login_e4')}">2FA Flow Demo</a></p>
    <p><a href="{url_for('show_messages')}">View Flash Messages</a></p>
    """

@app.route('/settings')
def settings():
    # 2. Settings form
    return """
    <h2>Select Language</h2>
    <form method="POST" action="/set_language">
        <select name="language">
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
        </select>
        <button type="submit">Save Preference</button>
    </form>
    <p><a href="/">Back to Home</a></p>
    """

@app.route('/set_language', methods=['POST'])
def set_language():
    selected_lang = request.form.get('language')
    
    # 3. Create response and set the cookie
    response = make_response(redirect(url_for('index')))
    
    # Set cookie to expire in 365 days (31,536,000 seconds)
    response.set_cookie('user_language', selected_lang, max_age=31536000)
    
    return response

# --- Exercise 2: Session Shopping Cart ---

@app.route('/products')
def product_list():
    # Ensure cart is initialized
    if 'shopping_cart' not in session:
        session['shopping_cart'] = []
        
    output = "<h2>Available Products (E2 Cart Demo)</h2>"
    output += "<ul>"
    for product in MOCK_PRODUCTS:
        output += f"<li>{product['name']} (<a href='{url_for('add_item', product_id=product['id'])}'>Add to Cart</a>)</li>"
    output += "</ul>"
    output += f"<p><a href='{url_for('view_cart')}'>View Cart ({len(session['shopping_cart']) if 'shopping_cart' in session else 0} items)</a></p>"
    output += f"<p><a href='{url_for('index')}'>Back to Home</a></p>"
    
    return output

@app.route('/add/<int:product_id>')
def add_item(product_id):
    product = next((p for p in MOCK_PRODUCTS if p['id'] == product_id), None)
    
    if product:
        # 3. Append item to session list
        if 'shopping_cart' not in session:
            session['shopping_cart'] = []
            
        session['shopping_cart'].append({'id': product['id'], 'name': product['name']})
        flash(f"{product['name']} added to cart!", 'success')
    else:
        flash("Product not found.", 'error')
        
    return redirect(url_for('product_list'))

@app.route('/cart')
def view_cart():
    cart = session.get('shopping_cart', [])
    output = "<h2>Your Shopping Cart (E2)</h2>"
    
    if cart:
        output += "<ul>"
        for item in cart:
            output += f"<li>{item['name']}</li>"
        output += "</ul>"
        output += f"<p>Total Items: {len(cart)}</p>"
        output += f"<p><a href='{url_for('clear_cart')}'>Clear Cart</a></p>"
    else:
        output += "<p>Your cart is empty.</p>"
        
    output += f"<p><a href='{url_for('product_list')}'>Continue Shopping</a></p>"
    
    return output

@app.route('/clear')
def clear_cart():
    # 5. Clear the cart
    session['shopping_cart'] = []
    flash("Cart cleared!", 'info')
    return redirect(url_for('view_cart'))


# --- Exercise 3: Secure Session Inactivity Timeout ---

TIMEOUT_SECONDS = 300 # 5 minutes

def check_activity_timeout():
    """Checks for inactivity and clears session if timed out."""
    if session.get('logged_in'):
        last_activity = session.get('last_activity')
        current_time = time.time()
        
        if last_activity and (current_time - last_activity) > TIMEOUT_SECONDS:
            # Session timed out
            session.clear()
            flash("Session expired due to inactivity (5 minutes). Please log in again.", 'warning')
            return redirect(url_for('login_e3'))
        
        # Reset the timer (Crucial: updates the session timestamp)
        session['last_activity'] = current_time
    return None # No redirect needed

@app.before_request
def before_request_e3():
    """Applies the inactivity check globally, but only affects logged_in users."""
    # We apply this check only to the protected route /dashboard
    if request.path == url_for('dashboard'):
        response = check_activity_timeout()
        if response:
            return response


@app.route('/login_e3', methods=['GET', 'POST'])
def login_e3():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        # Mock password verification success
        if username in MOCK_USERS: 
            # 2. Login Simulation: Set logged_in and last_activity
            session['logged_in'] = True
            session['last_activity'] = time.time()
            flash("Login successful! Session timer started.", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.", 'error')

    return """
    <h2>E3 Login (Inactivity Timeout Demo)</h2>
    <p>Log in and wait 5 minutes without refreshing the dashboard to trigger timeout.</p>
    <form method="POST">
        Username: <input type="text" name="username" value="alice"><br>
        Password: <input type="password" name="password"><br>
        <button type="submit">Log In</button>
    </form>
    <p><a href="/">Home</a></p>
    """

@app.route('/dashboard')
def dashboard():
    # 3. Check 1 (Authentication)
    if not session.get('logged_in'):
        flash("Access denied. Please log in.", 'error')
        return redirect(url_for('login_e3'))
    
    # If the before_request hook didn't catch a timeout, the user is active.
    last_activity_dt = datetime.fromtimestamp(session['last_activity']).strftime('%H:%M:%S')
    return f"""
    <h2>Welcome to the Secure Dashboard (E3)!</h2>
    <p>Your session is active. Last activity recorded at: {last_activity_dt}</p>
    <p>Refresh this page to reset the 5-minute inactivity timer.</p>
    <p><a href="{url_for('logout_e3')}">Logout</a></p>
    """

@app.route('/logout_e3')
def logout_e3():
    # 4. Logout Route
    session.clear()
    flash("You have been successfully logged out.", 'info')
    return redirect(url_for('login_e3'))


# --- Exercise 4: Interactive Challenge (Mock 2FA) ---

@app.route('/login_e4', methods=['GET', 'POST'])
def login_e4():
    # If the user is already fully logged in, redirect them
    if session.get('user_id'):
        return redirect(url_for('protected_e4'))

    if request.method == 'POST':
        username = request.form.get('username')
        # Mock password verification success
        if username == 'alice': 
            user_id = MOCK_USERS['alice']['id']
            
            # 1. Modify Login: Set 2FA pending state
            session['2fa_pending'] = True
            session['temp_user_id'] = user_id
            
            flash("Password verified. Please complete Two-Factor Authentication.", 'info')
            return redirect(url_for('verify_2fa'))
        else:
            flash("Invalid credentials.", 'error')

        
    return """
    <h2>E4 Login (Step 1: Password Verification)</h2>
    <p>Use username 'alice' to proceed to 2FA.</p>
    <form method="POST">
        Username: <input type="text" name="username" value="alice"><br>
        Password: <input type="password" name="password"><br>
        <button type="submit">Log In</button>
    </form>
    <p><a href="/">Home</a></p>
    """

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    # 2. Check for 2FA Pending State
    if not session.get('2fa_pending') or not session.get('temp_user_id'):
        flash("Authentication flow interrupted. Please log in again.", 'error')
        return redirect(url_for('login_e4'))

    if request.method == 'POST':
        code = request.form.get('2fa_code')
        
        # Mock 2FA verification: Any non-empty code works for this exercise
        if code:
            # 3. Successful 2FA Submission
            user_id = session['temp_user_id']
            
            # Set official authentication marker
            session['user_id'] = user_id 
            
            # Clear temporary flags
            session.pop('2fa_pending', None)
            session.pop('temp_user_id', None)
            
            flash("2FA successful. You are now fully authenticated!", 'success')
            return redirect(url_for('protected_e4'))
        else:
            # Failed 2FA Attempt (Failure clears all state)
            session.clear()
            flash("2FA code required or verification failed. Session cleared for security.", 'error')
            return redirect(url_for('login_e4'))

    return """
    <h2>E4 Login (Step 2: 2FA Verification)</h2>
    <p>Enter the mock 2FA code (e.g., 123456):</p>
    <form method="POST">
        2FA Code: <input type="text" name="2fa_code"><br>
        <button type="submit">Verify Code</button>
    </form>
    <p><a href="/">Home</a></p>
    """

@app.route('/protected_e4')
def protected_e4():
    # 4. Updated Protected Route Check
    # Only check for the final, official authentication marker
    if not session.get('user_id'):
        flash("You must be fully authenticated to view this page.", 'error')
        return redirect(url_for('login_e4'))
        
    user_id = session['user_id']
    return f"""
    <h2>E4 Protected Dashboard</h2>
    <p>Welcome, User ID {user_id}. You are fully authenticated.</p>
    <p><a href="{url_for('logout_e4')}">Logout</a></p>
    """

@app.route('/logout_e4')
def logout_e4():
    # T3: Logout
    session.clear()
    flash("Logged out.", 'info')
    return redirect(url_for('login_e4'))


if __name__ == '__main__':
    # Add a simple route to display flash messages for testing
    @app.route('/messages')
    def show_messages():
        messages_html = []
        # request.get_flashed_messages(with_categories=True) retrieves messages
        for category, message in request.get_flashed_messages(with_categories=True):
            # Using basic inline styles for visual categories
            style = ""
            if category == 'error':
                style = "color: red; border: 1px solid red; padding: 5px;"
            elif category == 'warning':
                style = "color: orange; border: 1px solid orange; padding: 5px;"
            elif category == 'success':
                style = "color: green; border: 1px solid green; padding: 5px;"
            else:
                style = "border: 1px solid gray; padding: 5px;"

            messages_html.append(f'<div style="{style}">{category.upper()}: {message}</div>')
            
        return "<h2>Flashed Messages</h2>" + "".join(messages_html) + "<p><a href='/'>Home</a></p>"

    app.run(debug=True)

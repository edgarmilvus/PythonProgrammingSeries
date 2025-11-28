
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

# app.py
from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# --- Data Structures for Exercises ---

# Exercise 1 & 2 Data
INVENTORY_DATA = [
    {"id": 101, "name": "Quantum Processor", "stock": 45, "price": 1299.99, "status": "active"},
    {"id": 102, "name": "Neural Link Cable", "stock": 0, "price": 49.50, "status": "out_of_stock"},
    {"id": 103, "name": "Holographic Projector", "stock": 12, "price": 550.00, "status": "active"},
    {"id": 104, "name": "Flux Capacitor (Replica)", "stock": 3, "price": 999.00, "status": "low_stock"},
    {"id": 105, "name": "Chronometer", "stock": 78, "price": 15.99, "status": "active"},
]

USER_DATA = [
    {"username": "alpha_dev", "status": "active", "access_level": "admin", "last_login_days": 1},
    {"username": "beta_tester", "status": "pending_approval", "access_level": "user", "last_login_days": 90},
    {"username": "gamma_guest", "status": "active", "access_level": "guest", "last_login_days": 5},
    {"username": "delta_banned", "status": "banned", "access_level": "user", "last_login_days": 150},
    {"username": "epsilon_user", "status": "active", "access_level": "user", "last_login_days": 30},
]

# --- Flask Routes ---

@app.route('/')
def index():
    """Route for Exercise 3 & 4 (Base Page)"""
    return render_template('index.html', current_page='home')

@app.route('/inventory')
def inventory_dashboard():
    """Route for Exercise 1 & 5"""
    # Pass the inventory list and a simple title variable
    return render_template('inventory.html', 
                           title="Warehouse Inventory Report", 
                           products=INVENTORY_DATA,
                           current_page='inventory') # Adding current_page for consistency

@app.route('/users')
def user_management():
    """Route for Exercise 2 & 4"""
    # Pass the user list
    return render_template('user_dashboard.html', 
                           users=USER_DATA,
                           current_page='users')

@app.route('/about')
def about_page():
    """Route for Exercise 3 & 4"""
    return render_template('about.html', current_page='about')

if __name__ == '__main__':
    # Ensure Flask runs in debug mode for development
    app.run(debug=True)


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

from flask import Flask, Blueprint, render_template_string

# ----------------------------------------------------------------------
# SIMULATED FILE 1: Blueprint Definition (e.g., 'auth_routes.py')
# ----------------------------------------------------------------------

# 1. Create a Blueprint instance
# 'auth' is the name of this blueprint.
# __name__ refers to the current module/file.
# url_prefix ensures all routes in this blueprint start with '/authentication'
auth_bp = Blueprint('auth', __name__, url_prefix='/authentication')

@auth_bp.route('/login')
def login():
    """Defines the login route within the auth blueprint."""
    content = """
    <h1>Authentication Module: Login</h1>
    <p>This route is handled entirely by the 'auth' blueprint.</p>
    <p>Try visiting the logout route: /authentication/logout</p>
    """
    return render_template_string(content)

@auth_bp.route('/logout')
def logout():
    """Defines the logout route within the auth blueprint."""
    return "You have been successfully logged out from the Auth system."

# ----------------------------------------------------------------------
# SIMULATED FILE 2: Main Application Setup (e.g., 'app.py')
# ----------------------------------------------------------------------

def create_app():
    """
    Function responsible for creating and configuring the Flask application.
    (This structure naturally leads to the Application Factory pattern.)
    """
    # Initialize the core application
    app = Flask(__name__)

    # Register the blueprint. This is the critical step where the modular
    # routes defined in auth_bp are merged into the main application.
    app.register_blueprint(auth_bp)

    # Define a route that belongs directly to the main application
    @app.route('/')
    def index():
        return "<h1>Main Application Index</h1><p>Go to /authentication/login to see the Blueprint routes.</p>"

    return app

# ----------------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Create and run the application instance
    app = create_app()
    # In a live environment, this would start the server:
    # app.run(debug=True)

    # Outputting the routes to confirm successful registration
    print("--- Blueprint Registration Successful ---")
    print(f"Main App Route: /")
    print(f"Blueprint Routes (prefixed by '{auth_bp.url_prefix}'):")
    print(f" - {auth_bp.url_prefix}/login")
    print(f" - {auth_bp.url_prefix}/logout")


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

import sys
from flask import Flask, Blueprint, jsonify

# --- 1. BLUEPRINT DEFINITION (Simulates routes/api_v1.py) ---

# Initialize a Blueprint object. This acts as a modular container for routes.
# 'simple_api' is the name of the blueprint.
# url_prefix ensures all routes defined in this blueprint start with /api/v1
api_bp = Blueprint('simple_api', __name__, url_prefix='/api/v1')

# Define a route using the blueprint object, not the main app object.
@api_bp.route('/status', methods=['GET'])
def get_api_status():
    """
    Endpoint to check the status of the API component.
    """
    # APIs communicate using JSON (JavaScript Object Notation).
    # jsonify converts the Python dictionary into a proper JSON response object.
    response_data = {
        "status": "active",
        "service": "Blogging Platform API Core",
        "version": "v1.0"
    }
    return jsonify(response_data), 200 # Return data and HTTP status code 200 (OK)

# --- 2. APPLICATION FACTORY AND REGISTRATION (Simulates app.py) ---

def create_app():
    """
    Application factory function: standard practice for configuring Flask apps.
    """
    # Initialize the main Flask application instance
    app = Flask(__name__)

    # CRITICAL STEP: Register the Blueprint with the main application.
    # This connects the modular routes defined in api_bp to the main app's routing system.
    app.register_blueprint(api_bp)

    return app

# --- 3. EXECUTION BLOCK ---

if __name__ == '__main__':
    # Create the application instance
    app = create_app()

    # Inform the user where to access the route
    print("-" * 50)
    print("FLASK BLUEPRINT EXAMPLE RUNNING")
    print(f"Access the status endpoint at: http://127.0.0.1:5000{api_bp.url_prefix}/status")
    print("-" * 50)

    # Start the development server
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("\nServer shutting down.")
        sys.exit(0)

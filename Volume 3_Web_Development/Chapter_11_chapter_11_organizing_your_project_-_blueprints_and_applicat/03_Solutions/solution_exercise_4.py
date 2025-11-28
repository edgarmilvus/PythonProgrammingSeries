
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

from flask import Flask, jsonify

# --- 1. Configuration Classes ---

class DevConfig:
    """Development configuration."""
    DEBUG = True
    SECRET_KEY = 'dev_key_secure_123'
    DATABASE_URI = 'sqlite:///dev.db'

class TestConfig:
    """Testing configuration."""
    DEBUG = False
    TESTING = True # Essential for Flask testing context
    SECRET_KEY = 'test_key_insecure_999'
    DATABASE_URI = 'sqlite:///:memory:' # Use in-memory DB for tests

# --- 2. Configuration Mapping ---
config_map = {
    'development': DevConfig,
    'testing': TestConfig
}

# --- 3. Application Factory ---
def create_app(config_name):
    """
    The Application Factory function.
    Creates and configures the Flask application instance.
    """
    # 1. Instantiate the core application
    app = Flask(__name__)

    # 2. Load configuration based on the input name
    if config_name in config_map:
        app.config.from_object(config_map[config_name])
    else:
        # Fallback to development if name is unknown
        app.config.from_object(DevConfig)

    # 3. Register a basic route for verification
    @app.route('/config')
    def show_config():
        return jsonify(
            secret_key=app.config.get('SECRET_KEY'),
            is_testing=app.config.get('TESTING'),
            db_uri=app.config.get('DATABASE_URI')
        )

    # Note: Blueprints and extensions would be registered here
    return app

# --- 4. Execution Demonstration (Verification) ---

# 1. Create a development environment app
dev_app = create_app('development')
with dev_app.test_client() as client:
    print("--- Development Environment Test ---")
    response = client.get('/config')
    print(f"Status: {response.status_code}")
    print(f"Config: {response.get_json()}")

# 2. Create a testing environment app
test_app = create_app('testing')
with test_app.test_client() as client:
    print("\n--- Testing Environment Test ---")
    response = client.get('/config')
    print(f"Status: {response.status_code}")
    print(f"Config: {response.get_json()}")

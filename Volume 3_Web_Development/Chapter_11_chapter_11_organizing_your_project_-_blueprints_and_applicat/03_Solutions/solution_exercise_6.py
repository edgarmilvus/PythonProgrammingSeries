
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

from flask import Flask, jsonify
# Note: We assume admin/routes.py exists in the same directory structure

# Configuration Classes (Updated with ADMIN_ENABLED)
class DevConfig:
    DEBUG = True
    SECRET_KEY = 'dev_key_secure_123'
    ADMIN_ENABLED = True # Admin is ON in development

class TestConfig:
    DEBUG = False
    TESTING = True
    SECRET_KEY = 'test_key_insecure_999'
    ADMIN_ENABLED = False # Admin is OFF during testing

config_map = {
    'development': DevConfig,
    'testing': TestConfig
}

def create_app(config_name):
    """Creates and configures the Flask application instance."""
    app = Flask(__name__)

    # 1. Load Configuration
    if config_name in config_map:
        app.config.from_object(config_map[config_name])
    else:
        app.config.from_object(DevConfig)

    # 2. Register Core Routes
    @app.route('/config')
    def show_config():
        return jsonify(
            admin_status=app.config.get('ADMIN_ENABLED'),
            environment=config_name
        )

    # 3. Conditional Blueprint Registration
    # Import the Blueprint here to ensure it uses the factory's context
    from admin.routes import admin_bp

    if app.config.get('ADMIN_ENABLED'):
        print(f"Registering Admin Blueprint for {config_name} environment.")
        app.register_blueprint(admin_bp)
    else:
        print(f"Skipping Admin Blueprint registration for {config_name} environment.")

    return app

# --- Verification ---

# Test 1: Development (Admin ON)
dev_app = create_app('development')
with dev_app.test_client() as client:
    print("\n--- Development Test (Admin ON) ---")
    response_admin = client.get('/admin/dashboard')
    print(f"Admin Dashboard Status (Dev): {response_admin.status_code}")
    print(f"Admin Dashboard Content (Dev): {response_admin.data.decode().strip()}")

# Test 2: Testing (Admin OFF)
test_app = create_app('testing')
with test_app.test_client() as client:
    print("\n--- Testing Test (Admin OFF) ---")
    response_admin = client.get('/admin/dashboard')
    print(f"Admin Dashboard Status (Test): {response_admin.status_code}")
    if response_admin.status_code == 404:
        print("Verification successful: Admin Blueprint correctly skipped.")
    else:
        print("Verification failed: Admin Blueprint should be inaccessible.")

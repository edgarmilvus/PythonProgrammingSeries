
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

# health_tracker.py - A Production-Ready Flask API for Service Status Checks

import os
import json
from flask import Flask, request, jsonify, render_template_string

# --- Configuration and Initialization ---

# Define the application object required by WSGI servers (Gunicorn)
# Gunicorn will import this file and look for the 'app' callable instance.
app = Flask(__name__)

# Simulated Database: In production, this data would reside in PostgreSQL or MySQL.
# We use a simple dictionary here to maintain state across requests (in a single process model).
# NOTE: When Gunicorn runs multiple workers, this dictionary will be separate for each worker,
# highlighting why a true database is necessary for persistent, shared state.
SERVICE_DATA = {
    "backend_api": {"status": "Operational", "last_check": "2023-10-27T10:00:00Z", "uptime_percent": 99.9},
    "database_orm": {"status": "Operational", "last_check": "2023-10-27T10:05:00Z", "uptime_percent": 99.8},
    "external_auth": {"status": "Degraded", "last_check": "2023-10-27T10:10:00Z", "uptime_percent": 95.1}
}

# Simple HTML template for the root endpoint (demonstrates templating capability)
HOME_TEMPLATE = """
<!doctype html>
<title>Service Health Dashboard</title>
<h1>Welcome to the Production Health Tracker</h1>
<p>This application is designed to run behind a robust WSGI server like Gunicorn, proxied by Nginx.</p>
<p>Access /api/status for JSON data.</p>
"""

# --- API Routes ---

@app.route('/')
def index():
    # Root endpoint serves simple HTML to confirm the service is reachable.
    # This is often used by Nginx health checks.
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/status', methods=['GET'])
def get_all_statuses():
    # Returns the full status dictionary as a JSON response.
    # This endpoint is read-only.
    return jsonify({"services": SERVICE_DATA, "count": len(SERVICE_DATA)})

@app.route('/api/status/<string:service_name>', methods=['GET'])
def get_service_status(service_name):
    # Retrieve status for a specific service by name.
    service_data = SERVICE_DATA.get(service_name)
    if service_data:
        return jsonify({service_name: service_data})
    # Return a 404 error if the service is not found, adhering to REST principles.
    return jsonify({"error": f"Service '{service_name}' not found"}), 404

@app.route('/api/update/<string:service_name>', methods=['POST'])
def update_service_status(service_name):
    # This critical endpoint handles status updates via POST requests.
    # It simulates the process of an external monitor reporting back.
    if service_name not in SERVICE_DATA:
        return jsonify({"error": f"Service '{service_name}' not recognized"}), 400

    # Ensure the request body is valid JSON and contains required fields
    try:
        data = request.get_json()
        if not data or 'status' not in data or 'last_check' not in data:
            return jsonify({"error": "Missing required fields (status, last_check) in JSON payload"}), 400
    except Exception:
        # Catches cases where the Content-Type is wrong or the JSON is malformed
        return jsonify({"error": "Invalid JSON format or missing Content-Type: application/json header"}), 400

    # Update the simulated database entry (state change)
    SERVICE_DATA[service_name]['status'] = data['status']
    SERVICE_DATA[service_name]['last_check'] = data['last_check']

    # Optionally update uptime if provided in the payload
    if 'uptime_percent' in data:
        SERVICE_DATA[service_name]['uptime_percent'] = data['uptime_percent']

    # Return the updated data structure and a 200 OK status
    return jsonify({"message": f"Status for {service_name} updated successfully",
                    "new_status": SERVICE_DATA[service_name]}), 200


# --- Entry Point for Development Server ---

if __name__ == '__main__':
    # CRITICAL: This block is ONLY for local development using the built-in Flask server.
    # In a production deployment (using Gunicorn), this block is entirely ignored.
    # Gunicorn imports 'health_tracker' and calls the 'app' object directly.
    app.run(host='0.0.0.0', port=5000, debug=True)

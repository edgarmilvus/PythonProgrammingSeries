
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

from flask import Flask, jsonify, make_response
import json # Included for conceptual completeness, though not strictly needed for basic jsonify

# 1. Initialize the Flask application
app = Flask(__name__)

# Define a simple data structure (a Python dictionary)
# This represents the information we want to share about our API's status.
API_DATA = {
    "service_name": "Inventory_Service_V1",
    "status": "Operational",
    "version": 1.0,
    "endpoints_available": ["/api/status", "/api/item/<id>"],
    "timestamp": "2024-05-15T10:00:00Z"
}

# 2. Define the API endpoint route for the health check
@app.route('/api/status', methods=['GET'])
def get_api_status():
    """
    Handles GET requests to /api/status.
    Returns the current operational status of the service as JSON data.
    """
    
    # 3. Use jsonify to convert the Python dictionary (API_DATA) into a JSON response object.
    # jsonify automatically serializes the data and sets the Content-Type header.
    json_response_body = jsonify(API_DATA)

    # 4. Explicitly create the full response object and set the HTTP status code.
    # We use make_response to combine the JSON body and the status code (200 OK).
    # The status code 200 is the universal signal for 'Success'.
    response = make_response(json_response_body, 200)
    
    # 5. Return the final response object to the client
    return response

# 6. Define a second endpoint demonstrating mandatory error handling (404 Not Found)
@app.route('/api/item/<int:item_id>', methods=['GET'])
def get_item_details(item_id):
    """
    Simulates retrieving an item based on its ID. 
    If the ID is 42, it succeeds (200). Otherwise, it fails (404).
    """
    
    if item_id == 42:
        # Success case: Item found. We use the Flask shorthand for success.
        item_data = {"id": 42, "name": "Flux Capacitor", "price": 1985.00}
        
        # Flask shortcut: returning a tuple (body, status_code) is equivalent to using make_response
        return jsonify(item_data), 200 
    else:
        # Failure case: Item not found.
        error_message = {
            "error": "Resource Not Found",
            "message": f"The requested item with ID {item_id} could not be located in the inventory."
        }
        
        # Crucial step: Returning the appropriate error status code (404 Not Found)
        return jsonify(error_message), 404

# 7. Run the application
if __name__ == '__main__':
    # The application will start listening on http://127.0.0.1:5000/
    app.run(debug=True)

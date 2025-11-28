
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

import json
from flask import Flask, jsonify, request, abort

# --- Dummy Data Store ---
PRODUCTS = {
    101: {"name": "Quantum Processor Kit", "price": 199.99, "category": "Hardware", "stock": 5},
    102: {"name": "Neural Network Library v3.0", "price": 49.99, "category": "Software", "stock": 150},
    103: {"name": "Data Science Handbook", "price": 29.99, "category": "Book", "stock": 300},
    104: {"name": "IoT Sensor Pack", "price": 75.00, "category": "Hardware", "stock": 0},
}

TASKS = [
    {"id": 201, "description": "Implement User Authentication", "status": "pending", "priority": "high"},
    {"id": 202, "description": "Optimize Database Queries", "status": "done", "priority": "medium"},
    {"id": 203, "description": "Write API Documentation", "status": "pending", "priority": "low"},
    {"id": 204, "description": "Review Pull Requests", "status": "done", "priority": "high"},
    {"id": 205, "description": "Setup CI/CD Pipeline", "status": "pending", "priority": "medium"},
]

ORDERS = {
    5001: {
        "order_id": 5001,
        "date": "2024-05-15",
        "customer_info": {
            "name": "Alex Turing",
            "email": "alex@example.com"
        },
        "items": [
            {"product_id": 101, "quantity": 1, "unit_price": 199.99},
            {"product_id": 103, "quantity": 2, "unit_price": 29.99}
        ],
        "total_amount": 259.97
    }
}

app = Flask(__name__)

# Helper function used primarily for Exercise 2 where specific validation messages are needed
def error_response(message, status_code):
    """Returns a simple standardized JSON error response."""
    return jsonify({"status": "error", "message": message}), status_code

# ----------------------------------------------------------------------
# SOLUTION 4: Interactive Challenge - Enforcing a Standardized Error Schema
# (This must be defined and registered before the routes that use 'abort')
# ----------------------------------------------------------------------

def handle_http_error(e):
    """
    Catches HTTP errors (400, 404, etc.) and returns a standardized JSON response 
    based on the required schema.
    """
    # Safely retrieve the status code and description from the exception object
    status_code = getattr(e, 'code', 500)
    message = getattr(e, 'description', 'An unknown server error occurred.')
    
    # Override generic descriptions for cleaner API output
    if status_code == 404:
        message = "The requested resource could not be found."
    elif status_code == 400 and not getattr(e, 'description'):
        message = "The request was malformed or missing required parameters."

    response = {
        "status": "error",
        "code": status_code,
        "message": message
    }
    return jsonify(response), status_code

# Register the handlers for 400 and 404
app.register_error_handler(404, handle_http_error)
app.register_error_handler(400, handle_http_error)


# ----------------------------------------------------------------------
# SOLUTION 1: Resource Retrieval and Explicit 404 Handling
# (Uses abort(404) to test the standardized handler from Solution 4)
# ----------------------------------------------------------------------
@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = PRODUCTS.get(product_id)
    
    if product is None:
        # Triggers the global 404 handler (Solution 4)
        abort(404) 
    
    # Success case: return data and explicitly set 200 OK
    return jsonify(product), 200


# ----------------------------------------------------------------------
# SOLUTION 2: Input Validation and HTTP 400 Responses
# ----------------------------------------------------------------------
@app.route('/api/v1/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if not data:
        # Triggers the global 400 handler (Solution 4)
        abort(400, description="No JSON payload provided in the request body.")
    
    required_fields = ['name', 'price', 'category']
    # Efficiently find missing fields
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        # Return a custom 400 response with detailed validation error
        message = f"Missing required fields: {', '.join(missing_fields)}"
        return error_response(message, 400)
        
    # Simulate resource creation
    # Find the next available ID
    new_id = max(PRODUCTS.keys()) + 1
    new_product = {
        "id": new_id,
        "name": data['name'],
        "price": data['price'],
        "category": data['category']
    }
    PRODUCTS[new_id] = new_product # Update in-memory store
    
    # Return the created resource with 201 status (Created)
    return jsonify(new_product), 201


# ----------------------------------------------------------------------
# SOLUTION 3: Dynamic Filtering with Query Parameters
# ----------------------------------------------------------------------
@app.route('/api/v1/tasks', methods=['GET'])
def list_tasks():
    # Retrieve the 'status' query parameter, returns None if not present
    status_filter = request.args.get('status')
    
    if status_filter:
        # Filter the list based on the provided status (case-insensitive comparison)
        filtered_tasks = [
            task for task in TASKS 
            if task['status'].lower() == status_filter.lower()
        ]
    else:
        # No filter provided, return all tasks
        filtered_tasks = TASKS
        
    # Return the resulting list (empty list is acceptable for 200 OK)
    return jsonify(filtered_tasks), 200


# ----------------------------------------------------------------------
# SOLUTION 5: Complex Data Structures and Nested JSON Responses
# ----------------------------------------------------------------------
@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = ORDERS.get(order_id)
    
    if order is None:
        # Triggers the standardized 404 handler
        abort(404)
        
    # jsonify automatically handles the deep nesting of dictionaries and lists
    return jsonify(order), 200


# Example of running the application (uncomment to test locally)
# if __name__ == '__main__':
#     app.run(debug=True)

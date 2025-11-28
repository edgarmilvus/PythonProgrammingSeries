
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

from flask import Flask, jsonify, request
import uuid
# Import HTTPStatus for explicit, readable status code definitions
from http import HTTPStatus 

# 1. Initialization and Data Setup
app = Flask(__name__)

# In-memory database simulation: A list of product dictionaries
# In a real application, this would be replaced by a database connection (e.g., SQLAlchemy)
products = [
    {"id": "a1b2c3d4", "name": "Quantum Processor", "price": 1200.00, "in_stock": True},
    {"id": "e5f6g7h8", "name": "Ergonomic Keyboard", "price": 75.50, "in_stock": False},
]

# Utility function to generate unique IDs for new products
def generate_unique_id():
    # Generates a short, readable UUID fragment for simplicity
    return str(uuid.uuid4())[:8]

# Utility function for basic input validation on POST requests
def validate_product_data(data):
    required_fields = ['name', 'price']
    
    # Check for presence of required keys
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Check for valid data types and business logic constraints
    price = data.get('price')
    if not isinstance(price, (int, float)) or price <= 0:
        return False, "Price must be a positive numeric value."
        
    return True, None

# 2. Endpoint for Listing and Creating Products (Collection Resource)
# This single function handles both GET (retrieve all) and POST (create new)
@app.route('/api/v1/products', methods=['GET', 'POST'])
def handle_products():
    
    # --- Handle GET Request: Retrieve all products ---
    if request.method == 'GET':
        # Use jsonify to serialize the Python list into a JSON array structure
        # The structure includes metadata (status, count) for robustness
        return jsonify({
            "status": "success",
            "count": len(products),
            "data": products
        }), HTTPStatus.OK # Explicitly return 200 OK
        
    # --- Handle POST Request: Create a new product ---
    elif request.method == 'POST':
        
        # 400 Bad Request check: Ensure client sent JSON data
        if not request.is_json:
            return jsonify({
                "status": "error", 
                "message": "Content-Type header must be application/json"
            }), HTTPStatus.BAD_REQUEST 

        # Extract the JSON payload from the request body
        data = request.get_json()
        
        # Validate the incoming data structure
        is_valid, error_msg = validate_product_data(data)
        if not is_valid:
            # 400 Bad Request if validation fails
            return jsonify({"status": "error", "message": error_msg}), HTTPStatus.BAD_REQUEST 

        # Construct the new product dictionary with a generated ID
        new_product = {
            "id": generate_unique_id(),
            "name": data['name'],
            "price": data['price'],
            # Safely retrieve optional fields, defaulting to True
            "in_stock": data.get('in_stock', True) 
        }

        # Persist the new product to our in-memory storage
        products.append(new_product)

        # Return the newly created resource. Use 201 CREATED status code 
        # as mandated by REST principles for successful resource creation.
        return jsonify({
            "status": "created", 
            "data": new_product
        }), HTTPStatus.CREATED 

# 3. Endpoint for Retrieving a Single Product (Item Resource)
@app.route('/api/v1/products/<product_id>', methods=['GET'])
def get_product(product_id):
    
    # Use a generator expression and next() for efficient searching
    # next() returns the first match or None if no match is found
    found_product = next((p for p in products if p['id'] == product_id), None)

    if found_product:
        # Resource found, return data with 200 OK
        return jsonify({
            "status": "success",
            "data": found_product
        }), HTTPStatus.OK 
    else:
        # Resource not found, return 404 Not Found
        return jsonify({
            "status": "error", 
            "message": f"Product with ID '{product_id}' not found."
        }), HTTPStatus.NOT_FOUND 

# 4. Run the Application
if __name__ == '__main__':
    # Running the application starts the development server
    app.run(debug=True)

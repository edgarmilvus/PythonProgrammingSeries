
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

# inventory_tracker.py
# A Flask application demonstrating combined GET (retrieval/search) and POST (submission/update) handling.

from flask import Flask, request, render_template, redirect, url_for

# --- 1. Initialization and Configuration ---
app = Flask(__name__)
# Note: SECRET_KEY is required if sessions or flash messages were used. Included for completeness.
app.config['SECRET_KEY'] = 'secure_development_key_12345'

# Simple in-memory database structure (Key: SKU, Value: Item Details Dictionary)
INVENTORY = {
    "SKU-001": {"name": "Laptop Charger", "stock": 50, "location": "Aisle 1"},
    "SKU-002": {"name": "Wireless Mouse", "stock": 120, "location": "Aisle 2"},
    "SKU-003": {"name": "Mechanical Keyboard", "stock": 35, "location": "Aisle 3"},
}

# --- 2. Utility Function for Data Integrity ---
def validate_submission(form_data):
    """Checks if required fields are present and ensures stock is a valid, non-negative integer."""
    required_fields = ['sku', 'item_name', 'stock', 'location']
    
    # Check for missing or empty fields
    if not all(field in form_data and form_data[field].strip() for field in required_fields):
        return False, "Missing required fields. Please fill out all fields."
    
    # Validate stock quantity type
    try:
        stock_value = int(form_data['stock'])
        if stock_value < 0:
             return False, "Stock quantity cannot be negative."
        return True, stock_value
    except ValueError:
        return False, "Stock must be a valid whole number (integer)."

# --- 3. Main Route Handler (GET and POST Combined) ---
@app.route('/', methods=['GET', 'POST'])
def inventory_manager():
    # Initialize message variable for user feedback
    feedback_message = None

    if request.method == 'POST':
        # --- POST Request Handling (Data Submission/Modification) ---
        
        # 3a. Retrieve data submitted via an HTML form (POST data is accessed via request.form)
        form_data = request.form
        
        is_valid, result = validate_submission(form_data)

        if is_valid:
            # Data is valid: result holds the validated integer stock value
            sku = form_data['sku'].strip().upper()
            item_name = form_data['item_name'].strip()
            new_stock = result 
            location = form_data['location'].strip()

            # 3b. Update or add the item in the in-memory database
            INVENTORY[sku] = {
                "name": item_name,
                "stock": new_stock,
                "location": location
            }
            feedback_message = f"SUCCESS: Item {sku} ({item_name}) updated/added. New stock: {new_stock}."
            
        else:
            # Handle validation failure (result holds the error message)
            feedback_message = f"ERROR: Submission failed. {result}"
            
    # --- GET Request Handling (Data Retrieval/Display/Search) ---
    
    # 4a. Handle optional search query parameters (GET data is accessed via request.args)
    # Default search query is an empty string if 'search' parameter is not present in the URL
    search_query = request.args.get('search', '').strip()
    
    display_inventory = INVENTORY
    
    if search_query:
        # 4b. Filter the inventory based on the search query
        search_term = search_query.lower()
        display_inventory = {
            sku: data for sku, data in INVENTORY.items()
            if search_term in sku.lower() or search_term in data['name'].lower()
        }
        
        # Update feedback message only if a search was performed
        if not feedback_message: # Don't overwrite a POST success/failure message
            feedback_message = f"Showing search results for '{search_query}'. Total items: {len(display_inventory)}"

    # 4c. Render the final template, passing the filtered data and feedback
    return render_template(
        'inventory_dashboard.html', 
        inventory=display_inventory, 
        feedback=feedback_message
    )

# --- 5. Application Entry Point ---
if __name__ == '__main__':
    # Running the application in debug mode for development
    app.run(debug=True)

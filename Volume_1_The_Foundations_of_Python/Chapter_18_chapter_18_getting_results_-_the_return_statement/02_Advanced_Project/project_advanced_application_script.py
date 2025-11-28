
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

# Inventory Management System: Simulating Order Processing and Result Handling

# 1. Initial Data Setup
INVENTORY_DATA = {
    "Laptop_X1": {"price": 1200.00, "stock": 5},
    "Monitor_M3": {"price": 350.00, "stock": 12},
    "Keyboard_K9": {"price": 75.00, "stock": 25},
    "Mouse_D2": {"price": 25.00, "stock": 0} # Item that is initially out of stock
}
TAX_RATE = 0.08  # 8% sales tax applied to all orders

# --- Helper Function 1: Data Retrieval ---

def retrieve_item_details(inventory, item_name):
    """
    Retrieves the price and current stock for a given item.
    Demonstrates returning multiple values (a tuple) or explicit None.
    Returns: (price, stock) tuple, or (None, None) if item is not found.
    """
    if item_name in inventory:
        details = inventory[item_name]
        # Returning multiple values packed into a tuple (price, stock)
        return details["price"], details["stock"]
    else:
        # Returning the explicit 'None, None' tuple signals failure clearly
        return None, None

# --- Helper Function 2: Calculation ---

def calculate_final_cost(unit_price, quantity, tax_rate):
    """
    Calculates the total cost including tax.
    Demonstrates returning a single, calculated float value.
    Returns: float (total cost), rounded to two decimal places.
    """
    subtotal = unit_price * quantity
    total_tax = subtotal * tax_rate
    final_total = subtotal + total_tax
    # Returning a single, calculated float value
    return round(final_total, 2)

# --- Helper Function 3: Validation ---

def check_availability(current_stock, requested_quantity):
    """
    Checks if the requested quantity is available.
    Demonstrates returning a status flag (boolean) paired with data (integer).
    Returns: (is_available: bool, remaining_stock: int) tuple.
    """
    if requested_quantity <= 0:
        # Invalid request, return False status
        return False, current_stock

    if current_stock >= requested_quantity:
        remaining = current_stock - requested_quantity
        # Success status and calculated remaining stock
        return True, remaining
    else:
        # Failure status, returning current stock level for context
        return False, current_stock

# --- Core Processing Function (Orchestrator) ---

def process_order(inventory, order_details, tax_rate):
    """
    Processes a single customer order using returned values from helper functions.
    This function demonstrates mandatory structured returns and multiple exit points.

    Returns: A tuple (status_code: str, message: str, data_payload: dict/None)
    """
    item_name = order_details.get("item")
    quantity = order_details.get("quantity", 0)

    # 1. Validate Item Existence and Retrieve Details
    unit_price, current_stock = retrieve_item_details(inventory, item_name)

    if unit_price is None:
        # Early exit point 1: Item not found. Stops execution immediately.
        return ("ERROR", f"Item '{item_name}' not recognized in inventory.", None)

    # 2. Check Stock Availability
    is_available, remaining_stock = check_availability(current_stock, quantity)

    if not is_available:
        # Early exit point 2: Stock insufficient or quantity invalid. Stops execution.
        if quantity <= 0:
            msg = "Order quantity must be positive."
        else:
            msg = f"Insufficient stock. Requested {quantity}, but only {current_stock} available."
        
        # Return structured error details
        return ("ERROR", msg, {"requested": quantity, "available": current_stock})

    # 3. Calculate Final Cost (Only reached if checks pass)
    total_cost = calculate_final_cost(unit_price, quantity, tax_rate)

    # 4. Update Inventory (Simulation of transaction completion)
    # The dictionary is passed by reference, so this change persists outside the function.
    inventory[item_name]["stock"] = remaining_stock

    # Final successful exit point
    payload = {
        "item": item_name,
        "quantity_shipped": quantity,
        "total_cost": total_cost,
        "new_stock_level": remaining_stock
    }
    # Return structured success details
    return ("SUCCESS", f"Order for {quantity}x {item_name} processed.", payload)

# --- Execution Block and Testing ---

print("--- Inventory Status Before Orders ---")
print(INVENTORY_DATA)
print("-" * 35)

# Test Case 1: Successful Order
order_1 = {"item": "Monitor_M3", "quantity": 3}
# The caller immediately unpacks the returned tuple
status, message, data = process_order(INVENTORY_DATA, order_1, TAX_RATE)
print(f"[Order 1] Status: {status}")
print(f"Message: {message}")
if status == "SUCCESS":
    print(f"Data Payload: Total Cost: ${data['total_cost']}")

print("-" * 35)

# Test Case 2: Insufficient Stock (Triggers Early Exit 2)
order_2 = {"item": "Laptop_X1", "quantity": 10}
status, message, data = process_order(INVENTORY_DATA, order_2, TAX_RATE)
print(f"[Order 2] Status: {status}")
print(f"Message: {message}")
if status == "ERROR" and data:
    print(f"Details: Requested {data['requested']}, Available {data['available']}")

print("-" * 35)

# Test Case 3: Invalid Item (Triggers Early Exit 1)
order_3 = {"item": "Tablet_T5", "quantity": 1}
status, message, data = process_order(INVENTORY_DATA, order_3, TAX_RATE)
print(f"[Order 3] Status: {status}")
print(f"Message: {message}")

print("-" * 35)
print("--- Inventory Status After Orders ---")
print(INVENTORY_DATA)

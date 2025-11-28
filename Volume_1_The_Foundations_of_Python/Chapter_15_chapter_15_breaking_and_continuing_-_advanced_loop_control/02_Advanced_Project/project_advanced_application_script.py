
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

# inventory_processor.py
"""
Script demonstrating advanced loop control for inventory order processing.
Uses 'continue' for data filtering and 'break' for prioritized search termination.
"""

# --- 1. Simulation Data Setup ---

orders_data = [
    {"id": 1001, "status": "PENDING", "quantity": 50, "priority": "LOW"},
    {"id": 1002, "status": "RETURN", "quantity": 10, "priority": "MEDIUM"},  # Should be skipped (continue)
    {"id": 1003, "status": "PENDING", "quantity": -5, "priority": "HIGH"},   # Invalid quantity (continue)
    {"id": 1004, "status": "PENDING", "quantity": 150, "priority": "LOW"},
    {"id": 1005, "status": "URGENT", "quantity": 25, "priority": "CRITICAL"}, # Should trigger break
    {"id": 1006, "status": "PENDING", "quantity": 75, "priority": "MEDIUM"},
    {"id": 1007, "status": "PENDING", "quantity": 12, "priority": "HIGH"},
    {"id": 1008, "status": "RETURN", "quantity": 30, "priority": "LOW"},    # Should be skipped (continue)
    {"id": 1009, "status": "PENDING", "quantity": 200, "priority": "MEDIUM"},
]

# --- 2. Function for Data Validation (Using 'continue') ---

def validate_orders(orders: list[dict]) -> list[dict]:
    """
    Iterates through orders, validating data integrity. Uses 'continue' 
    to skip iterations that contain unusable or already resolved data.
    Returns a list of orders deemed valid for further processing.
    """
    valid_orders = []
    invalid_count = 0
    print("\n--- 1. Data Validation Pass (Using 'continue' for Filtering) ---")
    
    for order in orders:
        order_id = order.get('id', 'N/A')
        status = order.get('status', 'UNKNOWN')
        quantity = order.get('quantity', 0)

        # 2a. Integrity Check 1: Skip orders marked for return or cancellation.
        if status in ("RETURN", "CANCELED"):
            print(f"[SKIP: Status] Order {order_id}: Status is '{status}'. Skipping inventory update.")
            invalid_count += 1
            continue # Immediately jump to the next item in the list

        # 2b. Integrity Check 2: Validate quantity integrity (must be positive).
        if quantity <= 0:
            print(f"[SKIP: Data Error] Order {order_id}: Quantity ({quantity}) is invalid. Flagging error.")
            invalid_count += 1
            continue # Immediately jump to the next item in the list

        # If the loop reaches this point, the order is clean and ready.
        print(f"[VALID] Order {order_id} ({status}): Quantity {quantity}. Ready for processing queue.")
        valid_orders.append(order)
        
    print(f"\nValidation Summary: {len(valid_orders)} valid orders identified. {invalid_count} records skipped.")
    return valid_orders


# --- 3. Function for Urgent Search (Using 'break') ---

def process_urgent_search(orders: list[dict]):
    """
    Searches the order list for the first critically urgent item.
    Uses 'break' to terminate the search immediately upon finding the target, 
    maximizing response speed.
    """
    print("\n--- 2. Urgent Order Search (Using 'break' for Efficiency) ---")
    found_urgent = False
    
    # We prioritize speed; we only need to find the first critical item.
    for order in orders:
        order_id = order.get('id', 'N/A')
        priority = order.get('priority', 'LOW')
        status = order.get('status', 'PENDING')

        # Preliminary check: We only search within active, pending orders.
        if status in ("RETURN", "CANCELED"):
            continue # Use continue to ignore non-active orders efficiently

        # Critical condition: Check for highest priority flags
        if priority == "CRITICAL" or status == "URGENT":
            print(f"\n!!! IMMEDIATE ACTION REQUIRED !!!")
            print(f"Found CRITICAL Order {order_id}. Priority: {priority}. Quantity: {order['quantity']}.")
            print("Action: Initiating emergency fulfillment sequence.")
            found_urgent = True
            break # Terminate the entire loop immediately
        
        # Log search progress if not critical
        print(f"[Search] Checking Order {order_id} (Priority: {priority})...")
        
    if not found_urgent:
        print("\nSearch complete. No critical or urgent orders found in this batch.")


# --- 4. Main Execution Block ---

if __name__ == "__main__":
    
    print("Starting Inventory Order Processing Script...")
    
    # Step 1: Validate the raw incoming data (uses 'continue')
    validated_list = validate_orders(orders_data)
    
    print("\n" + "="*70)
    
    # Step 2: Search the validated list for the highest priority item (uses 'break')
    # Note: We pass the raw data here to show how the functions handle filtering independently.
    process_urgent_search(orders_data) 
    
    print("="*70)
    print("Script execution finished. All critical tasks prioritized.")


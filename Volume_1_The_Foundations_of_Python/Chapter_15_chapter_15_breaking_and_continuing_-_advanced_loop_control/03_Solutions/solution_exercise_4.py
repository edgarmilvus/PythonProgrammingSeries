
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

print("\n--- Exercise 4: Inventory Stock Optimization ---")

INVENTORY = {
    "A90": {"stock": 500, "status": "ACTIVE"},
    "B22": {"stock": 15, "status": "ACTIVE"},
    "C45": {"stock": 5, "status": "DISCONTINUED"},
    "D77": {"stock": 120, "status": "ACTIVE"},
    "E11": {"stock": 8, "status": "ACTIVE"}
}

ORDER_LIST = ["A90", "D77", "B22", "C45", "E11"]
CRITICAL_THRESHOLD = 10 
processed_count = 0

print(f"Starting order processing. Critical threshold: {CRITICAL_THRESHOLD} units.")

# Requirement 1: Iterate through the ORDER_LIST
for item_id in ORDER_LIST:
    item_data = INVENTORY.get(item_id)
    
    # Requirement 2: Use continue to bypass discontinued items
    if item_data and item_data["status"] == "DISCONTINUED":
        print(f"NOTICE: {item_id} is DISCONTINUED. Skipping item.")
        continue # Skips to the next item in ORDER_LIST

    # Check for active items
    if item_data and item_data["status"] == "ACTIVE":
        current_stock = item_data["stock"]
        
        # Requirement 3: Use break for critical low stock
        if current_stock <= CRITICAL_THRESHOLD:
            print(f"\n!!! CRITICAL ALERT: {item_id} Stock is {current_stock} !!!")
            print("Halting all order processing immediately.")
            break # Terminates the entire 'for' loop
            
        # Requirement 4: Confirmation for active, sufficient stock
        print(f"SUCCESS: {item_id} (Stock: {current_stock}) confirmed.")
        processed_count += 1
    else:
        # Handle items not found or with unknown status
        print(f"WARNING: Cannot process {item_id}.")


print(f"\nSimulation ended. Total active, sufficient items processed: {processed_count}")

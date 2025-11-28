
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

# Exercise 4: Interactive Challenge - Centralized Inventory Management

GLOBAL_TOTAL_STOCK = 1500
item_stock = {
    "Laptop": 300,
    "Monitor": 500,
    "Keyboard": 700
}

def check_inventory(item_name):
    """Reports the stock level for a specific item."""
    if item_name in item_stock:
        print(f"\n[INFO] Current stock of {item_name}: {item_stock[item_name]}")
    else:
        print(f"\n[INFO] Item {item_name} not found.")
    
    # Reads the global variable correctly
    print(f"[INFO] Overall warehouse stock: {GLOBAL_TOTAL_STOCK}")

# 1. Modified function to update GLOBAL_TOTAL_STOCK
def process_shipment_in(item_name, quantity):
    """Handles an incoming shipment (updates both item stock and global total)."""
    # 1a. Declare intent to modify the simple integer global variable
    global GLOBAL_TOTAL_STOCK
    
    if item_name in item_stock:
        # Note: Modifying the dictionary element does NOT require 'global'
        item_stock[item_name] += quantity
        # 1b. Update the global total
        GLOBAL_TOTAL_STOCK += quantity
        print(f"\n[IN] Processed {quantity} of {item_name}. Total stock updated.")
    else:
        print(f"\n[ERROR] Cannot process shipment: {item_name} not recognized.")

# 2. New function for outgoing shipments
def process_shipment_out(item_name, quantity):
    """Handles an outgoing shipment (updates both item stock and global total)."""
    # 2a. Declare intent to modify the simple integer global variable
    global GLOBAL_TOTAL_STOCK
    
    if item_name in item_stock:
        if item_stock[item_name] >= quantity:
            # Decrement local item stock
            item_stock[item_name] -= quantity
            # 2b. Decrement global total
            GLOBAL_TOTAL_STOCK -= quantity
            print(f"\n[OUT] Shipped {quantity} of {item_name}. Total stock updated.")
        else:
            print(f"\n[WARNING] Insufficient stock for {item_name}. Shipment failed.")
    else:
        print(f"\n[ERROR] Cannot process shipment: {item_name} not recognized.")


# 3. Test the full cycle
print("==================================================")
print(f"Starting Global Stock: {GLOBAL_TOTAL_STOCK}")
check_inventory("Monitor")

# Test 1: Incoming Shipment (1500 + 100 = 1600)
process_shipment_in("Monitor", 100)
check_inventory("Monitor") 

# Test 2: Outgoing Shipment (1600 - 50 = 1550)
process_shipment_out("Laptop", 50)
check_inventory("Laptop")

# Test 3: Attempting to ship too much (1550 remains unchanged)
process_shipment_out("Keyboard", 1000)
check_inventory("Keyboard")

print("\n==================================================")
print(f"Final Verified Global Stock: {GLOBAL_TOTAL_STOCK}")

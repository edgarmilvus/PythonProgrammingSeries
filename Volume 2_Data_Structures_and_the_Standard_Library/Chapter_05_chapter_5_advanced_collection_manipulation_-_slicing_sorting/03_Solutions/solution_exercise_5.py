
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

warehouse_a = ['Hammer', 'Wrench', 'Screwdriver', 'Drill']
warehouse_b = ['Saw', 'Level', 'Tape Measure', 'Gloves']
incoming_shipments = ['Bolts', 'Nails', 'Hammer']
outgoing_orders = ['Wrench', 'Level', 'Saw', 'Missing Item']

print("--- Exercise 5 Results (List Methods Mastery) ---")
print(f"Initial A: {warehouse_a}")
print(f"Initial B: {warehouse_b}")

# 1. Initial Transfer: Move the first two items from warehouse_b to warehouse_a
items_to_move = warehouse_b[:2]  # Use slicing to get the items
warehouse_a.extend(items_to_move) # Use extend() to add them efficiently

# Remove the items from warehouse_b using slicing assignment
warehouse_b = warehouse_b[2:]
print(f"\nAfter Transfer (A extended, B sliced):")
print(f"Warehouse A: {warehouse_a}")
print(f"Warehouse B: {warehouse_b}")

# 2. Incoming Stock: Add all incoming_shipments to warehouse_a
warehouse_a.extend(incoming_shipments)
print(f"\nAfter Incoming Shipments:")
print(f"Warehouse A: {warehouse_a}")

# 3. Outgoing Orders: Process removals using index() and pop() with error handling
print("\n--- Processing Outgoing Orders ---")
for item in outgoing_orders:
    removed = False
    
    # Priority 1: Check warehouse_a
    try:
        # Find the index of the item
        idx_a = warehouse_a.index(item)
        # Remove the item by index using pop()
        warehouse_a.pop(idx_a)
        print(f"Removed '{item}' from Warehouse A.")
        removed = True
    
    except ValueError:
        # Item not in A, proceed to check B
        pass
        
    if not removed:
        # Priority 2: Check warehouse_b
        try:
            idx_b = warehouse_b.index(item)
            warehouse_b.pop(idx_b)
            print(f"Removed '{item}' from Warehouse B.")
            removed = True
        
        except ValueError:
            # Item not found in either A or B
            print(f"STOCK OUT: '{item}' not found in inventory.")
            
# --- Final State Verification ---
print("\n--- Final Inventory State ---")
print(f"Warehouse A: {warehouse_a}")
print(f"Warehouse B: {warehouse_b}")

# Expected Final State:
# A should contain: ['Hammer', 'Screwdriver', 'Drill', 'Saw', 'Bolts', 'Nails', 'Hammer']
# B should contain: ['Tape Measure', 'Gloves']

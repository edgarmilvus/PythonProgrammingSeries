
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

INVENTORY_STOCK = [
    ["Laptop Pro", 15],
    ["Monitor X", 45],
    ["Keyboard Mech", 30],
    ["Mouse Wireless", 55]
]

# Define costs for calculation later
COSTS = {
    "Laptop Pro": 200,
    "Monitor X": 150,
    "Keyboard Mech": 50,
    "Server Blade 7": 500
}

print("--- Exercise 4: Enhancing the Inventory System ---")

# 1. Urgent Entry: Insert "Server Blade 7" at index 0
INVENTORY_STOCK.insert(0, ["Server Blade 7", 5])
print(f"After Insertion: {INVENTORY_STOCK}")

# 2. Discontinuation: Remove "Mouse Wireless"
# We use .remove() as the value is known and we don't need the returned item.
INVENTORY_STOCK.remove(["Mouse Wireless", 55]) 
print(f"After Removal: {INVENTORY_STOCK}")

# 3. Reordering: Sort alphabetically based on item name (index 0)
# We use a lambda function as the key to specify sorting by the first element of the inner list
INVENTORY_STOCK.sort(key=lambda item: item[0])
print(f"After Sorting: {INVENTORY_STOCK}")

# 4. Value Calculation (Comprehension): Stock Level * Cost
# item[1] is the stock level; item[0] is the name used for cost lookup
item_total_values = [
    item[1] * COSTS.get(item[0], 0) 
    for item in INVENTORY_STOCK
]

print(f"\nFinal Inventory State: {INVENTORY_STOCK}")
print(f"Calculated Total Values: {item_total_values}")

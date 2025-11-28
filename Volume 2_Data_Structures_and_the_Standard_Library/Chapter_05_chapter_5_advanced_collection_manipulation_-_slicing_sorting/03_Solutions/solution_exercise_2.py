
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

from collections import namedtuple

# 1. Data Structure Definition
Component = namedtuple('Component', ['sku', 'name', 'price', 'quantity'])

# 2. Sample Data Initialization
inventory = [
    Component('A001', 'Resistor', 50.00, 10),
    Component('B002', 'Capacitor', 12.50, 10),  # Prioritized due to lower price
    Component('C003', 'Transistor', 100.00, 5),
    Component('D004', 'Diode', 5.99, 20),      # Highest quantity
    Component('E005', 'Inductor', 75.00, 20),   # Secondary priority due to higher price
    Component('F006', 'Chip', 1.00, 5)
]

# 3. Sorting Logic
# Key tuple: (-c.quantity) achieves descending order for quantity.
# (c.price) achieves ascending order for price (the tie-breaker).
sorted_inventory = sorted(
    inventory,
    key=lambda c: (-c.quantity, c.price)
)

# --- Verification ---
print("\n--- Exercise 2 Results (Custom Sorting) ---")
print("SKU | QTY | PRICE")
print("-" * 20)

for item in sorted_inventory:
    print(f"{item.sku} | {item.quantity:3} | {item.price:6.2f}")

# Expected Order Verification:
# D004 (20, 5.99)
# E005 (20, 75.00)
# B002 (10, 12.50)
# A001 (10, 50.00)
# F006 (5, 1.00)
# C003 (5, 100.00)

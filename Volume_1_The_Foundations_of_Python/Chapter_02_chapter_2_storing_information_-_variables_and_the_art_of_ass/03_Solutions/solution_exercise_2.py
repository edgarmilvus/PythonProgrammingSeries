
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

# 1. Initial Setup
product_name = "Quantum Lever"
initial_stock = 150
unit_price_usd = 45.99

# 2. Calculate Initial Value
# Calculate the total value before any sales
total_inventory_value = initial_stock * unit_price_usd

print("--- Initial Inventory Report ---")
print(f"Product: {product_name}")
print(f"Initial Stock: {initial_stock}")
# Format the currency output to two decimal places
print(f"Initial Value: ${total_inventory_value:.2f}")

# 3. Simulation: Sale of 25 units
units_sold = 25

# 4. Reassignment of Stock
# Update the initial_stock variable by subtracting the units sold
initial_stock = initial_stock - units_sold

# 5. Recalculate Inventory Value
# total_inventory_value is reassigned (overwritten) based on the new stock level
total_inventory_value = initial_stock * unit_price_usd

# 6. Output Final State
print("\n--- Post-Sale Inventory Report ---")
print(f"Product: {product_name}")
print(f"Remaining Stock: {initial_stock}")
print(f"New Total Value: ${total_inventory_value:.2f}")

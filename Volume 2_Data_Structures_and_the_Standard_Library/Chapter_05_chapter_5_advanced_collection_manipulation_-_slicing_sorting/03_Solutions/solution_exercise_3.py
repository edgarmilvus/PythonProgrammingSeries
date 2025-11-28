
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

from collections import defaultdict

# Sample Input Data
transactions = [
    {'product_id': 'A45', 'revenue': 150.00},
    {'product_id': 'B90', 'revenue': 300.50},
    {'product_id': 'A45', 'revenue': 200.00},
    {'product_id': 'C11', 'revenue': 50.00},
    {'product_id': 'B90', 'revenue': 250.00},
    {'product_id': 'D01', 'revenue': 600.00},
    {'product_id': 'C11', 'revenue': 400.00},
]
MIN_REVENUE = 500.00

# 1. Aggregation using defaultdict
product_revenues = defaultdict(float)
for transaction in transactions:
    # Aggregation is simple and safe with defaultdict
    product_revenues[transaction['product_id']] += transaction['revenue']

# Convert to a standard dictionary for the cleanup phase
aggregated_data = dict(product_revenues)

# 2. Filtering and Removal
# Crucial step: To safely modify the dictionary during iteration, we must iterate
# over a copy of the keys (or items).
keys_to_remove = []
for product_id, total_revenue in aggregated_data.items():
    if total_revenue < MIN_REVENUE:
        keys_to_remove.append(product_id)

# Perform removal using the list of keys identified
for product_id in keys_to_remove:
    # Use the del keyword to remove the key-value pair
    del aggregated_data[product_id]

# --- Verification ---
print("\n--- Exercise 3 Results (Dynamic Aggregation and Cleanup) ---")
print(f"Minimum Revenue Threshold: ${MIN_REVENUE:.2f}")
print(f"Final Filtered Aggregation: {aggregated_data}")

# Expected: {'B90': 550.5, 'D01': 600.0}

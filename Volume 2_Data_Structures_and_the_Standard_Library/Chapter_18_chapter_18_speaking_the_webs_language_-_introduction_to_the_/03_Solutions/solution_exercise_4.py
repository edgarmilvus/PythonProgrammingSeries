
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

import json

# 1. Raw JSON data simulation (multi-line string)
raw_api_data = """
[
    {"id": 101, "name": "Wireless Mouse", "price": 45.99, "stock": true},
    {"id": 102, "name": "Mechanical Keyboard", "price": 125.00, "stock": true},
    {"id": 103, "name": "Webcam Pro", "price": 89.99, "stock": false},
    {"id": 104, "name": "USB Hub", "price": 19.50, "stock": true},
    {"id": 105, "name": "Monitor Stand", "price": 150.00, "stock": true}
]
"""

print("\n--- Exercise 4 Solution ---")

# 2. Deserialize the JSON string into a Python list of dictionaries
product_list = json.loads(raw_api_data)
print(f"Total products loaded: {len(product_list)}")

# 3 & 4. Filter products using a list comprehension
# Criteria: must be in stock (item['stock'] is True) AND price must be < 100.00
filtered_products = [
    product
    for product in product_list
    if product['stock'] is True and product['price'] < 100.00
]

# 5. Print results
print(f"\nTotal filtered products found: {len(filtered_products)}")
print("Affordable, in-stock products:")

# Extract and print names for clean output
for product in filtered_products:
    print(f"- {product['name']} (Price: ${product['price']:.2f})")

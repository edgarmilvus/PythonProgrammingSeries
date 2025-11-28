
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

# Source File: solution_exercise_6.py
# Description: Solution for Exercise 6
# ==========================================

inventory_data = [
    {"name": "Laptop", "price": 1200.00, "quantity": 15},
    {"name": "Monitor", "price": 300.00, "quantity": 35},
    {"name": "Keyboard", "price": 75.00, "quantity": 50},
    {"name": "Mouse", "price": 25.00, "quantity": 100},
]

def analyze_inventory(data):
    """
    Calculates inventory statistics (average price and total units) 
    and returns them as a structured dictionary.
    The function must NOT use print().
    """
    total_items = len(data)
    
    sum_prices = 0.0
    total_units = 0
    
    # Iterate through the data to aggregate metrics
    for item in data:
        sum_prices += item['price']
        total_units += item['quantity']
        
    # Calculate average price, safely handling empty inventory
    if total_items > 0:
        average_price = sum_prices / total_items
    else:
        average_price = 0.0
        
    # Return the results as a dictionary with descriptive keys
    return {
        'avg_price': average_price,
        'total_units': total_units
    }

# Execution: The caller receives the structured data
summary = analyze_inventory(inventory_data)

print("--- Inventory Summary Report ---")
# The caller is now responsible for displaying or using the data
print(f"Total Units in Stock: {summary['total_units']}")
print(f"Average Item Price: ${summary['avg_price']:.2f}")
print(f"Type of returned object: {type(summary)}")

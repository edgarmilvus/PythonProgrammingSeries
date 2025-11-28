
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

# Module-level constants defined using CAPITAL_SNAKE_CASE
SALES_TAX_RATE = 0.08
FREE_SHIPPING_THRESHOLD = 100.00
STANDARD_SHIPPING_FEE = 10.00


def calculate_total_cost(price_per_item, quantity):
    """
    Calculates the total cost of an order including tax and conditional shipping.
    """
    
    # Calculate the base cost before tax or shipping
    subtotal = price_per_item * quantity
    
    # Initialize shipping cost to the standard fee
    shipping_cost = STANDARD_SHIPPING_FEE
    
    # Conditional logic: Check if the subtotal qualifies for free shipping.
    if subtotal > FREE_SHIPPING_THRESHOLD:
        shipping_cost = 0.00
        
    # Calculate the subtotal including sales tax
    taxed_subtotal = subtotal * (1 + SALES_TAX_RATE)
    
    # Final calculation: taxed subtotal plus the applicable shipping cost
    total_cost = taxed_subtotal + shipping_cost
    
    return total_cost

# Example Usage:
# cost_1 = calculate_total_cost(price_per_item=10, quantity=5)  # Subtotal 50, shipping $10
# cost_2 = calculate_total_cost(price_per_item=60, quantity=2)  # Subtotal 120, shipping $0

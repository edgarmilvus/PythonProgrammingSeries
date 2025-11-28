
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

# 1. Define Core Data (Strings simulating raw input)
product_name_str = "Elite Widget X1"
quantity_str = "150"
unit_price_str = "24.99"
discount_rate_str = "0.15"

# 2. Mandatory Casting: Converting strings to appropriate numerical types
quantity_int = int(quantity_str)
price_float = float(unit_price_str)
discount_float = float(discount_rate_str)

# 3. Calculation
# Calculate the total value before discount
subtotal = quantity_int * price_float

# Calculate the monetary value of the discount
discount_amount = subtotal * discount_float

# Calculate the final cost after applying the discount
final_cost = subtotal - discount_amount

# Prepare discount rate for percentage display (e.g., 0.15 -> 15.0)
discount_percentage_display = discount_float * 100

# Round the final cost to two decimal places for financial output
final_cost_rounded = round(final_cost, 2)

# 4. Formatted Output
print("\n--- Inventory Log Update ---")
print(f"Product: {product_name_str}")
print(f"Quantity: {quantity_int} @ ${price_float} each")
# Displaying the percentage rounded to one decimal place
print(f"Discount Applied: {round(discount_percentage_display, 1)}%")
# Final output using the rounded financial value
print(f"Final Cost: ${final_cost_rounded}")

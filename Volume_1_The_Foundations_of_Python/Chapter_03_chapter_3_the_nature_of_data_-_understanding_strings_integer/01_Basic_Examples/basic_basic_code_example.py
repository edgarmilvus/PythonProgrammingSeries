
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

# ----------------------------------------------------------------------
# Section 1: Variable Declaration and Data Type Assignment
# ----------------------------------------------------------------------

# String (str): Used for storing text data. Must be enclosed in quotes.
item_name = "Advanced Python Textbook"

# Integer (int): Used for whole numbers where precision is not needed.
quantity = 2

# Float (float): Used for numbers requiring decimal precision (currency, rates).
unit_price = 49.99

# Float (float): The sales tax rate (7.5% represented as a decimal).
tax_rate = 0.075

# ----------------------------------------------------------------------
# Section 2: Arithmetic Operations and Implicit Type Conversion
# ----------------------------------------------------------------------

# Calculate the subtotal (unit_price * quantity).
# Python automatically promotes the integer 'quantity' to a float for this calculation.
subtotal = unit_price * quantity

# Calculate the tax amount based on the subtotal.
tax_amount = subtotal * tax_rate

# Calculate the final total cost.
total_cost = subtotal + tax_amount

# ----------------------------------------------------------------------
# Section 3: Output and Type Verification
# ----------------------------------------------------------------------

print("--- Purchase Summary ---")
print("Item:", item_name)
print(f"Quantity: {quantity}")
print(f"Unit Price: ${unit_price}")
print("-" * 30)
print(f"Subtotal: ${subtotal:.2f}") # Formatted to two decimal places
print(f"Total Tax: ${tax_amount:.2f}")
print(f"Final Cost: ${total_cost:.2f}")
print("-" * 30)

# Use the built-in type() function to inspect the resulting data types
print("\nVerification of Data Types:")
print(f"Type of item_name is: {type(item_name)}")
print(f"Type of quantity is: {type(quantity)}")
print(f"Type of subtotal is: {type(subtotal)}")
print(f"Type of total_cost is: {type(total_cost)}")

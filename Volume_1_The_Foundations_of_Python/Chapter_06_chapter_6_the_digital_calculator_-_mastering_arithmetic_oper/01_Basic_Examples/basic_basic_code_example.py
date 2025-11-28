
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

# --- 1. Initialization: Defining the base costs ---
# We use floating-point numbers (floats) because prices often involve cents.
item_price_main = 45.99  # Price of the main dish
item_price_side = 12.50  # Price of the side item
tax_rate = 0.08          # 8% tax rate (represented as a decimal)
number_of_diners = 3     # The group size for splitting the bill

# --- 2. Calculation Block A: Addition and Multiplication ---
# Calculate the initial cost before tax.
subtotal = item_price_main + item_price_side

# Calculate the tax amount using multiplication.
tax_amount = subtotal * tax_rate

# Calculate the final total using addition.
grand_total = subtotal + tax_amount

# --- 3. Calculation Block B: Subtraction (Change Due) ---
# Assume we pay with a $100 bill.
payment_amount = 100.00
change_due = payment_amount - grand_total

# --- 4. Specialized Division Operations (Splitting the Bill) ---
# Goal: Find the cost per person and the remainder.

# Standard Division (/) - Provides the exact, fractional cost per person.
cost_per_person_exact = grand_total / number_of_diners

# Floor Division (//) - Provides the largest whole dollar amount everyone must pay.
# This truncates the fractional part.
cost_per_person_floor = grand_total // number_of_diners

# Modulus Operator (%) - Finds the remainder left over after the floor division.
# This represents the small amount still owed after everyone pays the floor amount.
remainder_cents = grand_total % number_of_diners

# --- 5. Output: Displaying the results ---
print("--- Detailed Dinner Bill Breakdown ---")
print(f"1. Subtotal (Main + Side): ${item_price_main} + ${item_price_side} = ${subtotal:.2f}")
print(f"2. Tax Amount (8%): ${tax_amount:.2f}")
print(f"3. Grand Total: ${grand_total:.2f}")
print("-" * 40)
print(f"Payment Received: ${payment_amount:.2f}")
print(f"Change Due: ${change_due:.2f}")
print("-" * 40)
print(f"Splitting the Bill among {number_of_diners} people:")
print(f"A. Exact Cost per Person (/): ${cost_per_person_exact:.2f}")
print(f"B. Floor Cost per Person (//): ${cost_per_person_floor:.2f}")
print(f"C. Remaining Cents to Cover (%): ${remainder_cents:.2f}")

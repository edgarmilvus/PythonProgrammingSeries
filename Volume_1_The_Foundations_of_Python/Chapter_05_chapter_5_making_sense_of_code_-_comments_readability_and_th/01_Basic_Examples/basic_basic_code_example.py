
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

# File: pricing_calculator.py
"""
Module Docstring: Calculates the final price of a product after applying 
a fixed discount and a standard sales tax rate.
This script demonstrates proper commenting, section separation, and 
variable naming conventions for clarity.
"""

# ----------------------------------------------------
# --- 1. Configuration Variables (Inputs) ---
# ----------------------------------------------------

# The initial price of the item before any adjustments (e.g., a video game).
base_price = 49.99

# CONSTANT: The percentage discount offered (expressed as a decimal, 
# e.g., 0.15 represents 15%). Named in ALL CAPS to signify it should not change.
DISCOUNT_RATE = 0.15 

# CONSTANT: The standard sales tax rate for the region (expressed as a decimal).
SALES_TAX_RATE = 0.075 

# ----------------------------------------------------
# --- 2. Core Calculation Logic ---
# ----------------------------------------------------

# Step 1: Calculate the dollar amount saved due to the discount.
discount_amount = base_price * DISCOUNT_RATE

# Step 2: Calculate the price after the discount is applied.
# This is the price that tax will be applied to.
price_after_discount = base_price - discount_amount

# Step 3: Calculate the tax amount based on the discounted price.
tax_amount = price_after_discount * SALES_TAX_RATE

# Step 4: Calculate the final price the customer pays.
final_price = price_after_discount + tax_amount

# ----------------------------------------------------
# --- 3. Output and Presentation ---
# ----------------------------------------------------

# Display the results clearly to the user using f-strings for formatting.
print("--- Pricing Summary ---")
print(f"Original Price: ${base_price}")
print(f"Discount Applied: {DISCOUNT_RATE * 100}%")

# We use the round() function to ensure currency displays with exactly two decimal places.
print(f"Price After Discount: ${round(price_after_discount, 2)}")
print(f"Total Tax ({SALES_TAX_RATE * 100}%): ${round(tax_amount, 2)}")
print("-----------------------")
print(f"FINAL COST: ${round(final_price, 2)}")


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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

# Constants and Configuration (Floats and Strings)
STORE_NAME = "The Pythonic Emporium"
TAX_RATE_PERCENT = 8.75  # Defined as a float for high-precision calculation
MAX_ITEM_NAME_LENGTH = 20 # Used for receipt alignment
SEPARATOR_LINE = "----------------------------------------"

# --- Input Data Simulation: Data often arrives as strings or raw integers ---
# Item 1: High-value, single item
item_1_name = "Advanced Logic Board"
item_1_quantity = 1        # Integer (whole number count)
item_1_unit_price_raw = "199.99" # Price input simulated as a string

# Item 2: Low-value, bulk item
item_2_name = "Standard Cable Set (5m)"
item_2_quantity = 5
item_2_unit_price_raw = "12.50"

# --- Step 1: Data Preparation and Casting ---

# Convert raw string prices to precise float types for arithmetic
price_1 = float(item_1_unit_price_raw)
price_2 = float(item_2_unit_price_raw)

# Calculate the tax multiplier (Float division ensures precision)
tax_multiplier = TAX_RATE_PERCENT / 100.0

# --- Step 2: Core Calculations (Integers and Floats) ---

# Calculate item subtotals (Float * Integer = Float)
subtotal_1 = item_1_quantity * price_1
subtotal_2 = item_2_quantity * price_2

# Calculate the overall transaction subtotal
transaction_subtotal = subtotal_1 + subtotal_2

# Calculate the tax amount
tax_amount = transaction_subtotal * tax_multiplier

# Calculate the final grand total
grand_total = transaction_subtotal + tax_amount

# --- Step 3: Formatting and String Manipulation ---

# 3a. Truncate and pad item names for alignment using string slicing and concatenation

# Item 1 formatting: Truncate the name if it exceeds the max length (slicing)
name_1_truncated = item_1_name[0:MAX_ITEM_NAME_LENGTH]
# Calculate necessary padding spaces
padding_1 = MAX_ITEM_NAME_LENGTH - len(name_1_truncated)
# Apply padding using string multiplication and concatenation
padded_name_1 = name_1_truncated + (" " * padding_1)

# Item 2 formatting: Apply the same logic
name_2_truncated = item_2_name[0:MAX_ITEM_NAME_LENGTH]
padding_2 = MAX_ITEM_NAME_LENGTH - len(name_2_truncated)
padded_name_2 = name_2_truncated + (" " * padding_2)

# 3b. Format calculated numerical totals back into display strings (Casting and Slicing)
# Note: This technique simulates rounding to two decimals using only casting and slicing.

# Convert transaction_subtotal to string
subtotal_str_raw = str(transaction_subtotal)
# Find the index of the decimal point
decimal_index_sub = subtotal_str_raw.find('.')
# Slice the string to include the index and the two characters following it (+3)
formatted_subtotal = subtotal_str_raw[0:decimal_index_sub + 3]

# Convert tax_amount to string
tax_str_raw = str(tax_amount)
decimal_index_tax = tax_str_raw.find('.')
formatted_tax = tax_str_raw[0:decimal_index_tax + 3]

# Convert grand_total to string
total_str_raw = str(grand_total)
decimal_index_total = total_str_raw.find('.')
formatted_total = total_str_raw[0:decimal_index_total + 3]

# 3c. Construct the final receipt output string using concatenation and alignment methods

# Header Construction: Center the store name based on the separator length
header = STORE_NAME.center(len(SEPARATOR_LINE)) + "\n"
header += "Transaction Summary\n"
header += SEPARATOR_LINE + "\n"

# Item Line 1 Construction: Concatenate padded name, quantity (cast to string, left justified), and totals
line_1 = padded_name_1 + " | " + str(item_1_quantity).ljust(3) + " | $"
line_1 += str(price_1).ljust(7) + " | $" + str(subtotal_1) + "\n"

# Item Line 2 Construction
line_2 = padded_name_2 + " | " + str(item_2_quantity).ljust(3) + " | $"
line_2 += str(price_2).ljust(7) + " | $" + str(subtotal_2) + "\n"

# Footer Construction (Using formatted strings and right justification)
footer = SEPARATOR_LINE + "\n"
footer += "Subtotal: ".rjust(30) + "$" + formatted_subtotal + "\n"
# Include the tax rate percentage in the display
footer += "Tax (" + str(TAX_RATE_PERCENT) + "%): ".rjust(30) + "$" + formatted_tax + "\n"
footer += SEPARATOR_LINE + "\n"
footer += "GRAND TOTAL: ".rjust(30) + "$" + formatted_total + "\n"

# Final Output display
print(header + line_1 + line_2 + footer)


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
# Section 1: Variable Definition and Assignment
# ----------------------------------------------------------------------

# 1. Assigning a user's identity (a sequence of characters, or a String)
# We use 'snake_case' for variable names (all lowercase, words separated by underscores).
user_name = "Elara Vance"

# 2. Assigning a numerical count (a whole number, or an Integer)
# This variable tracks the quantity of items Elara has selected.
item_quantity = 5

# 3. Assigning a precise monetary value (a number with a decimal point, or a Float)
# This represents the unit price of the item.
unit_price = 45.50

# ----------------------------------------------------------------------
# Section 2: Displaying Stored Information
# ----------------------------------------------------------------------

# Display a header for clarity
print("--- User Session Data Log ---")

# Retrieve and print the stored user name
# The print function can display text literals and the values held by variables.
print("Registered User:", user_name)

# Retrieve and print the stored item quantity
print("Current Cart Quantity:", item_quantity)

# Retrieve and print the stored unit price
print("Price Per Unit:", unit_price)

# Calculate and display the subtotal directly using the stored variables
# Note: Python retrieves the values stored in the variables for this calculation.
subtotal = item_quantity * unit_price
print("Calculated Subtotal:", subtotal)

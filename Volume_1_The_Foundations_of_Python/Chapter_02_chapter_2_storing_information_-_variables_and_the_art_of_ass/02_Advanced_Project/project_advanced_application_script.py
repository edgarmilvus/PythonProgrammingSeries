
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

# E-commerce Inventory and Transaction Processor
# This script demonstrates variable assignment, basic arithmetic operations,
# and variable reassignment to track inventory and calculate an order total.

# --- 1. System Constants and Initial Inventory Setup ---
# These variables hold the foundational data for the product being sold.
# Note the use of snake_case for PEP 8 compliance.

product_sku = "PROD-A47B"       # String: Unique product identifier
product_description = "High-Performance Mechanical Keyboard"  # String: Descriptive name

# Numerical variables representing initial state and fixed rates
initial_stock_level = 150       # Integer: How many units are currently available
unit_price_usd = 129.99         # Float: The base price per unit, requiring decimal precision
tax_rate = 0.075                # Float: 7.5% sales tax (stored as a decimal for calculation)

# Variables purely for clean output formatting
output_separator = "-" * 60
warning_separator = "=" * 60

print("--- INITIAL INVENTORY STATE ---")
# Using f-strings to embed variable values into descriptive output strings
print(f"Product: {product_description} (SKU: {product_sku})")
print(f"Initial Stock: {initial_stock_level} units")
# Using format specifier :.2f to ensure the price displays with two decimal places
print(f"Price per unit: ${unit_price_usd:.2f}")
print(output_separator)

# --- 2. Processing a New Customer Order ---
# Variables are assigned values specific to this transaction.

customer_name = "Eleanor Vance" # String variable for the customer's identity
order_id = 900123               # Integer variable for tracking the order
order_quantity = 5              # Integer: The number of units purchased

print(f"Processing Order #{order_id} for {customer_name}...")
print(f"Quantity Requested: {order_quantity}")

# --- 3. Financial Calculations: Assignment of Calculated Values ---
# New variables are created to store the results of arithmetic operations.
# This demonstrates calculating new values and assigning them to descriptive variable names.

# Calculate the total cost before tax (Float = Float * Integer)
subtotal_cost = unit_price_usd * order_quantity

# Calculate the specific tax amount (Float = Float * Float)
tax_amount = subtotal_cost * tax_rate

# Calculate the final amount due (Float = Float + Float)
grand_total = subtotal_cost + tax_amount

# Variables for formatting currency output and displaying the rate
currency_symbol = "$"
tax_percentage_display = tax_rate * 100 # Convert decimal rate to percentage for display

print(output_separator)
print("--- ORDER FINANCIAL SUMMARY ---")
print(f"Subtotal: {currency_symbol}{subtotal_cost:.2f}")
print(f"Tax Rate: {tax_percentage_display:.1f}%")
print(f"Tax Amount: {currency_symbol}{tax_amount:.2f}")
print(f"GRAND TOTAL DUE: {currency_symbol}{grand_total:.2f}")
print(output_separator)

# --- 4. Inventory Management: Variable Assignment and Boolean Logic ---
# The result of the subtraction operation is assigned to a new variable.

remaining_stock_level = initial_stock_level - order_quantity

# A check is performed to see if the stock dropped below a threshold (10 units).
# The result of this comparison is stored in a boolean variable (True/False).
is_low_stock = remaining_stock_level < 10

# --- 5. Final Report and Conditional Status Update ---
print("--- INVENTORY UPDATE STATUS ---")
print(f"Stock Before Transaction: {initial_stock_level}")
print(f"Units Sold: {order_quantity}")
print(f"Remaining Stock: {remaining_stock_level}")

# Conditional output based on the boolean variable's assigned value
if is_low_stock:
    warning_message = "CRITICAL: Stock is dangerously low! Reorder immediately."
    print(warning_separator)
    print(warning_message)
    print(warning_separator)
else:
    status_message = "Inventory level is healthy."
    print(f"Status: {status_message}")

# --- 6. Demonstration of Variable Reassignment (Refund Scenario) ---
# The 'remaining_stock_level' variable is updated (reassigned) to reflect a return.
print(output_separator)
print("--- DEMO: Variable Reassignment (Refund Scenario) ---")

# A new variable stores the amount being returned
returned_units = 2

# Reassign the 'remaining_stock_level' variable by increasing its value.
# The previous value (145) is overwritten in memory by the new value (147).
remaining_stock_level = remaining_stock_level + returned_units

# Reassign the 'is_low_stock' variable to reflect the new state, even though
# in this case, the result (False) remains the same.
is_low_stock = remaining_stock_level < 10

print(f"Units Returned: {returned_units}")
print(f"New Stock Level After Refund: {remaining_stock_level}")
print(f"Is Stock Low Now? {is_low_stock}")

# End of script marker
print(output_separator)

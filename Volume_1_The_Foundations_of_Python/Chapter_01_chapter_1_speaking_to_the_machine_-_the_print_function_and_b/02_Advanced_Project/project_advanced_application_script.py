
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

# ==============================================================================
# SCRIPT TITLE: Static Inventory and Sales Receipt Generator
# CONCEPTS USED: print() function, String literals, Integer and Float literals, 
#                Basic Arithmetic Operators (+, -, *, /).
#
# OBJECTIVE: Calculate and display a formatted receipt using only sequential 
#            execution and hardcoded values.
# ==============================================================================

# --- 1. Receipt Header Output ---
# Displaying the top boundary of the receipt using print()
print("===================================================")
# Centering the store name
print("       THE PYTHON FOUNDATION STORE")
# Adding a descriptive subtitle
print("           Static Sales Receipt")
print("===================================================")
# Using print() without arguments to create a blank line for visual spacing
print() 

# --- 2. Defining Static Inventory and Sales Data ---
# Since variables are not yet covered, we define the data conceptually 
# and use the raw values repeatedly in the calculation steps below.

# Item 1: Python Handbook
# Price: 59.99, Quantity: 2
ITEM_1_NAME = "Python Foundation Handbook"
ITEM_1_PRICE = 59.99
ITEM_1_QTY = 2

# Item 2: Advanced Data Structures Poster
# Price: 15.50, Quantity: 1
ITEM_2_NAME = "Data Structures Poster"
ITEM_2_PRICE = 15.50
ITEM_2_QTY = 1

# Item 3: Debugging Rubber Duck
# Price: 4.00, Quantity: 5
ITEM_3_NAME = "Debugging Rubber Duck"
ITEM_3_PRICE = 4.00
ITEM_3_QTY = 5

# Define the Sales Tax Rate (8.5% or 0.085)
SALES_TAX_RATE = 0.085

# --- 3. Printing the Table Headers ---
# Manually aligning the column headers using spaces
print("ITEM DESCRIPTION                      QTY      UNIT PRICE      LINE TOTAL")
# Creating a separator line
print("-----------------------------------------------------------------------")

# --- 4. Processing and Displaying Line Item 1 ---
# Calculation: 59.99 * 2 = 119.98
# We perform the calculation directly inside the print statement (or conceptually 
# before printing) and convert the results to strings for concatenation.
ITEM_1_TOTAL = 59.99 * 2
print(ITEM_1_NAME + "               " + str(ITEM_1_QTY) + "         " + str(ITEM_1_PRICE) + "          " + str(ITEM_1_TOTAL))

# --- 5. Processing and Displaying Line Item 2 ---
# Calculation: 15.50 * 1 = 15.50
ITEM_2_TOTAL = 15.50 * 1
# Note the manual spacing adjustments needed for alignment due to different string lengths
print(ITEM_2_NAME + "                  " + str(ITEM_2_QTY) + "         " + str(ITEM_2_PRICE) + "           " + str(ITEM_2_TOTAL))

# --- 6. Processing and Displaying Line Item 3 ---
# Calculation: 4.00 * 5 = 20.00
ITEM_3_TOTAL = 4.00 * 5
print(ITEM_3_NAME + "             " + str(ITEM_3_QTY) + "         " + str(ITEM_3_PRICE) + "            " + str(ITEM_3_TOTAL))

# Adding a separator before the summary
print("-----------------------------------------------------------------------")
print() # Spacing

# --- 7. Calculating and Displaying the Subtotal ---
# Subtotal = 119.98 (Item 1) + 15.50 (Item 2) + 20.00 (Item 3) = 155.48
SUBTOTAL_CALCULATION = 119.98 + 15.50 + 20.00
# Using extreme manual spacing to push the numerical result to the right
print("Subtotal before Tax:                                        " + str(SUBTOTAL_CALCULATION))

# --- 8. Calculating and Displaying Sales Tax ---
# Tax Amount = 155.48 * 0.085 = 13.2158
TAX_CALCULATION = 155.48 * 0.085
print("Sales Tax (8.5%):                                            " + str(TAX_CALCULATION))

# --- 9. Calculating and Displaying the Grand Total ---
# Grand Total = 155.48 + 13.2158 = 168.6958
GRAND_TOTAL_CALCULATION = 155.48 + 13.2158
print("===================================================")
print("GRAND TOTAL DUE:                                            " + str(GRAND_TOTAL_CALCULATION))
print("===================================================")

# --- 10. Final Footer and Verification ---
print()
print("Thank you for shopping at The Python Foundation Store!")
print("Receipt ID: 1001A")
print("Date: 2024-01-15")
print()
print("Verification Note: This sequential execution confirms that Python")
print("processes arithmetic operations immediately when encountered, and")
print("the output function successfully combines text (strings) and numerical")
print("results (floats) using the string concatenation operator (+).")
print("---------------------------------------------------")

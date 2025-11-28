
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

# 1. Variable Declaration: Defining income (int) and expenses (floats)
monthly_income = 5500
rent_cost = 1250.00
grocery_expense = 450.75
utility_cost = 185.33

# 2. Calculation: Total expenses and net savings
# The result of the sum will be a float due to the mixed types.
total_expenses = rent_cost + grocery_expense + utility_cost

# Net savings calculation (int - float results in a float)
net_savings = monthly_income - total_expenses

# 3. Percentage Calculation: Ensuring float division is used
# Python 3 automatically handles this division as a float result.
savings_percentage = (net_savings / monthly_income) * 100

# 4. Output and Formatting
print("--- Financial Summary ---")
print(f"Total Monthly Income: {monthly_income}")
# Rounding total expenses for cleaner display
print(f"Total Expenses: {round(total_expenses, 2)}")

# Print net_savings rounded to exactly two decimal places
net_savings_rounded = round(net_savings, 2)
print(f"Net Savings: {net_savings_rounded}")

# Print savings_percentage rounded to one decimal place, followed by '%'
savings_percentage_rounded = round(savings_percentage, 1)
# Casting the numerical result into a string to concatenate with the '%' symbol
print(f"Savings Percentage: {savings_percentage_rounded}%")

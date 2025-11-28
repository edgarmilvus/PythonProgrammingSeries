
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

# 1. Define the required variables
principal = 5000.00
annual_rate = 0.045  # 4.5% expressed as a decimal
time_in_years = 10

# 2. Calculate the Future Value (FV)
# Formula: FV = P * (1 + R)**T
# Parentheses ensure (1 + Rate) is calculated before exponentiation.
future_value = principal * ((1 + annual_rate) ** time_in_years)

# 3. Calculate the total interest earned
total_interest_earned = future_value - principal

# 4. Print the results, rounded to two decimal places for currency
print(f"--- Compound Interest Simulation ---")
print(f"Initial Principal: ${principal:.2f}")
print(f"Annual Rate: {annual_rate * 100}% over {time_in_years} years")
print(f"Future Value (rounded): ${round(future_value, 2)}")
print(f"Total Interest Earned (rounded): ${round(total_interest_earned, 2)}")

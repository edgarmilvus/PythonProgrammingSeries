
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

# Data for Exercise 9.3
report_title = "Q3 FINANCIAL SUMMARY"
project_name = "Project Alpha"
revenue = 123456.789
expenses = 98765.4
profit_margin = 0.2345

print("\n" + "=" * 50)

# 1. Centered Title (50 width, padded by *)
# :*^50 means pad with '*', center (^), total width 50
print(f"{report_title:*^50}")

print("=" * 50)

# 2. Left-aligned Project Name
# :<41 means left align (<), total width 41. (50 total width - 9 chars for "Project: " = 41)
print(f"Project: {project_name:<41}")

# 3. Revenue and Expenses (Currency Formatting)
print("-" * 50)
# :>,15.2f means right align (>), width 15, comma separator (,), 2 decimal float (.2f)
print(f"Revenue:   ${revenue:>,15.2f}")
print(f"Expenses:  ${expenses:>,15.2f}")
print("-" * 50)

# 4. Profit Margin (Percentage Formatting)
# :>10.2% means right align (>), width 10, 2 decimal percentage (.2%)
print(f"Profit Margin: {profit_margin:>10.2%}")
print("=" * 50)

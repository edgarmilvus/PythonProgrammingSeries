
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

# Define the required variables
demand = 150
lead_time = 25
carrying_cost = 18

# Calculate the Adjustment Factor using a single assignment statement.
# Numerator: (demand * 2) + lead_time
# Denominator: (carrying_cost - 5) * 3
# Final Expression: (Numerator / Denominator) ** 2
adjustment_factor = (((demand * 2) + lead_time) / ((carrying_cost - 5) * 3)) ** 2

# Print the final result
print(f"Demand: {demand}, Lead Time: {lead_time}, Carrying Cost: {carrying_cost}")
print(f"The calculated Adjustment Factor is: {adjustment_factor}")

# Calculation Breakdown:
# Numerator: (150 * 2) + 25 = 300 + 25 = 325
# Denominator: (18 - 5) * 3 = 13 * 3 = 39
# Division: 325 / 39 ≈ 8.33333
# Result: 8.33333 ** 2 ≈ 69.44444444444444

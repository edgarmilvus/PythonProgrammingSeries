
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

print("\n--- Exercise 2: Transaction Log Sanitizer ---")

# Requirement 1: Sample transactions
transactions = [150.00, 20.50, -10.00, 0.00, 500.00, 75.25, -5.00, 120.00]
# Requirement 2: Initialize accumulator
total_revenue = 0.0

print(f"Processing Transactions: {transactions}")

# Requirement 3: Iterate through the transaction list
for amount in transactions:
    
    # Requirement 4: If the transaction is zero or negative, skip it
    if amount <= 0:
        print(f"-> Skipping invalid entry: {amount}")
        continue # Immediately jumps to the next iteration
        
    # Requirement 5: Accumulate only positive amounts
    total_revenue += amount
    print(f"-> Adding valid revenue: {amount}")

# Requirement 6: Print result
print(f"\nFinal Calculated Total Revenue: ${total_revenue:.2f}")

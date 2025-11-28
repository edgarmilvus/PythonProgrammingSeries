
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

from collections import defaultdict

# Raw Data Example
transactions = [
    (101, 55.50, '2023-10-01', 'Groceries'),
    (102, 1200.00, '2023-10-05', 'Rent'),
    (103, 15.25, '2023-10-02', 'Groceries'),
    (104, 30.00, '2023-10-08', 'Entertainment'),
    (105, 200.00, '2023-10-10', 'Utilities'),
    (106, 45.00, '2023-11-01', 'Groceries'),
    (107, 5000.00, '2023-11-15', 'Salary'),
]

# 1. Define the default factory function using lambda
# This function returns the desired initial dictionary structure for a new category.
category_factory = lambda: {'total': 0.0, 'transactions': []}

# 2. Initialize the defaultdict
grouped_transactions = defaultdict(category_factory)

# 3. Processing Loop
print("--- Exercise 1: Financial Transaction Grouping (defaultdict) ---")
for _, amount, _, category in transactions:
    # Accessing the key automatically creates the {'total': 0.0, 'transactions': []} structure
    # if the category is encountered for the first time.
    data = grouped_transactions[category]

    # Update the total expenditure
    data['total'] += amount

    # Append the individual transaction amount
    data['transactions'].append(amount)

# 4. Final Output
for category, data in grouped_transactions.items():
    print(f"\nCategory: {category}")
    print(f"  Total Spent: ${data['total']:.2f}")
    print(f"  Individual Amounts: {data['transactions']}")

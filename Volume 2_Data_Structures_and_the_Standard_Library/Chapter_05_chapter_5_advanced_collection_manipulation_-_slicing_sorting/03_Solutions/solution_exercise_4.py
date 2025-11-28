
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

from datetime import datetime

# Sample Input Data
raw_transactions = [
    {'date': '2023-11-20', 'value': 1500.00, 'status': 'COMPLETE'},
    {'date': '2023-10-01', 'value': 50.00, 'status': 'PENDING'},
    {'date': '2023-11-25', 'value': 999.99, 'status': 'COMPLETE'},
    {'date': '2023-10-15', 'value': 1000.00, 'status': 'COMPLETE'},
    {'date': '2023-12-05', 'value': 200.00, 'status': 'FAILED'},
    {'date': '2023-10-05', 'value': 1200.00, 'status': 'COMPLETE'},
    {'date': '2023-12-10', 'value': 100.00, 'status': 'COMPLETE'},
    {'date': '2023-12-15', 'value': 2500.00, 'status': 'COMPLETE'},
]
DATE_FORMAT = "%Y-%m-%d"
HIGH_VALUE_THRESHOLD = 1000.00

# 1. Data Transformation: Convert date strings to datetime objects
# Use a list comprehension to create a new list with the updated date type.
processed_transactions = [
    {
        'date': datetime.strptime(t['date'], DATE_FORMAT),
        'value': t['value'],
        'status': t['status']
    }
    for t in raw_transactions
]

# 2. Chronological Sort: Sort based on the datetime object
# datetime objects are inherently sortable, making the key straightforward.
sorted_transactions = sorted(
    processed_transactions,
    key=lambda t: t['date']
)

# 3. Partitioning: Separate into high and standard value lists
high_value_transactions = []
standard_transactions = []

for t in sorted_transactions:
    if t['value'] >= HIGH_VALUE_THRESHOLD:
        high_value_transactions.append(t)
    else:
        standard_transactions.append(t)

# --- Verification ---
print("\n--- Exercise 4 Results (Advanced Sorting and Partitioning) ---")

print("\n--- High Value Transactions (>= $1000.00) ---")
print(f"Total High Value: {len(high_value_transactions)}")
print("First 3 (Chronological):")
for t in high_value_transactions[:3]:
    print(f"  {t['date'].strftime(DATE_FORMAT)} | ${t['value']:.2f}")

print("\n--- Standard Transactions (< $1000.00) ---")
print(f"Total Standard: {len(standard_transactions)}")
print("First 3 (Chronological):")
for t in standard_transactions[:3]:
    print(f"  {t['date'].strftime(DATE_FORMAT)} | ${t['value']:.2f}")

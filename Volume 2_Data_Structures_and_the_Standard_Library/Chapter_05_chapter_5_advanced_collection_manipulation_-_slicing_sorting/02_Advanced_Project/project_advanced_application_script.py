
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

import operator
from collections import namedtuple
from datetime import datetime

# 1. Setup Data Structure: Define a structure for transaction records
# namedtuple provides readable, immutable records, ideal for raw data input.
Transaction = namedtuple('Transaction', ['date_str', 'product_id', 'category', 'amount'])

# 2. Sample Data: A list of transactions (simulating database fetch)
RAW_DATA = [
    Transaction('2023-11-01', 'P101', 'Electronics', 450.00),
    Transaction('2023-11-05', 'P205', 'Books', 19.99),
    Transaction('2023-11-03', 'P102', 'Electronics', 1200.50),
    Transaction('2023-11-01', 'P301', 'Apparel', 75.00),
    Transaction('2023-11-07', 'P404', 'Furniture', 350.00),
    Transaction('2023-11-02', 'P205', 'Books', 19.99),
    Transaction('2023-11-06', 'P101', 'Electronics', 89.99),
    Transaction('2023-11-08', 'P305', 'Apparel', 150.00),
    Transaction('2023-11-08', 'P501', 'Services', 500.00),
    Transaction('2023-11-04', 'P401', 'Furniture', 210.00),
    Transaction('2023-11-09', 'P105', 'Electronics', 60.00),
    Transaction('2023-11-09', 'P201', 'Books', 45.00),
    Transaction('2023-11-10', 'P600', 'Tools', 30.00),
    Transaction('2023-11-10', 'P110', 'Electronics', 99.99),
    Transaction('2023-11-11', 'P700', 'Services', 1500.00),
]

# --- Core Processing Functions ---

def process_data(data_list):
    """
    Cleans date strings into datetime objects and sorts the entire dataset.
    """
    processed_records = []
    
    # 3. Data Preparation: Convert date strings to comparable datetime objects
    for record in data_list:
        try:
            # Use strptime to parse the date string
            dt_obj = datetime.strptime(record.date_str, '%Y-%m-%d')
            
            # Create a standard tuple (datetime_obj, product_id, category, amount)
            # We use tuple concatenation (record[1:]) to efficiently rebuild the structure
            new_record = (dt_obj,) + record[1:]
            processed_records.append(new_record)
        except ValueError:
            # Skip records with malformed dates
            print(f"Skipping invalid date record: {record.date_str}")
            continue
    
    # 4. Advanced Sorting: Sort by multiple criteria using operator.itemgetter
    # Sort primarily by date (index 0), secondarily by amount (index 3).
    # reverse=True ensures the newest (largest) dates appear first.
    sorted_by_date = sorted(
        processed_records, 
        key=operator.itemgetter(0, 3), 
        reverse=True
    )

    return sorted_by_date

def analyze_transactions(sorted_data):
    """
    Performs slicing operations and aggregates totals using dictionary methods.
    """
    
    # 5. Top Recent Transactions (Advanced Slicing)
    print("\n--- Top 5 Most Recent Transactions (Slicing [0:5]) ---")
    # Since the list is sorted descending by date, the first 5 elements are the most recent.
    # We use the simplified slice notation `[:5]`
    top_recent = sorted_data[:5]
    
    for i, record in enumerate(top_recent):
        # record[0] is the datetime object, record[2] is category, record[3] is amount
        print(f"  {i+1}. Date: {record[0].strftime('%Y-%m-%d')} | Category: {record[2]:<12} | Amount: ${record[3]:.2f}")

    # 6. Aggregation using Dictionary Methods
    category_totals = {}
    category_counts = {}

    for record in sorted_data:
        category = record[2]
        amount = record[3]
        
        # Use dict.get() for safe, efficient accumulation. 
        # If the key doesn't exist, it defaults to 0.0 or 0, preventing KeyError.
        category_totals[category] = category_totals.get(category, 0.0) + amount
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\n--- Category Sales Summary (Sorting dict.items()) ---")
    
    # Sort the dictionary view (items()) by the total sales amount (index 1 of the tuple)
    sorted_summary = sorted(
        category_totals.items(), 
        key=operator.itemgetter(1), 
        reverse=True
    )

    for category, total in sorted_summary:
        count = category_counts[category]
        avg = total / count
        print(f"  Category: {category:<12} | Total Sales: ${total:10.2f} | Transactions: {count} | Avg Sale: ${avg:.2f}")

    # 7. Advanced Slicing with Step: Analyzing a specific subset
    print("\n--- Slicing with Step: Every Second Electronics Sale ---")
    # First, filter the list to only include 'Electronics' records
    electronics_sales = [r for r in sorted_data if r[2] == 'Electronics']
    
    # Slice using a step of 2 [start:end:step] to get every second item
    every_second_sale = electronics_sales[::2]
    
    for i, record in enumerate(every_second_sale):
        print(f"  {i+1}. Date: {record[0].strftime('%Y-%m-%d')} | Amount: ${record[3]:.2f}")

# --- Execution ---
if __name__ == "__main__":
    print("Starting Transaction Analysis System...")
    
    # Step 1: Pre-process and sort data
    sorted_records = process_data(RAW_DATA)
    
    # Step 2: Analyze and report
    analyze_transactions(sorted_records)
    
    print("\nAnalysis Complete.")

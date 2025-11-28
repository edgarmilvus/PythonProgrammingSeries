
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

# inventory_processor.py

"""
Advanced Application Script: Retail Inventory Data Processor
This script simulates processing raw sales transaction data stored in a list of lists.
It demonstrates iteration, indexing, slicing, list mutation, and list comprehensions
to clean, validate, calculate totals, and generate a structured report.
"""

# ----------------------------------------------------------------------
# 1. Initial Data Setup
# Format: [Item Name (str), Quantity (int), Unit Price (float), Status (str)]
# Status is initially 'Pending'
# ----------------------------------------------------------------------

raw_transactions = [
    ["Laptop Pro X1", 2, 1299.99, "Pending"],
    ["Monitor 4K", 5, 349.50, "Pending"],
    ["USB Hub C", 10, 25.00, "Pending"],
    ["Ergo Mouse", 1, 45.99, "Pending"],
    ["Keyboard Mech", 3, 110.00, "Pending"],
    ["Webcam HD", 7, 55.50, "Pending"],
    ["Laptop Pro X1", 1, 1299.99, "Pending"], # Duplicate item, different transaction
]

HIGH_VALUE_THRESHOLD = 500.00
TAX_RATE = 0.08

# ----------------------------------------------------------------------
# 2. Core Processing Function (Demonstrates Mutation and Indexing)
# ----------------------------------------------------------------------

def process_transactions(data_list):
    """
    Iterates through the transaction list, calculates line totals,
    and updates the status based on a high-value threshold.
    This function modifies the original list (in-place mutation).
    """
    print("--- 2. Starting Transaction Processing and Mutation ---")
    processed_count = 0
    
    # We use enumerate() to get both the index (i) and the item (transaction)
    # This is crucial for direct indexed mutation later.
    for i, transaction in enumerate(data_list):
        
        # Accessing elements by index: Quantity is index 1, Price is index 2
        quantity = transaction[1]
        unit_price = transaction[2]
        line_total = quantity * unit_price
        
        # Mutating the list: Updating the 'Status' field (index 3)
        # This demonstrates direct list mutation using nested indexing: data_list[i][3]
        if line_total >= HIGH_VALUE_THRESHOLD:
            data_list[i][3] = "Flagged: High Value"
        else:
            data_list[i][3] = "Processed: Standard"
            
        # Mutating the list: Inserting the calculated total at index 4
        # This permanently changes the structure of every inner list in the original data_list
        data_list[i].insert(4, round(line_total, 2))
        
        processed_count += 1
        
    print(f"Processed {processed_count} records. List structure mutated.")
    return data_list

# ----------------------------------------------------------------------
# 3. Summary Generation (Demonstrates Slicing and List Comprehensions)
# ----------------------------------------------------------------------

def generate_summary(processed_data):
    """
    Generates key summaries using slicing and list comprehensions.
    """
    print("\n--- 3. Generating Summary Report ---")
    
    # A. List Comprehension 1: Extract all item names (Index 0)
    item_names = [item[0] for item in processed_data]
    # Using set() to quickly find the count of unique items
    print(f"Total unique items tracked: {len(set(item_names))}") 
    
    # B. List Comprehension 2: Filter only High-Value Flagged items
    # We check index 3 (the updated status field)
    high_value_sales = [
        t for t in processed_data 
        if t[3].startswith("Flagged")
    ]
    print(f"High Value Transactions identified: {len(high_value_sales)}")
    
    # C. List Comprehension 3: Calculate Subtotal from all transactions
    # The total is now stored at index 4 (due to mutation in step 2)
    subtotal = sum([transaction[4] for transaction in processed_data])
    
    # Calculate tax and grand total
    tax_amount = subtotal * TAX_RATE
    grand_total = subtotal + tax_amount
    
    # D. Final Report Structure (Sorting)
    # Sort the high-value items by their total amount (index 4) in descending order.
    # The sort() method is an in-place mutation of the high_value_sales list.
    high_value_sales.sort(key=lambda x: x[4], reverse=True)
    
    print("\n--- High-Value Sales Detailed Report (Sorted by Total) ---")
    for item in high_value_sales:
        # Accessing elements by index for formatted display
        print(f"  {item[0]:<15} | Qty: {item[1]:<3} | Unit P: ${item[2]:<8.2f} | Total: ${item[4]:<10.2f} | Status: {item[3]}")
        
    print("\n--- Financial Totals ---")
    print(f"Subtotal: ${subtotal:,.2f}")
    print(f"Tax ({TAX_RATE*100}%): ${tax_amount:,.2f}")
    print(f"Grand Total: ${grand_total:,.2f}")
    
    return high_value_sales

# ----------------------------------------------------------------------
# 4. Execution Flow
# ----------------------------------------------------------------------

if __name__ == "__main__":
    
    # 4a. Initial State Check
    print("1. Initial Raw Data Structure:")
    for record in raw_transactions:
        print(f"  {record}")
        
    # 4b. Process the data (This mutates raw_transactions in place)
    final_data = process_transactions(raw_transactions)
    
    # 4c. Verification: The original list 'raw_transactions' is now mutated
    print("\n--- 2b. Verification: The original list 'raw_transactions' is now mutated ---")
    for record in raw_transactions:
        # Note the presence of the calculated total (index 4)
        print(f"  {record}")
        
    # 4d. Generate Final Report
    generate_summary(final_data)

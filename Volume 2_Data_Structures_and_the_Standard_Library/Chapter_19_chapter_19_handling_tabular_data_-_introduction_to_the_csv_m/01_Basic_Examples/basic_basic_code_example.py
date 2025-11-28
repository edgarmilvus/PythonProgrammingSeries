
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

import csv
import os

# 1. Setup: Define the file path and the structured data we want to save
FILE_NAME = "inventory_report.csv"
inventory_data = [
    ['Product ID', 'Name', 'Quantity', 'Price'], # Header Row
    ['P001', 'Widget Alpha', 150, 10.99],
    ['P002', 'Gear Beta', 45, 25.50],
    ['P003', 'Cog Gamma', 300, 1.25]
]

# --- PART A: Writing the CSV File using csv.writer ---

print(f"--- Creating {FILE_NAME} ---")
try:
    # Open the file in write mode ('w'). Crucially, newline='' prevents extra blank rows.
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file_handle:
        
        # 1. Instantiate the writer object, linking it to the open file handle
        writer = csv.writer(file_handle)
        
        # 2. Write all rows defined in the list of lists
        writer.writerows(inventory_data)
    
    print(f"Successfully wrote {len(inventory_data)} rows to {FILE_NAME}.")

except IOError as e:
    print(f"Error writing file: {e}")
    
# --- PART B: Reading the CSV File using csv.reader ---

print("\n--- Reading Data Back and Processing ---")
try:
    # Open the file in read mode ('r').
    with open(FILE_NAME, mode='r', encoding='utf-8') as file_handle:
        
        # 1. Instantiate the reader object
        reader = csv.reader(file_handle)
        
        # 2. Iterate through each row provided by the reader object
        for row in reader:
            # The 'row' variable is a list of strings representing one line of the CSV
            
            # Print the raw list data received
            print(f"Raw Row: {row}")
            
            # Example Processing: Skip the header row and process numeric data
            if row[0] != 'Product ID': 
                product_id = row[0]
                
                # CRITICAL: CSV data is always read as strings. We must use Type Conversion (Casting).
                quantity = int(row[2]) 
                price = float(row[3])
                
                inventory_value = quantity * price
                
                print(f"  -> Inventory Check: {product_id} has {quantity} units. Total value: ${inventory_value:.2f}")
                
except FileNotFoundError:
    print(f"Error: The file {FILE_NAME} was not found.")
except Exception as e:
    print(f"An unexpected error occurred during reading: {e}")

# --- PART C: Cleanup ---
# Remove the file created during the script execution
if os.path.exists(FILE_NAME):
    os.remove(FILE_NAME)

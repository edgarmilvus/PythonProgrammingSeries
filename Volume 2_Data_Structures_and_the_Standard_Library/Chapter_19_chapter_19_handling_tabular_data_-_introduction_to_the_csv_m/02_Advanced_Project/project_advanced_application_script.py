
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

import csv
import os
from datetime import datetime

# --- Configuration and File Paths ---
INPUT_FILE = 'sales_regional.csv'
OUTPUT_FILE = 'sales_standardized.csv'
DATE_INPUT_FORMAT = '%d/%m/%Y' # European format: Day/Month/Year
DATE_OUTPUT_FORMAT = '%Y-%m-%d' # ISO standard format: Year-Month-Day

def create_sample_data():
    """Generates a sample semicolon-delimited CSV file for input."""
    data = [
        ['Transaction_ID', 'Date', 'Product', 'Revenue', 'Cost', 'Region'],
        ['T1001', '01/03/2023', 'Laptop Pro', '1200.50', '850.00', 'EU'],
        ['T1002', '15/03/2023', 'Monitor 4K', '450.00', '300.25', 'EU'],
        ['T1003', '28/03/2023', 'Keyboard Mech', '150.99', '100.00', 'EU'],
        ['T1004', '05/04/2023', 'Mouse Wireless', '50.00', '35.00', 'EU'],
        ['T1005', '10/04/2023', 'Server Rack', '5000.00', '3500.00', 'EU']
    ]
    
    # Use 'w' mode to write the file, specifying the semicolon delimiter
    with open(INPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';')
        writer.writerows(data)
    print(f"[SETUP] Created sample input file: {INPUT_FILE} (Semicolon delimited)")

def process_sales_report(input_path, output_path):
    """
    Reads regional sales data, calculates profit margin, standardizes dates,
    and writes the result to a standard CSV file.
    """
    processed_count = 0
    
    # 1. Open the source file for reading (using the custom delimiter)
    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as infile:
            # Initialize the reader object, specifying the semicolon delimiter
            reader = csv.reader(infile, delimiter=';')
            
            # 2. Open the destination file for writing (using standard comma delimiter)
            with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
                # Initialize the writer object. Use QUOTE_MINIMAL for efficiency.
                writer = csv.writer(outfile, 
                                    delimiter=',', 
                                    quoting=csv.QUOTE_MINIMAL)
                
                # Process the header row first
                try:
                    header = next(reader)
                    # Add the new calculated field to the header
                    new_header = header[:-2] + ['Revenue', 'Cost', 'Profit_Margin', 'Region']
                    # Standardize the date column name
                    new_header[1] = 'Standard_Date'
                    writer.writerow(new_header)
                except StopIteration:
                    print(f"Error: Input file {input_path} is empty.")
                    return

                # 3. Iterate through the data rows
                for row in reader:
                    if len(row) < 6:
                        print(f"Skipping malformed row: {row}")
                        continue
                        
                    transaction_id, date_str, product, revenue_str, cost_str, region = row
                    
                    try:
                        # Convert string revenue/cost to floating point numbers
                        revenue = float(revenue_str)
                        cost = float(cost_str)
                        
                        # Calculate the derived metric: Profit Margin (as a percentage)
                        profit = revenue - cost
                        profit_margin = (profit / revenue) * 100 if revenue != 0 else 0
                        
                        # Standardize the date format using datetime
                        date_obj = datetime.strptime(date_str, DATE_INPUT_FORMAT)
                        standard_date = date_obj.strftime(DATE_OUTPUT_FORMAT)
                        
                        # 4. Assemble the new, standardized row
                        output_row = [
                            transaction_id,
                            standard_date,
                            product,
                            f"{revenue:.2f}", # Format floats for clean output
                            f"{cost:.2f}",
                            f"{profit_margin:.2f}",
                            region
                        ]
                        
                        # 5. Write the processed row to the output file
                        writer.writerow(output_row)
                        processed_count += 1
                        
                    except ValueError as e:
                        # Handle cases where data conversion (float or date) fails
                        print(f"[WARNING] Skipping row due to data conversion error: {e} in row {transaction_id}")
                        continue
                        
        print(f"\n[SUCCESS] Data translation complete.")
        print(f"Processed {processed_count} records and saved to {output_path}.")
        
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {input_path}")
    except Exception as e:
        print(f"[CRITICAL ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Clean up previous runs if files exist
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # 1. Setup the input data
    create_sample_data()
    
    # 2. Execute the processing pipeline
    process_sales_report(INPUT_FILE, OUTPUT_FILE)
    
    # 3. Optional: Print the first few lines of the output for verification
    print("\n--- Output Verification (First 3 lines) ---")
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 3:
                    print(line.strip())
                else:
                    break

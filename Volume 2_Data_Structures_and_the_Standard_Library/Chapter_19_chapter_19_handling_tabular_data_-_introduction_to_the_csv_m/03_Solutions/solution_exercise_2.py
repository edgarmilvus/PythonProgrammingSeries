
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

def inventory_audit():
    """Reads inventory data, calculates total value, and prints a summary."""
    input_file = 'inventory_data.csv'
    grand_total = 0.0
    report_lines = []

    try:
        # Requirement 1: Reading data using csv.reader
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            
            # Hint: Skip header row
            try:
                next(reader) 
            except StopIteration:
                print(f"Error: {input_file} is empty.")
                return

            # Process data rows
            for row in reader:
                if len(row) < 3:
                    print(f"Skipping malformed row: {row}")
                    continue
                
                product_name = row[0]
                price_str = row[1]
                quantity_str = row[2]
                
                try:
                    # Requirement 2: Conversion to float and int
                    price = float(price_str)
                    quantity = int(quantity_str)
                    
                    # Requirement 3: Calculation
                    total_value = price * quantity
                    grand_total += total_value
                    
                    # Requirement 4: Formatted output preparation
                    # Using f-string formatting for alignment and currency (.2f)
                    report_lines.append(
                        f"{product_name:<15}: ${total_value:,.2f}"
                    )
                    
                except ValueError:
                    # Basic error handling for malformed numbers
                    print(f"Warning: Could not convert data for product '{product_name}'. Skipping calculation.")
        
        # Output the final report
        print("\n--- Inventory Stock Value Report ---")
        for line in report_lines:
            print(line)
            
        print("-" * 35)
        # Requirement 5: Grand total summary
        print(f"GRAND TOTAL INVENTORY VALUE: ${grand_total:,.2f}")
        print("-" * 35)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Please ensure it is created.")

# Run Exercise 1
# inventory_audit()

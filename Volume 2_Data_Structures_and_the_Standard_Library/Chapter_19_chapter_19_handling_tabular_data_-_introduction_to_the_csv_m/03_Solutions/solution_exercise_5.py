
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

def process_transactions_with_logging():
    """
    Reads transactions, filters based on amount/status, calculates total, 
    and logs invalid amounts to a separate CSV file.
    """
    input_file = 'transactions.csv'
    error_file = 'error_log.csv'
    
    total_qualified_amount = 0.0
    
    try:
        # Open input file (read) and error log file (write) simultaneously
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
             open(error_file, mode='w', newline='', encoding='utf-8') as error_log_file:
            
            # Input reader
            reader = csv.reader(infile)
            # Output writer for errors
            error_writer = csv.writer(error_log_file)
            
            # Handle Header
            try:
                header = next(reader)
                # Requirement 5: Write header to error log
                error_writer.writerow(header)
            except StopIteration:
                print("Input file is empty.")
                return

            # Main processing loop
            for row in reader:
                if len(row) < 3:
                    continue 

                transaction_id = row[0]
                amount_str = row[1]
                status = row[2]
                
                # Requirement 2: Data Validation using try...except
                try:
                    # Attempt to convert amount string to float
                    amount = float(amount_str)
                    
                    # Requirement 3: Filtering Logic (Dual condition)
                    if status == 'Completed' and amount >= 100.00:
                        total_qualified_amount += amount
                        
                except ValueError:
                    # If conversion fails (e.g., 'N/A', 'Error'), log the row
                    # Requirement 5: Writing the error row to the log file
                    error_writer.writerow(row)
                    print(f"Logged invalid amount for TX ID {transaction_id}: '{amount_str}'")

        # Requirement 4: Print summary
        print("\n--- Transaction Processing Summary ---")
        print(f"Total sum of qualifying completed transactions (>= $100.00): ${total_qualified_amount:,.2f}")
        print(f"Errors logged to: {error_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run Exercise 4
# process_transactions_with_logging()


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

def filter_dark_mode_users():
    """Reads a semicolon-delimited file, filters, and writes standard CSV output."""
    input_file = 'preferences_input.txt'
    output_file = 'dark_mode_users.csv'
    
    dark_mode_users = []
    
    try:
        # Requirement 1: Reading custom delimiter (semicolon)
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            # Crucial: Specify the delimiter argument
            reader = csv.reader(infile, delimiter=';')
            
            # Skip header
            next(reader) 
            
            for row in reader:
                if len(row) >= 3:
                    user_id = row[0]
                    theme = row[2]
                    
                    # Requirement 2: Filtering logic (Theme is the third column, index 2)
                    if theme.strip() == 'Dark Mode':
                        # Append only the required columns (UserID and Theme)
                        dark_mode_users.append([user_id, theme])
                        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except StopIteration:
        print(f"Error: {input_file} is empty or only contains a header.")
        return
        
    # Requirement 3 & 4: Writing standard CSV output (comma is default)
    output_header = ['UserID', 'Theme']
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            
            # Requirement 5: Write header
            writer.writerow(output_header) 
            
            # Write filtered data
            writer.writerows(dark_mode_users)
            
        print(f"Successfully filtered {len(dark_mode_users)} users who prefer Dark Mode.")
        print(f"Output written to: {output_file}")

    except Exception as e:
        print(f"An error occurred during output file writing: {e}")

# Run Exercise 3
# filter_dark_mode_users()

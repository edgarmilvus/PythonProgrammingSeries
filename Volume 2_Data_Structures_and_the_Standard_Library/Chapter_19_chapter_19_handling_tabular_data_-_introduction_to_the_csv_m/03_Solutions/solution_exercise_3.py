
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

def generate_system_report():
    """Scans the current directory and generates a CSV report of files."""
    output_file = 'system_report.csv'
    # Requirement 1: Utilize os module to get the target directory
    target_dir = os.getcwd()
    
    # Requirement 1 & 3: Capture current time once for the report timestamp
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Scanning directory: {target_dir}")
    
    # Requirement 5: Define the header
    header = ['Filename', 'Size (Bytes)', 'Report Timestamp']
    
    try:
        # Requirement 4: Open file in write mode
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)

            # Iterate through all items in the directory
            for item_name in os.listdir(target_dir):
                
                # Requirement 2: Use os.path.join for safe path construction
                full_path = os.path.join(target_dir, item_name)
                
                # Check if the item is a file (ignore directories)
                if os.path.isfile(full_path):
                    try:
                        # Requirement 3: Collect file size
                        file_size = os.path.getsize(full_path)
                        
                        # Prepare the row data
                        row_data = [
                            item_name,
                            file_size,
                            current_time 
                        ]
                        
                        # Requirement 4: Write the row
                        writer.writerow(row_data)
                        
                    except OSError as e:
                        # Handle cases where permissions might prevent size retrieval
                        print(f"Warning: Could not access metadata for {item_name}: {e}")
                        
        print(f"System report successfully generated at: {output_file}")

    except Exception as e:
        print(f"An error occurred during file writing: {e}")

# Run Exercise 2
# generate_system_report()

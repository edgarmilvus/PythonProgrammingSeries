
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

# --- Exercise 3 Solution ---

def format_bytes(size_bytes):
    """Converts bytes to a human-readable string (KB, MB, GB)."""
    if size_bytes == 0:
        return "0 B"
    
    # Define units and calculate using 1024 (binary standard)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    
    # Ensure index does not exceed bounds
    if i >= len(units):
        i = len(units) - 1
        p = math.pow(1024, i)
        
    size_formatted = round(size_bytes / p, 2)
        
    return f"{size_formatted:.2f} {units[i]}"

def get_total_size(start_path):
    """Calculates the total size of all files in a directory tree."""
    if not os.path.exists(start_path):
        raise FileNotFoundError(f"Path not found: {start_path}")
        
    total_size = 0
    
    print("\n--- Exercise 3: Calculating Total Size ---")
    
    for root, dirs, files in os.walk(start_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            
            try:
                # Retrieve the size of the file
                total_size += os.path.getsize(full_path)
            
            # Handle common file system errors gracefully
            except (PermissionError, FileNotFoundError) as e:
                print(f"Warning: Skipping file '{full_path}' due to error: {e}")
                continue
                
    return total_size

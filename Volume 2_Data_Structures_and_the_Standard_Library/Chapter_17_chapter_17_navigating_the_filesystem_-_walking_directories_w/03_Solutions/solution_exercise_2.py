
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

# --- Exercise 1 Solution ---

def count_file_types(start_path):
    """Counts files by type in a directory tree."""
    if not os.path.exists(start_path):
        # Raise FileNotFoundError if the starting path is invalid
        raise FileNotFoundError(f"Path not found: {start_path}")
    
    counts = {'py': 0, 'txt': 0, 'csv': 0, 'others': 0}
    
    for root, dirs, files in os.walk(start_path):
        for filename in files:
            # Convert filename to lowercase for case-insensitive checking
            lower_filename = filename.lower()
            
            # Check against required extensions
            if lower_filename.endswith('.py'):
                counts['py'] += 1
            elif lower_filename.endswith('.txt'):
                counts['txt'] += 1
            elif lower_filename.endswith('.csv'):
                counts['csv'] += 1
            else:
                counts['others'] += 1
    
    return counts

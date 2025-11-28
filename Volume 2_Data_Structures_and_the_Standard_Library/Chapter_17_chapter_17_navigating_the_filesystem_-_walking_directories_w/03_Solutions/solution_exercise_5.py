
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

# --- Exercise 4 Solution ---

def advanced_file_finder(start_dir, exclusion_paths=None):
    """Finds files while excluding specified directory branches based on absolute path."""
    if exclusion_paths is None:
        exclusion_paths = []

    # 1. Normalize exclusion paths for robust comparison
    # Add os.sep to the end to prevent matching paths like 'temp' and 'template'
    normalized_exclusion_paths = [
        os.path.abspath(p) + os.sep for p in exclusion_paths
    ]
    
    # Also include the path without the separator for exact match checking
    normalized_exclusion_paths.extend([os.path.abspath(p) for p in exclusion_paths])
    
    found_files = []
    
    print("\n--- Exercise 4: Contextual Pruning ---")
    
    for root, dirs, files in os.walk(start_dir):
        normalized_root = os.path.abspath(root)
        
        # 2. Check if the current root path is excluded or is a subdirectory of an excluded path
        is_excluded = False
        for excluded_path in normalized_exclusion_paths:
            # Check if the root path starts with the excluded path
            if normalized_root.startswith(excluded_path):
                is_excluded = True
                break
        
        if is_excluded:
            # CRITICAL: Stop descent immediately by clearing the 'dirs' list
            dirs[:] = []
            print(f"Pruned entire branch: {root}")
            continue

        # 3. File processing logic (only process files in non-excluded roots)
        for filename in files:
            full_path = os.path.join(root, filename)
            found_files.append(full_path)
            
    return found_files


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

# env_checker.py

import os
import sys

def check_path_environment():
    """
    Retrieves and parses the PATH environment variable using os.pathsep.
    """
    # 1. Access Variable: Use os.environ.get() for safe access
    path_value = os.environ.get('PATH')

    # 2. Handle Absence
    if not path_value:
        print("Warning: The 'PATH' environment variable is not set.")
        sys.exit(0) # Exit gracefully

    # 3. Determine Separator: Use os.pathsep for cross-platform compatibility
    separator = os.pathsep
    
    # 4. Parsing: Split the string into a list of directories
    path_list = path_value.split(separator)

    # Clean up empty strings that might result from trailing separators
    path_list = [p for p in path_list if p]

    # 5. Reporting
    print("--- PATH Environment Variable Analysis ---")
    print(f"Raw PATH Value:\n{path_value[:100]}...") # Print first 100 chars
    print(f"Determined Separator (os.pathsep): '{separator}'")
    print(f"Total Directories Found: {len(path_list)}")
    print("-" * 35)
    
    print("First 5 Directories:")
    
    # Print the first five directories (or fewer)
    for i, path in enumerate(path_list[:5]):
        print(f"  {i+1}. {path}")
    
    if len(path_list) > 5:
        print("  ...")
    
    print("----------------------------------------")

if __name__ == "__main__":
    check_path_environment()

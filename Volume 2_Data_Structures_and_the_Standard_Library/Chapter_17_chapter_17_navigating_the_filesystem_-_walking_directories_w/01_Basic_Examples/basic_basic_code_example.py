
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

import os
import shutil
from pathlib import Path

# Define the root directory we will traverse
ROOT_DIR = "inventory_root"

# --- Setup: Create a dummy directory structure ---
# This section ensures the code is self-contained and runnable anywhere.
try:
    # 1. Create the main root directory
    Path(ROOT_DIR).mkdir(exist_ok=True)
    
    # 2. Create nested subdirectories and files
    Path(ROOT_DIR, "Photos_2023").mkdir()
    Path(ROOT_DIR, "Photos_2023", "P10001.jpg").touch()
    Path(ROOT_DIR, "Photos_2023", "P10002.jpg").touch()
    
    # 3. Create another branch
    Path(ROOT_DIR, "Videos_Archive").mkdir()
    Path(ROOT_DIR, "Videos_Archive", "setup.log").touch()
    
    # 4. Create a deeply nested branch
    Path(ROOT_DIR, "Misc").mkdir()
    Path(ROOT_DIR, "Misc", "Sub_Config").mkdir()
    Path(ROOT_DIR, "Misc", "Sub_Config", "notes.txt").touch()
    
    # 5. File directly in the root
    Path(ROOT_DIR, "readme.md").touch()

except FileExistsError:
    # This block handles potential errors during setup, though highly unlikely
    # given the use of exist_ok=True and the cleanup phase.
    pass

print(f"--- Starting recursive traversal of: {ROOT_DIR} ---\n")

# --- Core Logic: Using os.walk ---

# os.walk is a generator that traverses the directory tree depth-first.
# It yields a 3-tuple (root, dirs, files) for every directory visited.
for current_root, directories_in_root, files_in_root in os.walk(ROOT_DIR):
    
    # 1. Display the current directory path (the 'root' of this iteration)
    print(f"Processing Directory: {current_root}")
    
    # 2. Display the immediate subdirectories found within current_root
    print(f"  [Found Sub-Dirs]: {directories_in_root}")
    
    # 3. Display the immediate files found within current_root
    print(f"  [Found Files]: {files_in_root}")
    
    # Example task: List the full path of every file found in this specific directory
    for filename in files_in_root:
        # os.path.join is crucial: it safely combines the directory path (current_root) 
        # and the file name (filename) into a complete, usable path.
        full_path = os.path.join(current_root, filename)
        print(f"    -> Full Path: {full_path}")
        
    print("-" * 20)
    
# --- Cleanup ---
# Always clean up temporary structures created for testing
try:
    shutil.rmtree(ROOT_DIR)
    print(f"\nSuccessfully cleaned up temporary directory: {ROOT_DIR}")
except OSError as e:
    print(f"Error during cleanup: {e}")


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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

import os
import shutil
import stat
import math

# --- Setup for Demonstration and Testing ---

TEST_DIR = "test_walk_structure"

def setup_test_environment():
    """Creates a temporary directory structure for testing all exercises."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    
    os.makedirs(TEST_DIR, exist_ok=True)
    
    # 1. Files for Exercise 1
    with open(os.path.join(TEST_DIR, "script.py"), 'w') as f: f.write("print('hello')")
    with open(os.path.join(TEST_DIR, "data.csv"), 'w') as f: f.write("1,2,3")
    with open(os.path.join(TEST_DIR, "README.TXT"), 'w') as f: f.write("Read me") # Case-insensitive check
    with open(os.path.join(TEST_DIR, "license.md"), 'w') as f: f.write("MIT") # Others
    
    # 2. Directories for Exercise 2 (Pruning by name)
    os.makedirs(os.path.join(TEST_DIR, ".git", "objects"), exist_ok=True)
    os.makedirs(os.path.join(TEST_DIR, ".venv", "bin"), exist_ok=True)
    os.makedirs(os.path.join(TEST_DIR, "src", "node_modules"), exist_ok=True)
    
    # 3. Directories for Exercise 4 (Pruning by absolute path)
    EXCLUDED_BRANCH = os.path.join(TEST_DIR, "large_backups")
    os.makedirs(EXCLUDED_BRANCH, exist_ok=True)
    os.makedirs(os.path.join(EXCLUDED_BRANCH, "archive", "temp"), exist_ok=True)
    with open(os.path.join(EXCLUDED_BRANCH, "temp_file.dat"), 'w') as f: f.write("large data")
    
    # 4. Directories for Exercise 5 (Empty directories)
    os.makedirs(os.path.join(TEST_DIR, "empty_folder"), exist_ok=True)
    os.makedirs(os.path.join(TEST_DIR, "src", "sub_empty"), exist_ok=True)
    
    # 5. File for Exercise 3 (Size check and potential error simulation)
    large_file_path = os.path.join(TEST_DIR, "large_data.bin")
    with open(large_file_path, 'wb') as f:
        f.seek(1024 * 50 - 1) # 50 KB file
        f.write(b'\0')
        
    # Simulate a file that might cause PermissionError (difficult to simulate robustly without root, 
    # but we include the try/except block anyway as required)
    
    return os.path.abspath(TEST_DIR)

def cleanup_test_environment():
    """Removes the temporary directory structure."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

# --- End of Setup ---


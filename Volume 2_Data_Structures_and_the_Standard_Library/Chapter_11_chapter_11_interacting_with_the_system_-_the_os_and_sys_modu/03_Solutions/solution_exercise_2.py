
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

# dir_snapshot.py

import os
import sys

def generate_snapshot(target_path):
    """
    Analyzes the contents of a directory and reports file and directory counts.
    """
    file_count = 0
    dir_count = 0

    # 1. Input Handling: Check if path exists and is a directory
    if not os.path.exists(target_path):
        print(f"Error: Path not found: '{target_path}'", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isdir(target_path):
        print(f"Error: Path is not a directory: '{target_path}'", file=sys.stderr)
        sys.exit(1)

    print(f"--- Snapshot Report for: {os.path.abspath(target_path)} ---")

    try:
        # 2. Directory Traversal: Get contents
        entries = os.listdir(target_path)
        
        # 3. Classification and 4. Counting
        for entry in entries:
            # Construct the full path for accurate checking
            full_path = os.path.join(target_path, entry)

            if os.path.isdir(full_path):
                dir_count += 1
            elif os.path.isfile(full_path):
                file_count += 1
            # Note: We ignore symlinks, devices, etc., only counting files/dirs

    # 6. Error Robustness: Handle permission or other OS errors during listing
    except PermissionError:
        print(f"Error: Permission denied when accessing '{target_path}'", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"An unexpected OS error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Output
    print(f"Total entries found: {len(entries)}")
    print(f"  > Total Files: {file_count}")
    print(f"  > Total Directories: {dir_count}")
    print("-----------------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <directory_path>", file=sys.stderr)
        sys.exit(1)
    
    input_path = sys.argv[1]
    generate_snapshot(input_path)

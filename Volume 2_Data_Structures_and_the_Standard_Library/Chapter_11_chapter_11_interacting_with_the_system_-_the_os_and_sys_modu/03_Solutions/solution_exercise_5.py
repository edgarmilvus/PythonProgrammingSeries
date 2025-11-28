
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

# deep_cleaner.py

import os
import sys

def deep_search_and_cleanup(start_dir):
    """
    Recursively searches for 'temp.log' files and handles deletion confirmation.
    """
    # 1. Input Path validation
    if not os.path.isdir(start_dir):
        print(f"Error: Invalid directory path provided: {start_dir}", file=sys.stderr)
        sys.exit(1)

    found_files = []
    
    print(f"Starting deep search in: {os.path.abspath(start_dir)}")

    # 2. Recursive Traversal using os.walk
    try:
        for root, directories, filenames in os.walk(start_dir):
            # 3. File Identification
            if 'temp.log' in filenames:
                # 4. Full Path Reporting and storage
                full_path = os.path.join(root, 'temp.log')
                found_files.append(full_path)
                print(f"  [FOUND] {full_path}")
    
    except PermissionError as e:
        print(f"\nWarning: Skipping directory due to permission error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred during traversal: {e}", file=sys.stderr)
        sys.exit(1)

    num_found = len(found_files)
    if num_found == 0:
        print("\nSearch complete. No 'temp.log' files found.")
        return

    print(f"\n--- Search Complete: {num_found} file(s) found. ---")

    # 5. Deletion Challenge (Prompt)
    confirmation = input(f"Do you want to delete all {num_found} file(s) found? (y/N): ").strip().lower()

    if confirmation == 'y':
        deleted_count = 0
        print("\nAttempting deletion...")
        
        for file_path in found_files:
            try:
                # 6. Safe Deletion
                os.remove(file_path)
                print(f"  [DELETED] {file_path}")
                deleted_count += 1
            except PermissionError:
                print(f"  [FAILED] Permission denied for {file_path}")
            except OSError as e:
                print(f"  [FAILED] Could not delete {file_path}: {e}")
        
        print(f"\nCleanup finished. Successfully deleted {deleted_count} files.")
    else:
        print("Deletion cancelled by user.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <root_directory_to_clean>", file=sys.stderr)
        sys.exit(1)
    
    target_directory = sys.argv[1]
    deep_search_and_cleanup(target_directory)


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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import os
import sys
from typing import List, Tuple, Dict, Any

# 1. Configuration Constants
# Directories to be explicitly ignored during traversal (pruned).
IGNORED_DIRS: List[str] = [
    ".git", 
    "__pycache__", 
    "node_modules", 
    "venv", 
    ".vscode",
    "temp"
]

# Target file extensions for the audit (case-insensitive check later).
TARGET_EXTENSIONS: Tuple[str, ...] = (".py", ".md", ".ini", ".cfg", ".txt", ".json")

# 2. Helper Function for Size Formatting
def format_size(size_bytes: int) -> str:
    """Converts raw bytes into a human-readable string (KB, MB, GB)."""
    if size_bytes >= (1024 ** 3):
        return f"{size_bytes / (1024 ** 3):.2f} GB"
    if size_bytes >= (1024 ** 2):
        return f"{size_bytes / (1024 ** 2):.2f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes} Bytes"

# 3. Core Auditing Function (Utilizing os.walk)
def audit_directory(start_path: str) -> Dict[str, Any]:
    """
    Traverses a directory recursively, calculates total size of target files,
    and identifies the largest single target file, while pruning ignored directories.
    """
    # Initial path validation
    if not os.path.exists(start_path):
        print(f"Error: Path not found: {start_path}", file=sys.stderr)
        return {}
    if not os.path.isdir(start_path):
        print(f"Error: Path must be a directory: {start_path}", file=sys.stderr)
        return {}

    total_size_bytes: int = 0
    # largest_file stores (filepath, size_in_bytes)
    largest_file: Tuple[str, int] = ("", 0) 
    file_count: int = 0
    
    # Ensure start_path is absolute for clear reporting
    start_path = os.path.abspath(start_path)

    print(f"--- Starting Audit of: {start_path} ---")

    # The core traversal loop using os.walk
    for root, dirs, files in os.walk(start_path):
        
        # 4. Critical Optimization: Directory Pruning
        # We modify the 'dirs' list in place (using slicing `[:]`). 
        # os.walk respects this modification and will not recurse into pruned directories.
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        # 5. File Processing Loop
        for filename in files:
            # Check if the file name ends with any of the target extensions (case-insensitive)
            if filename.lower().endswith(TARGET_EXTENSIONS):
                full_path = os.path.join(root, filename)
                
                try:
                    # Retrieve the file size
                    file_size = os.path.getsize(full_path)
                    total_size_bytes += file_size
                    file_count += 1

                    # 6. Largest File Tracking
                    if file_size > largest_file[1]:
                        largest_file = (full_path, file_size)

                except OSError as e:
                    # Handle common exceptions like permission denied or file deletion during walk
                    print(f"Warning: Could not access {full_path}. Error: {e}", file=sys.stderr)
                    continue

    # 7. Compile Results Dictionary
    results = {
        "start_path": start_path,
        "extensions": TARGET_EXTENSIONS,
        "pruned_dirs": IGNORED_DIRS,
        "total_files": file_count,
        "total_size_bytes": total_size_bytes,
        "total_size_human": format_size(total_size_bytes),
        "largest_file_path": largest_file[0],
        "largest_file_size_bytes": largest_file[1],
        "largest_file_size_human": format_size(largest_file[1])
    }
    
    return results

# 8. Reporting Function
def generate_report(results: Dict[str, Any]) -> None:
    """Prints the final audit results in a structured, readable format."""
    if not results or results.get("total_files") is None:
        print("Audit failed or returned incomplete data.")
        return

    print("\n" + "="*70)
    print("PROFESSIONAL DIRECTORY AUDIT REPORT")
    print("="*70)
    print(f"Target Path:             {results['start_path']}")
    print(f"Extensions Audited:      {', '.join(results['extensions'])}")
    print(f"Directories Pruned:      {', '.join(results['pruned_dirs'])}")
    print("-" * 70)
    
    print(f"Total Target Files Found: {results['total_files']:,}")
    print(f"Cumulative Size:          {results['total_size_human']}")
    print("-" * 70)
    
    if results['largest_file_path']:
        print("Largest Single Target File Identified:")
        print(f"  Path: {results['largest_file_path']}")
        print(f"  Size: {results['largest_file_size_human']}")
    else:
        print("Note: No files matching the target extensions were found.")
    print("="*70 + "\n")


# 9. Main Execution Block
if __name__ == "__main__":
    # Determine the starting path. Prioritize command-line argument 
    # or default to the current working directory.
    if len(sys.argv) > 1:
        START_DIR = sys.argv[1]
    else:
        START_DIR = os.getcwd()
        print(f"Using current working directory as default: {START_DIR}")

    audit_results = audit_directory(START_DIR)
    generate_report(audit_results)

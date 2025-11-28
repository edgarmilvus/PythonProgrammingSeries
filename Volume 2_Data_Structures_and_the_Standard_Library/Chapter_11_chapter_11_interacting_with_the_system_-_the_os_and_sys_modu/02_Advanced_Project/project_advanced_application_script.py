
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

import sys
import os

# --- Configuration ---
REQUIRED_ARGS = 3  # Script name, Directory Path, File Extension
DEFAULT_SIZE_LIMIT_MB = 10  # Default limit if environment variable is not set

def display_system_info():
    """Prints basic system and execution environment information."""
    print("--- System Environment Report ---")
    # Using sys module to report Python version details
    print(f"Python Interpreter: {sys.version.split()[0]} on {sys.platform}")
    # Using os module to report OS type and CWD
    print(f"Operating System Type: {os.name}")
    print(f"Current Working Directory: {os.getcwd()}")
    print("-" * 35)

def get_size_limit_bytes():
    """
    Retrieves the file size limit from the environment variable 
    'CLEANUP_LIMIT_MB' or uses a default value. Returns size in bytes.
    """
    # Attempt to fetch the environment variable 'CLEANUP_LIMIT_MB'
    limit_mb_str = os.getenv('CLEANUP_LIMIT_MB')
    
    limit_mb = DEFAULT_SIZE_LIMIT_MB
    
    if limit_mb_str:
        try:
            # Convert the environment variable value (string) to an integer (int)
            limit_mb = int(limit_mb_str)
            if limit_mb <= 0:
                 # Handle non-positive limits
                print(f"[Warning] Invalid limit '{limit_mb_str}' detected in ENV. Using default {DEFAULT_SIZE_LIMIT_MB} MB.")
                limit_mb = DEFAULT_SIZE_LIMIT_MB
            else:
                print(f"[Info] Using size limit from environment variable: {limit_mb} MB.")
        except ValueError:
            # Handle cases where the environment variable is not a valid integer
            print(f"[Warning] Environment variable 'CLEANUP_LIMIT_MB' is not an integer. Using default {DEFAULT_SIZE_LIMIT_MB} MB.")
            limit_mb = DEFAULT_SIZE_LIMIT_MB
    else:
        print(f"[Info] Environment variable 'CLEANUP_LIMIT_MB' not set. Using default {DEFAULT_SIZE_LIMIT_MB} MB.")

    # Conversion: MB to Bytes (1024 * 1024)
    return limit_mb * 1024 * 1024

def scan_directory(target_dir, extension, size_limit_bytes):
    """
    Scans the directory for files matching the extension and exceeding the size limit.
    """
    print(f"\nScanning directory: {target_dir} for *.{extension} files > {size_limit_bytes / (1024*1024):.2f} MB...")
    
    found_files = []
    total_size = 0
    
    # Use os.listdir to get all entries (files and directories) in the target directory
    try:
        directory_contents = os.listdir(target_dir)
    except OSError as e:
        print(f"[Fatal Error] Could not access directory {target_dir}: {e}")
        # Use sys.exit to immediately terminate execution upon critical failure
        sys.exit(1)


    for item_name in directory_contents:
        # Construct the full path using os.path.join for cross-platform compatibility
        full_path = os.path.join(target_dir, item_name)
        
        # Check if the path points to a regular file using os.path.isfile
        if os.path.isfile(full_path):
            # Check if the file extension matches the required extension
            # Note: We convert both sides to lowercase for case-insensitive matching
            if item_name.lower().endswith(f".{extension.lower()}"):
                
                # Get the size of the file using os.path.getsize
                file_size = os.path.getsize(full_path)
                
                # Check if the file exceeds the defined limit
                if file_size > size_limit_bytes:
                    found_files.append((full_path, file_size))
                    total_size += file_size
                    
    return found_files, total_size

# --- Main Execution Block ---
if __name__ == "__main__":
    
    display_system_info()
    
    # 1. Check command-line arguments using sys.argv
    if len(sys.argv) != REQUIRED_ARGS:
        # os.path.basename extracts the script name regardless of how it was executed
        script_name = os.path.basename(sys.argv[0])
        print(f"\n[Error] Usage: python {script_name} <Directory Path> <File Extension>")
        print(f"Example: python {script_name} /home/user/logs log")
        # Exit the program gracefully using sys.exit(1) to signal an error state
        sys.exit(1)
        
    # Extract arguments
    target_path = sys.argv[1]
    file_ext = sys.argv[2]
    
    # 2. Validate the path using os.path functions
    if not os.path.isdir(target_path):
        print(f"\n[Error] Specified path is not a valid directory or does not exist: {target_path}")
        sys.exit(1)
        
    # 3. Determine the size limit using environment variables
    limit_bytes = get_size_limit_bytes()
    
    # 4. Perform the scan
    large_files, total_size_bytes = scan_directory(target_path, file_ext, limit_bytes)
    
    # 5. Report results
    if large_files:
        print("\n--- Large Files Report ---")
        for path, size in large_files:
            # Format size for readability
            size_mb = size / (1024 * 1024)
            print(f"Found: {path} ({size_mb:.2f} MB)")
            
        total_mb = total_size_bytes / (1024 * 1024)
        print(f"\nSummary: {len(large_files)} files found, totaling {total_mb:.2f} MB.")
    else:
        print("\nScan complete. No files found matching criteria.")
        
    # Standard exit code 0 indicates successful execution
    sys.exit(0)

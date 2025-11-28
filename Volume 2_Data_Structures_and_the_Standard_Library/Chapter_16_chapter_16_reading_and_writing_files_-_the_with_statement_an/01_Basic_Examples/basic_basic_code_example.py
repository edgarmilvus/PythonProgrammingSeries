
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
import sys

# 1. Define the file name globally
FILE_NAME = "chapter_16_notes.txt"
content_to_write = [
    "Configuration Note 1: The 'with' statement is essential for safety.",
    "Configuration Note 2: Mode 'w' means write and overwrite.",
    "Configuration Note 3: Mode 'r' means read only.",
    "Configuration Note 4: Remember to handle newline characters ('\\n')."
]

# --- PART 1: WRITING DATA using 'w' mode ---
print(f"--- 1. Attempting to write data to {FILE_NAME} ---")

try:
    # The 'with' statement handles opening and guaranteed closing.
    # 'w' mode opens the file for writing. If it exists, its content is truncated (deleted).
    with open(FILE_NAME, 'w') as file_writer:
        
        # Write each line from the list into the file
        for index, line in enumerate(content_to_write):
            # We must manually append '\n' to ensure each item occupies a new line in the file
            file_writer.write(f"[{index + 1}] {line}\n")
    
    # Execution leaves the 'with' block, and the file is automatically closed here.
    print(f"Successfully wrote {len(content_to_write)} lines and closed the file.")

except IOError as e:
    # IOError catches issues like permission denied or disk full
    print(f"CRITICAL ERROR during writing: {e}")
    sys.exit(1) # Exit the script if the write operation fails

# --- PART 2: READING DATA using 'r' mode ---
print(f"\n--- 2. Attempting to read data from {FILE_NAME} ---")
read_content = []

try:
    # 'r' mode opens the file for reading (this is the default mode).
    with open(FILE_NAME, 'r') as file_reader:
        
        # Iterating directly over the file object is the most memory-efficient way
        for line in file_reader:
            # .strip() removes leading/trailing whitespace, including the '\n' character
            read_content.append(line.strip())
    
    # Execution leaves the 'with' block, and the file is automatically closed here.
    print("Successfully read all content and closed the file.")
    
    # Display the content we read
    print("\n--- Displaying Read Content ---")
    for item in read_content:
        print(f"-> {item}")

except FileNotFoundError:
    # Catches the specific error if the file doesn't exist
    print(f"FATAL ERROR: The file {FILE_NAME} was not found.")
    sys.exit(1)

# --- PART 3: CLEANUP ---
# Clean up the generated file for subsequent runs
if os.path.exists(FILE_NAME):
    os.remove(FILE_NAME)
    print(f"\n--- 3. Cleanup: Deleted the file {FILE_NAME}. ---")

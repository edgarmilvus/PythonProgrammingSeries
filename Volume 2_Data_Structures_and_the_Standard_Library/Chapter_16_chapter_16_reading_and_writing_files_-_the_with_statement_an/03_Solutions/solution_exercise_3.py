
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

import os

RAW_FILE = "raw_data.txt"
CLEAN_FILE = "clean_data.txt"

# --- 1. Input Setup ---
dummy_data = """
user one
    
    USER TWO
    
user three    
four
"""
# Create the raw input file
with open(RAW_FILE, 'w') as f:
    f.write(dummy_data.strip())
    
# Initialize list to hold sanitized data
clean_lines = []

# --- 2. Phase 1: Reading and Transformation ---
print(f"Reading from {RAW_FILE} and sanitizing data...")
try:
    # Safely open the input file in read mode ('r')
    with open(RAW_FILE, 'r') as infile:
        for line in infile:
            # Step 1: Strip leading/trailing whitespace
            processed_line = line.strip()
            
            # Step 2: Convert to uppercase
            processed_line = processed_line.upper()
            
            # Step 3: Requirement - Only keep non-empty lines
            if processed_line:
                clean_lines.append(processed_line)

except FileNotFoundError:
    print(f"Error: Input file {RAW_FILE} not found.")
    exit()

# --- 3. Phase 2: Writing Output ---
print(f"Writing {len(clean_lines)} clean entries to {CLEAN_FILE}...")
try:
    # Safely open the output file in write mode ('w') to ensure it's fresh
    with open(CLEAN_FILE, 'w') as outfile:
        # Write all processed lines, separated by a newline
        # Adding a final newline ensures consistency
        outfile.write('\n'.join(clean_lines) + '\n')

except IOError as e:
    print(f"Error writing output file: {e}")

print("Pipeline complete. Verification of clean data:")
# Verification read
with open(CLEAN_FILE, 'r') as f:
    print(f.read())

# Clean up files
# os.remove(RAW_FILE)
# os.remove(CLEAN_FILE)

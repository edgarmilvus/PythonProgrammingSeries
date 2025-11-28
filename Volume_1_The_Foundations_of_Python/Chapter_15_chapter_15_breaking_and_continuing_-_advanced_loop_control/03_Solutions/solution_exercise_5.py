
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

print("\n--- Exercise 5: Nested Loop Control: The Matrix Search ---")

matrix = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]
TARGET = 50

# Requirement 3: Use a Boolean flag
found_flag = False
found_r = -1
found_c = -1

print(f"Searching for target: {TARGET} in the 3x3 matrix.")

# Outer loop (Rows)
for r in range(len(matrix)):
    
    # Inner loop (Columns)
    for c in range(len(matrix[r])):
        
        if matrix[r][c] == TARGET:
            # Requirement 4a: Set flag
            found_flag = True
            found_r = r
            found_c = c
            
            # Requirement 4b: Break inner (column) loop
            break 
            
    # Requirement 5: Check flag after inner loop completes
    if found_flag:
        # Break outer (row) loop
        break

# Final output
if found_flag:
    print(f"Target {TARGET} found and search terminated successfully.")
    print(f"Coordinates: Row {found_r}, Column {found_c}")
else:
    # This block executes if the outer loop completed without finding the target
    print(f"Target {TARGET} not found after exhaustive search.")

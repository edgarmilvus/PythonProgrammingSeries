
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

# Exercise 5: Scope and Debugging (The UnboundLocalError)

# 1. Global variable
error_count = 0

def log_error_broken():
    """
    Attempts to increment the global error_count without 'global', 
    leading to UnboundLocalError.
    """
    # 2. The compound assignment operator (+=) implies assignment, 
    # marking 'error_count' as local.
    # Python then attempts to READ the local 'error_count' to perform the addition 
    # (error_count = error_count + 1).
    # Since the local 'error_count' has not yet been assigned a value, it fails.
    print("Attempting to log error...")
    error_count += 1 
    print(f"Local error count: {error_count}")

# 3. If you uncomment the line below, the program will crash:
# log_error_broken() 
# Output: UnboundLocalError: local variable 'error_count' referenced before assignment

# 5. Explanation of the Error:
"""
The UnboundLocalError occurs because the assignment operator (+=) tells Python
that 'error_count' is intended to be a local variable within 'log_error_broken'.
However, since compound assignment (like +=) requires reading the variable's
current value before performing the operation, Python attempts to read the 
local 'error_count'. Since it has not yet been assigned a value in the local 
scope, the interpreter raises an UnboundLocalError. This is different from 
simple assignment (e.g., error_count = 1), which would cause silent shadowing 
(Exercise 1).
"""

# 6. Fix the function
def log_error_fixed():
    """
    Correctly increments the global error_count using the global keyword.
    """
    global error_count
    error_count += 1
    print(f"Error logged successfully. Global count is now: {error_count}")

# Test the fixed function
print("\n--- Testing Fixed Function ---")
log_error_fixed()
log_error_fixed()
log_error_fixed()

print(f"Final Global error_count: {error_count}")

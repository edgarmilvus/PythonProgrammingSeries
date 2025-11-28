
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

# Exercise 1: The Global Read vs. The Local Write

# 1. Define the global variable
MAX_ATTEMPTS = 5

def check_attempts():
    """Reads and prints the global attempt count."""
    # Python looks up and finds the global MAX_ATTEMPTS (5)
    print(f"Current attempts remaining (Global scope): {MAX_ATTEMPTS}")

def decrement_attempt():
    """Attempts to decrement the global variable without using 'global'."""
    # 3. This assignment operator tells Python to create a NEW local variable 
    # named MAX_ATTEMPTS inside this function's scope.
    # This local variable SHADOWS the global one.
    MAX_ATTEMPTS = 4
    print(f"Attempts inside function (Local scope): {MAX_ATTEMPTS}")
    # When the function exits, this local variable (4) is destroyed.

# Execution sequence
print("--- Initial Check ---")
check_attempts() # Output: 5

print("\n--- Running Decrement Function ---")
decrement_attempt() # Output: 4 (Local value)

print("\n--- Final Check ---")
check_attempts() # Output: 5 (Global value is unchanged)

# 5. Explanation:
# The final output of MAX_ATTEMPTS remains 5 because the 'decrement_attempt'
# function did not modify the global variable. When Python encountered the 
# assignment (MAX_ATTEMPTS = 4) inside the function, it defaulted to creating 
# a brand new variable named MAX_ATTEMPTS that existed only within 
# the local scope of that function. The global variable was merely shadowed, 
# not modified.

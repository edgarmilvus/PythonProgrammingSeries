
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

# Exercise 2 Solution
print("--- Exercise 2: Data Integrity Check and Value Error Handling ---")

def get_max_retries(input_string):
    """
    Attempts to convert an input string into an integer for a retry count.
    If conversion fails (ValueError), it returns a default value (3).
    """
    try:
        # Attempt the explicit type conversion using int()
        retries = int(input_string)
        print(f"SUCCESS: Converted '{input_string}' to integer {retries}.")
        return retries
    except ValueError:
        # Catch the specific error raised when conversion fails (e.g., "ten" or "4.0")
        print(f"ERROR: Cannot convert '{input_string}' to an integer.")
        print("Defaulting Maximum Retries to 3.")
        return 3

# Test Cases
print("\n--- Test Case 1: Valid Integer ---")
result_1 = get_max_retries("7")

print("\n--- Test Case 2: Invalid Text ---")
result_2 = get_max_retries("ten")

print("\n--- Test Case 3: Float String (Causes ValueError for int()) ---")
result_3 = get_max_retries("4.0")

print(f"\nFinal Results: 1: {result_1}, 2: {result_2}, 3: {result_3}")

print("-" * 50)

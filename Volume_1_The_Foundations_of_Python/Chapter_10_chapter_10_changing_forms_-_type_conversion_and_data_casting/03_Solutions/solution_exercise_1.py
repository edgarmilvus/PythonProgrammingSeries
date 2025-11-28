
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

# Exercise 1 Solution
print("--- Exercise 1: The Robust Arithmetic Calculator ---")

try:
    # 1. Prompt and receive user input (always strings initially)
    num_a_str = input("Enter the first number (A): ")
    num_b_str = input("Enter the second number (B): ")
    operation = input("Enter the operation symbol (+, -, *, /): ")

    # 3. Explicitly cast input strings to float types
    num_a = float(num_a_str)
    num_b = float(num_b_str)

    result = None

    # 4. Use if/elif/else structure for calculation
    if operation == '+':
        result = num_a + num_b
    elif operation == '-':
        result = num_a - num_b
    elif operation == '*':
        result = num_a * num_b
    elif operation == '/':
        # Handle division by zero
        if num_b == 0:
            print("Error: Division by zero is not allowed.")
            result = "UNDEFINED"
        else:
            result = num_a / num_b
    else:
        print(f"Error: Invalid operation symbol '{operation}' entered.")
        result = "N/A"

    # 5. Print the final result clearly using an f-string
    if result != "N/A" and result != "UNDEFINED":
        print(f"\nCalculation Result: {num_a} {operation} {num_b} = {result}")
    
except ValueError:
    # Catch error if the user inputs non-numeric characters
    print("\nInput Error: Please ensure you enter valid numerical values for the numbers.")

print("-" * 50)

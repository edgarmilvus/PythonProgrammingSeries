
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

# Interactive Challenge Solution Structure
print("--- Simple Interactive Calculator ---")

while True:
    user_input = input("Enter operation (add, sub, quit): ").strip().lower()

    if user_input == 'quit':
        print("Exiting calculator.")
        break

    # 1. Input Validation and Error Handling using try/except and continue
    try:
        # Attempt to convert input to float. This is where ValueError can occur.
        num_a = float(input("Enter first number: "))
        num_b = float(input("Enter second number: "))
        
    except ValueError:
        # If conversion fails (e.g., user typed 'x'), catch the error
        print("Error: Please enter only valid numeric values for calculations.")
        
        # Use continue to skip the calculation logic below and restart the loop
        continue 

    # 2. Calculation Logic
    result = None
    if user_input == 'add':
        result = num_a + num_b
    elif user_input == 'sub':
        result = num_a - num_b
    else:
        print(f"Unknown operation: {user_input}. Try again.")
        continue # Unknown command also skips output

    # 3. Output
    if result is not None:
        print(f"Result: {result}\n")

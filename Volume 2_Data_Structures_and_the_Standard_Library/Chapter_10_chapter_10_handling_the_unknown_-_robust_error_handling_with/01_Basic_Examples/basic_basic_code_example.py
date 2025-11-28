
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

# Example 10.2: Simple Robust Division Calculator

def safe_divide():
    """Attempts to perform division based on user input, handling common errors."""

    print("--- Safe Division Utility Initialized ---")
    result = None  # Initialize result outside the try block

    # 1. The try block contains the code that is prone to exceptions.
    try:
        # Get the numerator input (Input conversion might raise ValueError)
        numerator_str = input("Enter the numerator (number): ")
        # Get the denominator input (Input conversion might raise ValueError)
        denominator_str = input("Enter the denominator (number): ")

        # Convert inputs to float (This is the first potential failure point)
        numerator = float(numerator_str)
        denominator = float(denominator_str)

        # Perform the division (This is the second potential failure point: ZeroDivisionError)
        result = numerator / denominator

    # 2. Specific exception handler: Catches errors when conversion to float fails.
    except ValueError:
        print("\n[ERROR] Invalid Input Type: Please ensure both inputs are valid numerical values (e.g., 10 or 3.14).")
        print("The division operation could not be attempted.")

    # 3. Specific exception handler: Catches the error when dividing by zero.
    except ZeroDivisionError:
        print("\n[ERROR] Mathematical Impossibility: Division by zero is undefined.")
        print("Please choose a non-zero denominator for the calculation.")

    # 4. The optional 'else' block executes ONLY if the 'try' block completes without raising any exception.
    else:
        # Since 'result' was successfully calculated, we can confidently print it here.
        print(f"\n[SUCCESS] Operation completed successfully.")
        print(f"Result: {numerator} / {denominator} = {result}")

    # 5. The optional 'finally' block executes regardless of whether an exception occurred or not.
    finally:
        print("\n--- Division Attempt Concluded. Cleaning up resources. ---")

# Execute the function to run the utility
safe_divide()

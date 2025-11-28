
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

def safe_calculate(num1_str, num2_str, op):
    """
    Safely performs arithmetic operations, handling ValueErrors and ZeroDivisionErrors.
    """
    try:
        # Attempt to convert string inputs to floats (can raise ValueError)
        num1 = float(num1_str)
        num2 = float(num2_str)

        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            # Division operation (can raise ZeroDivisionError if num2 is 0)
            result = num1 / num2
        else:
            # If the operator is unknown, raise TypeError as requested
            raise TypeError("Unsupported operator symbol.")

    except ValueError:
        # Catches errors from float() conversion (e.g., input is "ten")
        return "Error: Input must be a valid number."
    except ZeroDivisionError as e:
        # Catches division by zero
        return f"Calculation Error: Cannot divide by zero. Details: {e}"
    except TypeError as e:
        # Catches unsupported operator
        return f"Operation Error: {e}"
    except Exception as e:
        # Catch any other unexpected error
        return f"An unexpected error occurred: {e}"

    # Return the result if the try block succeeded
    return result

# Example tests
# print(safe_calculate("10", "2", "/"))
# print(safe_calculate("ten", "2", "+"))
# print(safe_calculate("10", "0", "/"))
# print(safe_calculate("10", "2", "%"))

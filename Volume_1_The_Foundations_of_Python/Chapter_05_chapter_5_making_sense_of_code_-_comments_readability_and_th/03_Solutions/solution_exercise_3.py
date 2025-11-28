
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

def is_leap_year_complex(y):
    # This implementation is unnecessarily complex and hard to follow
    if y % 4 == 0:
        if y % 100 == 0:
            if y % 400 == 0:
                result = True
            else:
                result = False
        else:
            result = True
    else:
        result = False
    return result


def is_leap_year_simple(year: int) -> bool:
    """
    Determines if a given year is a leap year using a concise boolean expression.
    
    The rules are: 
    (Divisible by 4 AND NOT divisible by 100) OR (Divisible by 400).

    This adheres to the Zen of Python: "Simple is better than complex."
    """
    # Use a single return statement with logical operators for maximum clarity.
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Testing and Verification
print("--- Leap Year Test Results ---")
print(f"Year 2000 (Expected: True): Simple={is_leap_year_simple(2000)}")
print(f"Year 1900 (Expected: False): Simple={is_leap_year_simple(1900)}")
print(f"Year 2024 (Expected: True): Simple={is_leap_year_simple(2024)}")
print(f"Year 2023 (Expected: False): Simple={is_leap_year_simple(2023)}")

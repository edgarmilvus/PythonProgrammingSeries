
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

def calculate_perimeter(width, height):
    """
    Calculates the perimeter of a rectangle given its width and height.

    Parameters:
        width (float or int): The width of the rectangle.
        height (float or int): The height of the rectangle.

    Returns:
        float or int: The calculated perimeter.
    """
    # Calculation: P = 2 * (width + height)
    perimeter = 2 * (width + height)
    return perimeter

# --- Testing the Function ---
print("--- Exercise 1: Perimeter Calculator ---")

# Test Case 1: Integers (5 and 10)
w1, h1 = 5, 10
result1 = calculate_perimeter(w1, h1)
print(f"Perimeter for width={w1}, height={h1}: {result1}")

# Test Case 2: Floats (7.5 and 3)
w2, h2 = 7.5, 3
result2 = calculate_perimeter(w2, h2)
print(f"Perimeter for width={w2}, height={h2}: {result2}")

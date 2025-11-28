
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

# Exercise 4 Solution
print("--- Exercise 4: Precision Loss and Truncation ---")

# 1. Define variables
pi_estimate = 3.14159
almost_four = 3.99999

# 3. Explicitly cast floats to integers using int()
int_pi = int(pi_estimate)
int_four = int(almost_four)

# 4. Print the results
print(f"Original float (pi_estimate): {pi_estimate}")
print(f"Converted integer (int_pi):   {int_pi}")
print("-" * 20)
print(f"Original float (almost_four): {almost_four}")
print(f"Converted integer (int_four): {int_four}")

# 5. Explanation
print("\nExplanation:")
print("Both converted integers are 3 because the int() function,")
print("when converting from a float, performs strict truncation.")
print("It simply discards the fractional part (the digits after the decimal point),")
print("regardless of how close the float is to the next whole number.")

print("-" * 50)

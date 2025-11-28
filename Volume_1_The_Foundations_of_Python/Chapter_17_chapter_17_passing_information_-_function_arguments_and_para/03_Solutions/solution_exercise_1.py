
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

def calculate_volume(length, width, height):
    """
    Calculates the volume of a three-dimensional space.

    Args:
        length (float): The length dimension.
        width (float): The width dimension.
        height (float): The height dimension.

    Returns:
        float: The total calculated volume.
    """
    return length * width * height

# 3. Positional Call (Correct Order)
L_correct, W_correct, H_correct = 10, 5, 2
volume_correct = calculate_volume(L_correct, W_correct, H_correct)
print(f"1. Correct Positional Call (L={L_correct}, W={W_correct}, H={H_correct}): {volume_correct}")

# 4. Positional Call (Incorrect Logical Order)
# We intentionally swap width and height in the argument list (5, 2 -> 2, 5)
L_incorrect, W_incorrect, H_incorrect = 10, 2, 5
volume_incorrect = calculate_volume(L_incorrect, W_incorrect, H_incorrect)
print(f"2. Incorrect Positional Call (L={L_incorrect}, W={W_incorrect}, H={H_incorrect}): {volume_incorrect}")
print("# Note: The mathematical result is the same (100), but Python accepted L=10, W=2, H=5, which might be logically confusing if the caller intended W=5 and H=2.")

# 5. Keyword Call (Clarity and Mixed Order)
# Keywords explicitly link the argument value to the parameter name, ignoring position.
volume_keyword = calculate_volume(height=2, length=10, width=5)
print(f"3. Keyword Call (Mixed Order: H=2, L=10, W=5): {volume_keyword}")
print("# Note: Keywords ensure clarity regardless of the order they are provided.")

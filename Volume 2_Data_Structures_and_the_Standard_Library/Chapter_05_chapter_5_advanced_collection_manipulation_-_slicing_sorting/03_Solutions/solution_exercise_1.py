
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

import re

def is_palindrome(text: str) -> bool:
    """
    Checks if a given string is a palindrome, ignoring case and non-alphanumeric characters.

    Args:
        text: The input string to check.

    Returns:
        True if the filtered string is a palindrome, False otherwise.
    """
    # 1. Preprocessing and Filtering:
    # Convert to lowercase first.
    # Use a generator expression combined with str.isalnum() to filter out non-alphanumeric characters.
    cleaned_text = "".join(char for char in text.lower() if char.isalnum())

    # 2. Slicing Implementation:
    # Compare the cleaned string with its reverse, obtained via the [::-1] slice step.
    return cleaned_text == cleaned_text[::-1]

# --- Test Cases ---
print("--- Exercise 1 Results ---")
test_cases = [
    ("Racecar", True),
    ("Hello, World!", False),
    ("Madam, I'm Adam", True),
    ("12321", True),
    ("A man, a plan, a canal: Panama", True),
    ("Python", False)
]

for input_text, expected in test_cases:
    result = is_palindrome(input_text)
    print(f"Input: '{input_text}' -> Result: {result} (Expected: {expected})")


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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

def check_palindrome(phrase):
    """
    Checks if a given phrase is a palindrome by normalizing (lowercase, no spaces) 
    and reversing the resulting string using slicing.
    """
    
    # 1. Normalization: Convert to lowercase and remove spaces
    # This ensures "Racecar" and "racecar" are treated identically.
    normalized_phrase = phrase.lower().replace(" ", "")
    
    # 2. Reversal using slicing [::-1]
    # The step value of -1 reverses the entire sequence.
    reversed_phrase = normalized_phrase[::-1]
    
    # 3. Comparison and Reporting
    print(f"\n--- Palindrome Analysis for '{phrase}' ---")
    print(f"Normalized String: {normalized_phrase}")
    print(f"Reversed String:   {reversed_phrase}")
    
    if normalized_phrase == reversed_phrase:
        # Use f-string for clear final report
        print(f"RESULT: Yes, '{phrase}' is a PALINDROME.")
        return True
    else:
        print(f"RESULT: No, '{phrase}' is NOT a palindrome.")
        return False

# Test Cases
check_palindrome("Racecar")
check_palindrome("A man a plan a canal Panama")
check_palindrome("Python")
check_palindrome("Level")

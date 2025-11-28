
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

def count_vowels(text):
    """
    Counts the total number of vowels (A, E, I, O, U) in a given string, 
    ignoring case, using sequence iteration.
    """
    vowels = 'aeiou'
    vowel_count = 0
    
    # 1. Convert the entire input string to lowercase for case insensitivity
    text_lower = text.lower()
    
    # 2. Iterate through every character in the processed string
    for char in text_lower:
        # 3. Check if the character is present in the defined set of vowels
        if char in vowels:
            vowel_count += 1
            
    # 4. Return the final accumulated count
    return vowel_count

# Sample Usage and Verification
print("--- Exercise 1: Universal Vowel Counter ---")
print(f"Input 'Programming is fun': {count_vowels('Programming is fun')}")  # Expected: 5
print(f"Input 'AEIOUaeiou': {count_vowels('AEIOUaeiou')}")              # Expected: 10
print(f"Input 'Rhythm': {count_vowels('Rhythm')}")                      # Expected: 0

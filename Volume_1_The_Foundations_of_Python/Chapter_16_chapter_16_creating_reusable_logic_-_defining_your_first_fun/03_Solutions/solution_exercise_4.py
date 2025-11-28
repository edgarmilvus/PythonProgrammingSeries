
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

def is_valid_input(input_string):
    """
    Checks if an input string meets specific criteria for length, 
    spaces, and forbidden characters.

    Parameters:
        input_string (str): The string to be validated.

    Returns:
        bool: True if the string is valid, False otherwise.
    """
    
    # 1. Length Check (Guard Clause)
    # The string must be longer than 8 characters.
    if len(input_string) <= 8:
        # print("Validation failed: Too short.") # Optional debug print
        return False
        
    # 2. Space Check (Guard Clause)
    # The 'in' operator checks for the presence of a space character.
    if " " in input_string:
        # print("Validation failed: Contains spaces.") # Optional debug print
        return False
        
    # 3. Forbidden Character Check (Guard Clause)
    # Define the set of characters that are not allowed.
    forbidden_chars = "!@$%"
    
    # Iterate through each character of the input string
    for char in input_string:
        # Check if the current character is in the forbidden set
        if char in forbidden_chars:
            # print(f"Validation failed: Contains forbidden character '{char}'.") # Optional debug print
            return False
            
    # 4. Success Condition
    # If the code reaches this point, all checks have passed.
    return True

# --- Testing the Function ---
print("\n--- Exercise 4: Data Validator Results ---")

test_cases = [
    "short",                # Fails: Length (<= 8)
    "valid_name_123",       # Passes
    "name with space",      # Fails: Space
    "name!with_symbol",      # Fails: Forbidden character '!'
    "PerfectlyValidName"    # Passes
]

for test_input in test_cases:
    result = is_valid_input(test_input)
    print(f"Input: '{test_input}' -> Valid: {result}")

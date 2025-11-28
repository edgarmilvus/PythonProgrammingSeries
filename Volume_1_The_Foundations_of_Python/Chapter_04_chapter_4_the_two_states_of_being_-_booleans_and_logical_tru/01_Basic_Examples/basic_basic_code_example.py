
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

# --- Age Verification Logic ---

# 1. Define the minimum required age for access.
# Using all caps signifies this value is intended to be a constant.
MINIMUM_AGE = 18

# 2. Define the first user's current age.
user_age_1 = 22

# 3. Generate the Boolean value using the comparison operator (>=).
# Python evaluates the relationship: Is 22 greater than or equal to 18?
is_eligible_1 = user_age_1 >= MINIMUM_AGE

# 4. Output the results for the first user.
print("--- User 1 Check ---")
print(f"User Age: {user_age_1}")
print(f"Is User 1 eligible? {is_eligible_1}")
print(f"Data Type of Result: {type(is_eligible_1)}")

# 5. Define a second user's age for a demonstration of a False result.
user_age_2 = 16

# 6. Generate the Boolean value for the second user.
# Python evaluates the relationship: Is 16 greater than or equal to 18?
is_eligible_2 = user_age_2 >= MINIMUM_AGE

# 7. Output the results for the second user.
print("\n--- User 2 Check ---")
print(f"User Age: {user_age_2}")
print(f"Is User 2 eligible? {is_eligible_2}")


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

# --- Scenario: Checking eligibility for a special movie ticket discount ---

# 1. Define the input conditions using variables
# We set initial values to simulate a specific user's profile.
user_age = 22
is_student = True
has_loyalty_card = False

# 2. Use the 'and' operator (Both conditions must be True)
# Rule: The youth discount requires the user to be under 25 AND currently a student.
# The comparison (user_age < 25) evaluates to True (22 < 25).
is_eligible_for_youth_discount = (user_age < 25) and is_student

# 3. Use the 'or' operator (At least one condition must be True)
# Rule: A user can get *some* discount if they qualify for the youth discount OR if they have a loyalty card.
# This demonstrates combining the result of a complex check (youth discount) with a simple check (loyalty card).
can_get_any_discount = is_eligible_for_youth_discount or has_loyalty_card

# 4. Use the 'not' operator (Inverts the condition)
# Check the inverse: Is the user NOT eligible for the youth discount?
is_not_youth_eligible = not is_eligible_for_youth_discount

# 5. Output the results clearly using f-strings
print("--- Movie Discount Eligibility Report ---")
print(f"User Age: {user_age}")
print(f"Is Student: {is_student}")
print(f"Has Loyalty Card: {has_loyalty_card}")
print("-" * 40)

print(f"1. Eligible for Youth Discount (Age < 25 AND Student): {is_eligible_for_youth_discount}")
print(f"2. Can Get Any Discount (Youth OR Loyalty Card): {can_get_any_discount}")
print(f"3. Is NOT Youth Eligible: {is_not_youth_eligible}")


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

# ----------------------------------------------------------------------
# Section 1: Setup
# ----------------------------------------------------------------------

# We define the variable holding the user's age.
# This variable uses the Integer (int) data type.
user_age = 19

# ----------------------------------------------------------------------
# Section 2: Conditional Logic Chain (if/elif/else)
# ----------------------------------------------------------------------

# 1. The initial 'if' statement is the first condition checked.
# We check if the age is less than the minimum threshold (e.g., 16).
if user_age < 16:
    # This block executes only if the condition (user_age < 16) is True.
    print("You are under 16. You are only eligible for school activities.")

# 2. The 'elif' (Else If) statement checks the next condition,
# but only if the preceding 'if' (or 'elif') was False.
# Check for eligibility for a driving permit (16 to 17).
elif user_age >= 16 and user_age < 18:
    # This block executes if the user is 16 or 17.
    print("You are eligible for a learner's driving permit.")

# 3. Another 'elif' handles the next major threshold.
# Check for voting eligibility (18 to 20).
elif user_age >= 18 and user_age < 21:
    # This block executes if the user is 18, 19, or 20.
    print("Congratulations! You are eligible to vote and join the military.")

# 4. The 'else' statement is the final, catch-all block.
# It executes only if ALL preceding 'if' and 'elif' conditions were False.
else:
    # If the user is not under 16, not 16-17, and not 18-20, they must be 21 or older.
    print("You are 21 or older. You have full adult privileges, including purchasing alcohol.")

# ----------------------------------------------------------------------
# Section 3: Program Conclusion
# ----------------------------------------------------------------------
print("Program execution complete.")

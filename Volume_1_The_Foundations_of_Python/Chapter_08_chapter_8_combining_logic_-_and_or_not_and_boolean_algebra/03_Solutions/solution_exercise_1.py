
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

# Exercise 8-1: The Enrollment Eligibility Checker

# --- Student A Data ---
age_a = 22
has_stats_a = True
has_discrete_math_a = False
gpa_a = 3.2

print("--- Checking Student A Eligibility ---")

# Requirement 1: DSF Eligibility (Age >= 18 AND has_stats)
is_eligible_dsf_a = (age_a >= 18) and has_stats_a

# Requirement 2: AA Eligibility (has_discrete_math OR GPA > 3.5)
is_eligible_aa_a = has_discrete_math_a or (gpa_a > 3.5)

# Conditional output based on eligibility
if is_eligible_dsf_a and is_eligible_aa_a:
    print("Student A is eligible for both Data Science Fundamentals and Advanced Algorithms.")
elif is_eligible_dsf_a:
    print("Student A is eligible for Data Science Fundamentals.")
elif is_eligible_aa_a:
    print("Student A is eligible for Advanced Algorithms.")
else:
    # General Warning if eligible for neither
    print("Student A is not eligible for any advanced course at this time.")

# --- Student B Data ---
age_b = 17
has_stats_b = False
has_discrete_math_b = True
gpa_b = 3.8

print("\n--- Checking Student B Eligibility ---")

# Requirement 1: DSF Eligibility (17 >= 18 is False)
is_eligible_dsf_b = (age_b >= 18) and has_stats_b

# Requirement 2: AA Eligibility (True OR 3.8 > 3.5 is True)
is_eligible_aa_b = has_discrete_math_b or (gpa_b > 3.5)

# Conditional output for Student B
if is_eligible_dsf_b and is_eligible_aa_b:
    print("Student B is eligible for both Data Science Fundamentals and Advanced Algorithms.")
elif is_eligible_dsf_b:
    print("Student B is eligible for Data Science Fundamentals.")
elif is_eligible_aa_b:
    print("Student B is eligible for Advanced Algorithms.")
else:
    print("Student B is not eligible for any advanced course at this time.")

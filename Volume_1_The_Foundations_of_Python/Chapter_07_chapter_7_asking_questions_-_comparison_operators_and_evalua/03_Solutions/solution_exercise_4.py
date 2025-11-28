
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

# Exercise 7.4.4 Setup: Enhancing the Eligibility Engine

# 1. Applicant Data
applicant_age = 35
applicant_income = 65000
applicant_credit_score = 720
applicant_dti_ratio = 0.41  # Test value: 0.41 (Disqualified)

# 2. Thresholds
MIN_AGE = 21
MIN_INCOME = 50000
MIN_CREDIT = 680
MAX_DTI = 0.40

# 3. Original Eligibility Checks
age_ok = (applicant_age >= MIN_AGE)
income_ok = (applicant_income >= MIN_INCOME)
credit_ok = (applicant_credit_score >= MIN_CREDIT)

# Combine original positive criteria (All True in this case)
original_criteria_met = (age_ok and income_ok and credit_ok)

# 4. New Disqualification Check
# DTI >= 0.40 means True (Disqualified)
is_disqualified_by_dti = (applicant_dti_ratio >= MAX_DTI)

# 5. Recalculate Final Eligibility
# Must meet positive criteria AND NOT meet the disqualification criteria.
is_eligible = original_criteria_met and (not is_disqualified_by_dti)

# 6. Print Result
print(f"Original criteria met (Age, Income, Credit): {original_criteria_met}")
print(f"Disqualified by DTI (DTI >= {MAX_DTI}): {is_disqualified_by_dti}")
print(f"Final Eligibility: {is_eligible}")

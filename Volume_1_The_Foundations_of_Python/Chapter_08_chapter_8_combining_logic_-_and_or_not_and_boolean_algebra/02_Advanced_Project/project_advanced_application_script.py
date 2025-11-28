
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

# Loan Eligibility System: Complex Conditional Assessment
# This script processes applicant data against a predefined set of financial rules.

# --- 1. System Constants (Defining the Policy Rules) ---
# These variables define the hard requirements for eligibility.
MIN_AGE = 18
MAX_DEBT_LOAD = 2
STANDARD_MIN_SCORE = 650
STANDARD_MIN_INCOME = 40000.00
CRITICAL_LOW_SCORE_CUTOFF = 550 # Absolute minimum for any consideration

# Exception Rules
STUDENT_EXCEPTION_SCORE = 600 # Lower score allowed for verified students
FIRST_TIME_EXCEPTION_INCOME = 30000.00 # Lower income allowed for first-time applicants

# --- 2. Applicant Data (Simulated Input) ---
# In a real system, this data would come from user input or a database.
applicant_name = "Elara Vance"
applicant_age = 25
applicant_income = 45000.00
applicant_credit_score = 680
applicant_existing_loans = 1
applicant_is_student = False
applicant_is_first_time = True

# --- 3. Initial Status Variables ---
# These Booleans track the success of different checks throughout the process.
is_age_eligible = False
is_financial_eligible = False
is_debt_acceptable = False
final_eligibility_status = False
rejection_reason = "N/A"

print(f"--- Processing Application for: {applicant_name} ---")

# 4. Step 1: Basic Age Check (Immediate rejection if too young)
# The 'not' operator is used here to trigger an early exit for the most basic failure.
is_age_eligible = (applicant_age >= MIN_AGE)

if not is_age_eligible:
    rejection_reason = "Applicant is below the minimum age requirement."
    print(f"Status: REJECTED (Reason: {rejection_reason})")
else:
    # If age passes, proceed to the next nested check.

    # 5. Step 2: Automatic Rejection Check (Using 'or' for multiple fatal flaws)
    # Check if the applicant has too many existing loans OR a critically low score.
    is_debt_acceptable = (applicant_existing_loans <= MAX_DEBT_LOAD)
    is_critically_low_score = (applicant_credit_score < CRITICAL_LOW_SCORE_CUTOFF) 

    # If the debt is NOT acceptable OR the score is critically low, reject.
    if (not is_debt_acceptable) or is_critically_low_score:
        
        # Determine the specific rejection message for clarity.
        if not is_debt_acceptable:
            rejection_reason = "Exceeds maximum allowable concurrent loans."
        elif is_critically_low_score:
            rejection_reason = "Credit score is critically low (below 550)."
        
        print(f"Status: REJECTED (Reason: {rejection_reason})")
        
    else:
        # If debt and critical score pass, proceed to financial assessment.

        # 6. Step 3: Standard Financial Check (Using 'and' for simultaneous requirements)
        # Applicant must meet standard income AND standard credit score requirements.
        standard_criteria_met = (applicant_income >= STANDARD_MIN_INCOME) and \
                                (applicant_credit_score >= STANDARD_MIN_SCORE)
        
        if standard_criteria_met:
            is_financial_eligible = True
            rejection_reason = "N/A - Standard Criteria Met."
            
        else:
            # 7. Step 4: Exception Handling (Complex 'and' and 'or' combination)
            # If standard criteria fail, check if they qualify via special exception.
            
            # Exception 1: Student Status Check
            # Requires being a student AND meeting the lower score AND meeting lower income.
            student_exception_ok = applicant_is_student and \
                                   (applicant_credit_score >= STUDENT_EXCEPTION_SCORE) and \
                                   (applicant_income >= FIRST_TIME_EXCEPTION_INCOME)
            
            # Exception 2: First-Time Applicant Check
            # Requires being first-time AND meeting the lower income AND meeting the standard score.
            first_time_exception_ok = applicant_is_first_time and \
                                      (applicant_income >= FIRST_TIME_EXCEPTION_INCOME) and \
                                      (applicant_credit_score >= STANDARD_MIN_SCORE)
            
            # Combine exceptions using 'or'. If E1 OR E2 is true, they pass the financial check.
            if student_exception_ok or first_time_exception_ok:
                is_financial_eligible = True
                rejection_reason = "N/A - Qualified via Special Exception."
            else:
                # If neither standard nor exceptions are met, the application fails here.
                rejection_reason = "Failed financial criteria (Income/Score too low)."
                print(f"Status: REJECTED (Reason: {rejection_reason})")


# 8. Step 5: Final Determination
# The final status requires all major Boolean flags to be True.
if is_age_eligible and is_financial_eligible and is_debt_acceptable:
    final_eligibility_status = True

# 9. Step 6: Output Results
print("\n--- Final Assessment Summary ---")
print(f"Applicant: {applicant_name}")
print(f"Age Check Passed: {is_age_eligible}")
print(f"Debt Check Passed: {is_debt_acceptable}")
print(f"Financial Check Passed: {is_financial_eligible}")

if final_eligibility_status:
    print("\nFINAL DECISION: APPLICATION APPROVED.")
else:
    # If the decision was made in an earlier 'REJECTED' block, the reason is preserved.
    print(f"\nFINAL DECISION: APPLICATION DENIED. (Detailed Reason: {rejection_reason})")

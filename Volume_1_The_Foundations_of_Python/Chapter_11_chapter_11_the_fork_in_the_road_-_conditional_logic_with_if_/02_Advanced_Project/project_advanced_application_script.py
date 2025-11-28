
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

# --- 1. CONFIGURATION AND CONSTANTS ---

# Define the minimum standards required for different eligibility tiers.
MIN_AGE = 18
MIN_INCOME_TIER_1 = 30000  # Minimum required income for any approval
MIN_INCOME_TIER_2 = 60000  # Income required for 'Low Risk' status
MIN_SCORE_B = 680          # Minimum score required for approval
MIN_SCORE_A = 750          # Score required for 'Very Low Risk' status

# --- 2. SAMPLE APPLICANT DATA ---

# Data structure representing a potential loan applicant.
applicant_data = {
    "name": "Alex Johnson",
    "age": 32,
    "annual_income": 72000,
    "credit_score": 765,
    "existing_debt_ratio": 0.25
}

# --- 3. CORE LOGIC: THE ASSESSMENT VIEW FUNCTION ---

def assess_eligibility(applicant: dict) -> tuple:
    """
    Performs a multi-stage conditional assessment of an applicant's risk profile.
    This function acts as the core 'View Function' for the decision logic.
    """
    # Initialize state variables. These flags track eligibility status across checks.
    is_eligible = True
    risk_level = "Undefined"
    reasons = []

    # --- GATE 1: AGE CHECK (Hard Block) ---
    # If the applicant fails this initial check, we set eligibility to False
    # and use a return statement to exit the function immediately (efficiency).
    if applicant['age'] < MIN_AGE:
        is_eligible = False
        reasons.append("Applicant is below the minimum required age.")
        risk_level = "High Risk - Ineligible (Age)"
        # Early exit: No need to process financial data if the age requirement fails.
        return is_eligible, "DENIED (Age Failure)", reasons, risk_level

    # --- GATE 2: INCOME ASSESSMENT (Tiered Logic using elif) ---
    income = applicant['annual_income']
    
    if income >= MIN_INCOME_TIER_2:
        # Highest income tier sets the initial low risk baseline.
        risk_level = "Low Risk"
    elif income >= MIN_INCOME_TIER_1:
        # Middle tier income is sufficient but carries higher initial risk.
        risk_level = "Medium Risk"
    else:
        # Income below the absolute minimum threshold.
        is_eligible = False
        reasons.append("Annual income is below the minimum required threshold.")
        risk_level = "High Risk - Income Failure"

    # --- GATE 3: CREDIT SCORE ASSESSMENT (Modifying existing state) ---
    # We only proceed with credit checks if the applicant is not yet ineligible.
    if is_eligible:
        score = applicant['credit_score']
        
        if score >= MIN_SCORE_A:
            # Exceptional score overrides previous income-based risk assessment.
            risk_level = "Very Low Risk"
        elif score >= MIN_SCORE_B:
            # Acceptable score, confirms the existing risk level determined by income.
            pass  # Risk level remains Low or Medium, no change needed.
        else:
            # Score is too low, overriding previous positive assessments.
            is_eligible = False
            reasons.append("Credit score is below the required minimum.")
            risk_level = "High Risk - Score Failure"

    # --- GATE 4: FINAL DECISION MATRIX (Translating state into recommendation) ---
    
    # The final recommendation relies on the accumulated state of is_eligible and risk_level.
    if not is_eligible:
        final_recommendation = "DENIED"
    elif risk_level == "Very Low Risk":
        final_recommendation = "APPROVED (Premium Rate Offer)"
    elif risk_level == "Low Risk":
        final_recommendation = "APPROVED (Standard Rate Offer)"
    elif risk_level == "Medium Risk":
        final_recommendation = "PENDING MANUAL REVIEW (High Rate Potential)"
    else:
        # Catch-all: Should only trigger if an unexpected state occurs.
        final_recommendation = "ERROR: System State Undefined"

    return is_eligible, final_recommendation, reasons, risk_level

# --- 4. PRESENTATION LOGIC ---

def display_results(applicant_name, is_eligible, recommendation, reasons, risk_level):
    """Prints the final, formatted results of the assessment."""
    print("=" * 60)
    print(f"APPLICANT ASSESSMENT: {applicant_name.upper()}")
    print("-" * 60)
    print(f"Eligibility Status: {'ELIGIBLE' if is_eligible else 'INELIGIBLE'}")
    print(f"Internal Risk Level: {risk_level}")
    print(f"Final Recommendation: {recommendation}")
    
    if reasons:
        print("\nREASONS FOR STATUS:")
        for reason in reasons:
            print(f"  - {reason}")
    print("=" * 60)

# --- 5. EXECUTION BLOCK ---

if __name__ == "__main__":
    # 1. Run the assessment using the core conditional logic function.
    eligible, recommendation, failure_reasons, internal_risk = assess_eligibility(applicant_data)
    
    # 2. Display the outcome.
    display_results(
        applicant_data['name'], 
        eligible, 
        recommendation, 
        failure_reasons, 
        internal_risk
    )

    # Example 2: A denied applicant (low income)
    print("\n--- Running Second Applicant Test ---")
    applicant_denied = {
        "name": "Sarah Miller",
        "age": 45,
        "annual_income": 20000, # Fails Tier 1
        "credit_score": 780,
        "existing_debt_ratio": 0.10
    }
    eligible_2, rec_2, reasons_2, risk_2 = assess_eligibility(applicant_denied)
    display_results(applicant_denied['name'], eligible_2, rec_2, reasons_2, risk_2)

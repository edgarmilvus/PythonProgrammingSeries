
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

# Define system constants for thresholds and limits
MIN_STANDARD_DISCOUNT_TOTAL = 50.00
MIN_MEMBER_DISCOUNT_TOTAL = 100.00
MIN_FIRST_TIME_BONUS_TOTAL = 75.00
MAX_APPLICABLE_DISCOUNT = 0.25  # 25% is the absolute maximum cap

# --- INPUT DATA SIMULATION ---
# Scenario: A customer with a high-value cart, who is new, and shopping on a weekend.
cart_total = 125.50
is_member = False
is_first_time_customer = True
promo_code_used = "SUMMER24"  # Currently unused in logic, reserved for future expansion
current_day_of_week = "Sunday"

# --- CORE LOGIC FUNCTIONS: Generating Boolean Truths ---

def is_standard_eligible(total, member_status):
    """
    Checks for the basic 10% discount.
    Rule: Cart must exceed $50 AND the customer must NOT be a member (incentivizing membership).
    """
    # Use comparison operator (>) to check value threshold
    is_high_enough = total > MIN_STANDARD_DISCOUNT_TOTAL
    # Use logical operator (not) to negate the membership status
    is_not_already_member = not member_status
    # Combine conditions using logical operator (and)
    return is_high_enough and is_not_already_member

def is_premium_eligible(total, member_status):
    """
    Checks for the 15% membership discount.
    Rule: Cart must exceed $100 OR the customer is a member.
    """
    is_very_high_enough = total >= MIN_MEMBER_DISCOUNT_TOTAL
    # Use logical operator (or) to allow either condition to grant eligibility
    return is_very_high_enough or member_status

def is_first_time_bonus_eligible(total, first_timer):
    """
    Checks for the 20% first-time customer bonus.
    Rule: Must be a first-timer AND meet the minimum total of $75.
    """
    # Combines two conditions using 'and'
    is_first_timer_and_high_value = first_timer and (total >= MIN_FIRST_TIME_BONUS_TOTAL)
    return is_first_timer_and_high_value

def is_weekend_special(day):
    """
    Checks if the current day qualifies for the 5% weekend special.
    Rule: Day must be Saturday OR Sunday.
    """
    # Use comparison operators (==) and logical operator (or)
    is_weekend = (day == "Saturday") or (day == "Sunday")
    return is_weekend

# --- MAIN CALCULATION FUNCTION: Decision Flow ---

def calculate_best_discount(total, member, first_time, promo, day):
    """
    Calculates the single best applicable discount rate based on tiered Boolean logic.
    """
    best_rate = 0.0

    # Step 1: Evaluate all potential Boolean outcomes using helper functions
    standard_eligible = is_standard_eligible(total, member)
    premium_eligible = is_premium_eligible(total, member)
    first_time_eligible = is_first_time_bonus_eligible(total, first_time)
    weekend_eligible = is_weekend_special(day)

    # Step 2: Check for the highest tier (20% First Time Bonus)
    # This is the most valuable discount and must be checked first.
    # We use 'and not member' to ensure this bonus is exclusive to non-members.
    if first_time_eligible and (not member):
        best_rate = max(best_rate, 0.20)
        print(f"# LOG: Applied 20% First-Time Bonus.")

    # Step 3: Check for the Premium/Membership Tier (15%)
    # Uses elif because if the 20% rate applied, we skip this check.
    elif premium_eligible:
        best_rate = max(best_rate, 0.15)
        print(f"# LOG: Applied 15% Premium/Member Discount.")

    # Step 4: Check for the Standard Tier (10%)
    # Only runs if the 20% and 15% tiers were False.
    elif standard_eligible:
        best_rate = max(best_rate, 0.10)
        print(f"# LOG: Applied 10% Standard Discount.")

    # Step 5: Check for the Weekend Special (5%) - Independent check
    # This is an independent 'if' block, allowing it to potentially stack IF the primary rate is low (0%).
    # We use 'and best_rate == 0.0' to ensure the 5% only applies if no major discount was found above.
    # Note: In this specific implementation, since the Elif chain ensures a rate is set,
    # we adjust the condition to ensure it only applies if no major rate (>= 10%) was found.
    if weekend_eligible and (best_rate < 0.10):
        best_rate = max(best_rate, 0.05)
        print(f"# LOG: Applied 5% Weekend Special.")

    # Step 6: Apply the overall cap (25%)
    final_rate = min(best_rate, MAX_APPLICABLE_DISCOUNT)
    
    return final_rate

# --- EXECUTION AND OUTPUT ---

print("--- Dynamic Discount Engine Initialization ---")
print(f"Cart Total: ${cart_total:.2f}")
print(f"Member Status: {is_member}")
print(f"First Time Customer: {is_first_time_customer}")
print(f"Day of Week: {current_day_of_week}\n")

# Run the calculation
discount_rate = calculate_best_discount(
    cart_total,
    is_member,
    is_first_time_customer,
    promo_code_used,
    current_day_of_week
)

# Calculate final monetary values
discount_amount = cart_total * discount_rate
final_total = cart_total - discount_amount

# Output Results
print("\n--- Final Calculation Summary ---")
print(f"Best Applicable Rate: {discount_rate:.0%}")
print(f"Discount Applied: -${discount_amount:.2f}")
print(f"Final Price Paid: ${final_total:.2f}")

# Example of a final Boolean check for auditing and reporting
is_major_discount_applied = discount_rate >= 0.15
print(f"\nAudit Check: Was a Major Discount (>= 15%) Applied? {is_major_discount_applied}")

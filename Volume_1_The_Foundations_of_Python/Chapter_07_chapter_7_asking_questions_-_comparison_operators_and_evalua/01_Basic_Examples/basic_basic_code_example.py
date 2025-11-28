
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

# --- 1. Define the parameters (The Rules) ---

# The minimum dollar amount required for a customer to qualify for free shipping.
MINIMUM_FOR_FREE_SHIPPING = 50.00

# The age we are checking against (e.g., for a specific promotion).
TARGET_AGE = 18

# --- 2. Define the current state (The Data) ---

# The customer's current cart total, stored as a floating-point number.
cart_total = 45.50

# A Boolean variable indicating membership status.
is_member = True

# The customer's actual age, stored as an integer.
customer_age = 35

# --- 3. Comparison Operations (Asking Questions) ---

# Question A: Is the cart total enough for free shipping? (Greater than or Equal to)
# This checks if 45.50 >= 50.00
is_eligible_for_shipping = cart_total >= MINIMUM_FOR_FREE_SHIPPING

# Question B: Is the customer exactly the target age? (Equal to)
# This checks if 35 == 18
is_exactly_target_age = customer_age == TARGET_AGE

# Question C: Is the customer NOT a member? (Not Equal to)
# This checks if True != False
is_not_a_member = is_member != False

# Question D: Is the total strictly less than the minimum? (Less than)
# This checks if 45.50 < 50.00
is_too_low = cart_total < MINIMUM_FOR_FREE_SHIPPING

# --- 4. Outputting the Results ---

print(f"--- E-Commerce Eligibility Check ---")
print(f"Minimum Required for Shipping: ${MINIMUM_FOR_FREE_SHIPPING:.2f}")
print(f"Current Cart Total:          ${cart_total:.2f}")
print("-" * 40)

# Display the results of our comparison questions
print(f"A. Eligible for Free Shipping? (>= 50.00): {is_eligible_for_shipping}")
print(f"B. Is customer exactly {TARGET_AGE} years old? (== 18):     {is_exactly_target_age}")
print(f"C. Is customer a member? (!= False):          {is_not_a_member}")
print(f"D. Is total below minimum? (< 50.00):        {is_too_low}")

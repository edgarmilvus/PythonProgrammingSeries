
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

# ====================================================================
# Exercise 4.1: The Secure Login Check
# ====================================================================

# 1. Define correct credentials (securely stored data)
CORRECT_USERNAME = "admin_user"
CORRECT_PASSWORD = "SuperSecurePassword123"

print("--- Exercise 4.1: Secure Login Check ---")

# 2. Prompt for user input
# NOTE: In a live environment, these lines wait for user input.
# For demonstration purposes, assume the user enters correct credentials first.
# To test failure, run the script and enter incorrect credentials.
username_input = input("Enter Username: ")
password_input = input("Enter Password: ")

# 3. Check username match using the equality operator (==)
username_match = (username_input == CORRECT_USERNAME)

# 4. Check password match using the equality operator (==)
password_match = (password_input == CORRECT_PASSWORD)

# 5. Determine final login success: both conditions MUST be True
login_successful = username_match and password_match

# 6. Print result
print(f"\nUsername Match: {username_match}")
print(f"Password Match: {password_match}")
print(f"Login Successful: {login_successful}")


# ====================================================================
# Exercise 4.2: University Eligibility Checker
# ====================================================================

print("\n--- Exercise 4.2: University Eligibility Checker ---")

# 1. Define student variables (Test Case 1: Meets Secondary only)
student_age = 19
student_gpa = 3.6
student_test_score = 1550

# 2. Primary Track Requirements: Age >= 18 AND GPA > 3.7
# Both conditions must be met for this track to be True.
is_primary_eligible = (student_age >= 18) and (student_gpa > 3.7)

# 3. Secondary Track Requirements: Age < 25 AND Test Score >= 1500
# Both conditions must be met for this alternative track to be True.
is_secondary_eligible = (student_age < 25) and (student_test_score >= 1500)

# 4. Final eligibility: Primary OR Secondary
# Only one track needs to be True for overall eligibility.
is_eligible = is_primary_eligible or is_secondary_eligible

# 5. Print results
print(f"Student Age: {student_age}, GPA: {student_gpa}, Score: {student_test_score}")
print(f"Primary Track Eligible (Age >= 18 AND GPA > 3.7): {is_primary_eligible}")
print(f"Secondary Track Eligible (Age < 25 AND Score >= 1500): {is_secondary_eligible}")
print(f"Overall Eligible (Primary OR Secondary): {is_eligible}")

# Test Case 2: Fails both (Age 30 fails secondary age, Score 1400 fails secondary score)
student_age_fail = 30
student_gpa_fail = 3.8
student_test_score_fail = 1400

is_primary_fail = (student_age_fail >= 18) and (student_gpa_fail > 3.7)
is_secondary_fail = (student_age_fail < 25) and (student_test_score_fail >= 1500)
is_eligible_fail = is_primary_fail or is_secondary_fail

print(f"\nTest Case 2 (30 y/o, 3.8 GPA, 1400 Score) Eligible: {is_eligible_fail}")


# ====================================================================
# Exercise 4.3: Sensor Data Inversion (Using NOT)
# ====================================================================

print("\n--- Exercise 4.3: Sensor Data Inversion ---")

# 1. Define variables and constants
current_temp = 25.5  # Test value (outside range)
MIN_SAFE_TEMP = 18.0
MAX_SAFE_TEMP = 24.0

# 3. Success condition: Check if temperature is within the safe range (18.0 to 24.0 inclusive)
# Using Python's concise chained comparison
is_within_safe_range = MIN_SAFE_TEMP <= current_temp <= MAX_SAFE_TEMP

# 4. Failure condition: Use NOT to invert the success condition
# If it IS NOT within the safe range, it IS a critical failure.
is_critical_failure = not is_within_safe_range

# 5. Print results
print(f"Current Temperature: {current_temp}°C")
print(f"Is within safe range ({MIN_SAFE_TEMP}-{MAX_SAFE_TEMP}): {is_within_safe_range}")
print(f"Is Critical Failure: {is_critical_failure}")

# Test with a safe value (19.0)
current_temp = 19.0
is_within_safe_range = MIN_SAFE_TEMP <= current_temp <= MAX_SAFE_TEMP
is_critical_failure = not is_within_safe_range
print(f"\nTest Temp: {current_temp}°C")
print(f"Is Critical Failure: {is_critical_failure}")


# ====================================================================
# Exercise 4.4: Interactive Challenge - The Override Switch
# ====================================================================

print("\n--- Exercise 4.4: The Override Switch ---")

# --- STARTING STATE ---
user_level = "Premium"
system_load = 0.55  # Load is currently acceptable for Premium user

PREMIUM_LOAD_THRESHOLD = 0.80
STANDARD_LOAD_THRESHOLD = 0.40

# --- ORIGINAL COMPLEX LOGIC ---
is_premium_allowed = (user_level == "Premium") and (system_load < PREMIUM_LOAD_THRESHOLD)
is_standard_allowed = (user_level == "Standard") and (system_load < STANDARD_LOAD_THRESHOLD)
original_access_granted = is_premium_allowed or is_standard_allowed

print(f"User Level: {user_level}, System Load: {system_load}")
print(f"Original decision (user qualifies based on load/level): {original_access_granted}") # True

# 2. Add the new override switch
SYSTEM_MAINTENANCE = True # Test 1: System is down

# 3. Modify the final access decision logic

# First, define the requirement that the system must be available
is_system_available = not SYSTEM_MAINTENANCE

# The final decision requires the complex original conditions AND system availability
final_access_granted = original_access_granted and is_system_available

print(f"System Maintenance Active: {SYSTEM_MAINTENANCE}")
# Expected result: False (Maintenance overrides the positive original decision)
print(f"Final Access Granted (Test 1 - Maintenance ON): {final_access_granted}")

# Test 2: Maintenance is off
SYSTEM_MAINTENANCE = False
is_system_available = not SYSTEM_MAINTENANCE
final_access_granted = original_access_granted and is_system_available

print(f"\nSystem Maintenance Active: {SYSTEM_MAINTENANCE}")
# Expected result: True (Original logic holds, and maintenance is not active)
print(f"Final Access Granted (Test 2 - Maintenance OFF): {final_access_granted}")


# ====================================================================
# Exercise 4.5: The Truthiness Test (Conceptual Deep Dive)
# ====================================================================

print("\n--- Exercise 4.5: The Truthiness Test ---")

# Define values of various data types
number_zero = 0
number_positive = 100
empty_string = ""
non_empty_string = "Hello"
none_value = None
empty_list = []

# All numerical zeros are Falsy
print(f"Value: {number_zero} (0). bool(): {bool(number_zero)}")

# Any non-zero number is Truthy
print(f"Value: {number_positive} (100). bool(): {bool(number_positive)}")

# Empty sequences (strings, lists, etc.) are Falsy
print(f"Value: '{empty_string}' (empty string). bool(): {bool(empty_string)}")

# Non-empty sequences are Truthy
print(f"Value: '{non_empty_string}' (non-empty string). bool(): {bool(non_empty_string)}")

# The special constant None is Falsy
print(f"Value: {none_value} (None). bool(): {bool(none_value)}")

# Empty collections are Falsy
print(f"Value: {empty_list} (empty list). bool(): {bool(empty_list)}")

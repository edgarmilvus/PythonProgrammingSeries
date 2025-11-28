
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

# Exercise 8-4: Interactive Challenge - Enhancing Access Control

# --- Scenario 1 Test Data (Standard Fail, Temp Pass) ---
user_role_1 = 'Editor'
is_active_1 = False
has_temp_access_token_1 = True
is_read_only_request_1 = True

# Part 1: Standard Access Logic
# Must be active AND have an eligible role. (False AND True) -> False
standard_access_1 = is_active_1 and (user_role_1 == 'Admin' or user_role_1 == 'Editor')

# Part 2: Temporary Override Logic
# Must be INACTIVE AND have token AND be read-only. (True AND True AND True) -> True
temp_override_1 = (not is_active_1) and has_temp_access_token_1 and is_read_only_request_1

# Combined Access: Standard OR Temporary (False OR True) -> True
access_granted_1 = standard_access_1 or temp_override_1

print("--- Scenario 1 Test ---")
print(f"Standard Access Granted: {standard_access_1}")
print(f"Temporary Override Active: {temp_override_1}")
print(f"Final Access Granted: {access_granted_1}")


# --- Scenario 2 Test Data (Standard Pass, Temp Irrelevant) ---
user_role_2 = 'Admin'
is_active_2 = True
has_temp_access_token_2 = False
is_read_only_request_2 = False

# Part 1: Standard Access Logic (True AND True) -> True
standard_access_2 = is_active_2 and (user_role_2 == 'Admin' or user_role_2 == 'Editor')

# Part 2: Temporary Override Logic (not True is False, so the whole expression is False)
temp_override_2 = (not is_active_2) and has_temp_access_token_2 and is_read_only_request_2

# Combined Access: Standard OR Temporary (True OR False) -> True
access_granted_2 = standard_access_2 or temp_override_2

print("\n--- Scenario 2 Test ---")
print(f"Standard Access Granted: {standard_access_2}")
print(f"Temporary Override Active: {temp_override_2}")
print(f"Final Access Granted: {access_granted_2}")

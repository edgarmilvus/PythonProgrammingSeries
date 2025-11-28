
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

# --- Scenario A: Admin with correct permissions ---
# user_role = "Administrator"
# user_permissions = "FULL_ACCESS"

# --- Scenario B: Manager with incorrect permissions ---
# user_role = "Manager"
# user_permissions = "READ_ONLY"

# --- Scenario C: Guest ---
user_role = "Guest"
user_permissions = "NONE"

print(f"Attempting access for Role: {user_role}, Permissions: {user_permissions}")
print("-" * 30)

# Primary Role Check (Outer Conditional)
if user_role == "Administrator":
    # Role passed, proceed to nested Permission Check
    # 2. Nesting: Administrator must have FULL_ACCESS
    if user_permissions == "FULL_ACCESS":
        print("ACCESS GRANTED: Administrator with full system privileges.")
    else:
        print("ACCESS DENIED: Administrator role detected, but required permission 'FULL_ACCESS' is missing.")

elif user_role == "Manager":
    # Role passed, proceed to nested Permission Check
    # 2. Nesting: Manager must have READ_WRITE
    if user_permissions == "READ_WRITE":
        print("ACCESS GRANTED: Manager with read/write privileges.")
    else:
        print("ACCESS DENIED: Manager role detected, but required permission 'READ_WRITE' is missing.")

# 3. Guest Access Check
elif user_role == "Guest":
    print("ACCESS DENIED: Guest roles are strictly prohibited from this system.")

# 4. Unknown Role Check
else:
    print(f"ACCESS DENIED: Unknown or unauthorized role '{user_role}'.")


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

def check_access(user_role, current_hour, subscription_tier):
    """
    Determines user access based on subscription tier, role, and time of day.
    Subscription tier logic takes precedence.
    """
    print(f"\n--- Checking Access: Role={user_role}, Hour={current_hour}, Tier={subscription_tier} ---")
    
    # 1. Highest Priority Check: Premium Tier
    if subscription_tier == "Premium":
        print("RESULT: Priority Access (Tier override).")
        
    # 2. Second Priority Check: Standard Tier
    # Standard tier users follow the original role-based logic.
    elif subscription_tier == "Standard":
        # Check original role logic:
        if user_role == "Admin":
            print("RESULT: Full access granted (Standard Tier, Admin Role).")
        elif user_role == "Standard":
            # Check time restriction for Standard Role
            if current_hour >= 9 and current_hour <= 17:
                print("RESULT: Standard access granted during business hours.")
            else:
                print("RESULT: Standard access denied outside business hours.")
        else:
            print("RESULT: Guest access only (Standard Tier).")
            
    # 3. Third Priority Check: Free Tier
    elif subscription_tier == "Free":
        # Apply complex Free Tier rules
        if user_role == "Admin":
            # Free Tier Admin is treated as Standard Tier for security
            print("RESULT: Standard access granted (Free Tier Admin treated as Standard).")
        else:
            # All other Free Tier users get read-only access
            print("RESULT: Read-Only Access.")
            
    # 4. Fallback (If subscription tier is unrecognized)
    else:
        print("RESULT: Access Denied (Unknown Subscription Tier).")

# Example Usage:

# Premium Tier Override (regardless of role or time)
check_access("Standard", 22, "Premium") 

# Standard Tier following time restriction
check_access("Standard", 10, "Standard") # Standard access granted
check_access("Standard", 20, "Standard") # Standard access denied

# Free Tier complex logic
check_access("Admin", 12, "Free")      # Treated as Standard access
check_access("Guest", 12, "Free")      # Read-Only Access

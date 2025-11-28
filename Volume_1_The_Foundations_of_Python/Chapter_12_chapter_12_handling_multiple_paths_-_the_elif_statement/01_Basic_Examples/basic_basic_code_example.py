
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

# --- Membership Tier Classifier ---

# 1. Define the input variable representing years of service
years_of_membership = 3

# 2. Start the conditional structure using 'if'
# We check the most exclusive (highest) condition first.
if years_of_membership >= 10:
    # This block runs only if the member has 10 or more years
    subscription_level = "Platinum Tier"
    print(f"Congratulations! You are a highly valued {subscription_level} member.")

# 3. Use 'elif' to check the next condition
# This check only happens if the 'if' condition (>= 10) was False.
elif years_of_membership >= 5:
    # This block runs only if the member has 5 to 9 years
    subscription_level = "Gold Tier"
    print(f"Welcome back! You are a prestigious {subscription_level} member.")

# 4. Use a second 'elif' to check the third condition
# This check only happens if the previous two conditions were False.
elif years_of_membership >= 2:
    # This block runs only if the member has 2 to 4 years
    subscription_level = "Silver Tier"
    print(f"Enjoy the perks of the {subscription_level}.")

# 5. Use 'else' as the final fallback
# This block runs only if ALL preceding 'if' and 'elif' conditions were False.
else:
    # This block covers all memberships less than 2 years
    subscription_level = "Bronze Tier"
    print(f"Thank you for being a {subscription_level} member.")

# 6. Final output confirming the result
print("-" * 30)
print(f"Processing complete. Assigned Tier: {subscription_level}")

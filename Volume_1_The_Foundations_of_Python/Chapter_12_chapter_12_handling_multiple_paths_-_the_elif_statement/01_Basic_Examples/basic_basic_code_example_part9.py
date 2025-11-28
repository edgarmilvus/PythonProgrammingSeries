
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

# Source File: basic_basic_code_example_part9.py
# Description: Basic Code Example
# ==========================================

years_of_membership = 12

# INCORRECT ORDERING: Checking the broad condition first
if years_of_membership >= 2:
    # This condition is TRUE for 2, 5, 10, 12, etc.
    subscription_level = "Silver Tier"
    print(f"Assigned: {subscription_level}")

# This elif will NEVER be reached if years_of_membership >= 2
elif years_of_membership >= 5:
    subscription_level = "Gold Tier"
    print(f"Assigned: {subscription_level}")

# This elif will also NEVER be reached
elif years_of_membership >= 10:
    subscription_level = "Platinum Tier"
    print(f"Assigned: {subscription_level}")

else:
    subscription_level = "Bronze Tier"

# Output for input 12: Assigned: Silver Tier (INCORRECT!)

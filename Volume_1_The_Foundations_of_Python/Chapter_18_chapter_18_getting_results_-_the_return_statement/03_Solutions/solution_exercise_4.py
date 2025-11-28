
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

def validate_password(password):
    """
    Validates a password based on length and character presence.
    Uses early return (guard clauses) for immediate failure signaling.
    """
    MIN_LENGTH = 8
    REQUIRED_CHAR = '@'
    
    print(f"-> Validating: '{password}'")
    
    # Check 1: Length validation (Guard Clause)
    if len(password) < MIN_LENGTH:
        print("   [FAIL] Password too short. Exiting.")
        # Early exit: If this condition is met, the function stops here.
        return False
    
    # Check 2: Character presence validation (Guard Clause)
    # This line is only reached if Check 1 passed.
    if REQUIRED_CHAR not in password:
        print(f"   [FAIL] Missing required character '{REQUIRED_CHAR}'. Exiting.")
        # Early exit: Function stops here.
        return False
        
    # If execution reaches this point, all conditions passed.
    print("   [PASS] Password is valid.")
    return True

# Test Cases
print(f"\nResult 1 (Too short): {validate_password('short')}")
print("-" * 30)
print(f"Result 2 (Missing '@'): {validate_password('longenough123')}")
print("-" * 30)
print(f"Result 3 (Valid): {validate_password('Secure@Pass123')}")

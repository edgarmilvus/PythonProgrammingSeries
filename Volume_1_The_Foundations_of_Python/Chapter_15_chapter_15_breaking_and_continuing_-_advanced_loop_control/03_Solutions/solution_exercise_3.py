
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

def validate_password_loop():
    """Continuously prompts for a password until security criteria are met."""
    print("\n--- Exercise 3: Secure Password Input Loop ---")
    
    # Requirement 1: Use while True for continuous prompting
    while True:
        # Note: In a real application, input() should be handled safely.
        password = input("Enter password (min 8 chars, 1 uppercase, 1 digit): ")
        
        # Check 1: Length (Requirement 1)
        if len(password) < 8:
            print("ERROR: Password must be at least 8 characters long.")
            # Requirement 3: Restart loop iteration
            continue 
            
        # Check 2: Uppercase Letter (Requirement 2)
        # Use any() for efficient checking if any character is uppercase
        if not any(c.isupper() for c in password):
            print("ERROR: Password must contain at least one uppercase letter.")
            # Requirement 3: Restart loop iteration
            continue
            
        # Check 3: Digit (Requirement 3)
        # Use any() for efficient checking if any character is a digit
        if not any(c.isdigit() for c in password):
            print("ERROR: Password must contain at least one digit.")
            # Requirement 3: Restart loop iteration
            continue
            
        # Requirement 4: All checks passed
        print("\nSUCCESS: Password meets all security requirements.")
        # Requirement 4: Exit the infinite loop
        break

# Execute the interactive function (Uncomment to run interactively)
# validate_password_loop() 

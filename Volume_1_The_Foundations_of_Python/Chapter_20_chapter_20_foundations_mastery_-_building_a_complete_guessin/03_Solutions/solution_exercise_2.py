
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# --- Function for Robust Input Handling ---
def get_safe_guess(prompt):
    """
    Safely prompts the user for a positive integer input using .isdigit() 
    and handles invalid input without crashing.
    """
    while True:
        user_input = input(prompt)
        
        # 1. String Check: Use .isdigit() to verify input is a positive whole number string
        if user_input.isdigit():
            # 2. Conversion and Exit: If valid, convert and return the integer
            return int(user_input)
        else:
            # 3. Validation Feedback: If invalid, notify the user and loop again
            print("Error: Invalid input. Please enter a positive whole number.")

# --- Integration into a Simplified Game Structure ---
SECRET = 50
print("--- Starting Safe Guess Test (Secret number is 50) ---")

attempts = 0
guess = -1 # Initialize guess to guarantee loop starts

while guess != SECRET:
    attempts += 1
    
    # Use the robust input function
    guess = get_safe_guess(f"Attempt {attempts}. Enter your guess: ")
    
    # Provide feedback
    if guess < SECRET:
        print("Too low, try again.")
    elif guess > SECRET:
        print("Too high, try again.")

print(f"\nCorrect! The number was {SECRET}. You took {attempts} attempts.")

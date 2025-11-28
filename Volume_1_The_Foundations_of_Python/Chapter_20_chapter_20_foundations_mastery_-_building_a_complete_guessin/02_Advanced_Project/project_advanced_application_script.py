
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import random
import sys 

# --- 1. CONFIGURATION CONSTANTS ---
# Define the constraints for the simulation
MAX_ALLOCATION_PERCENT = 100
MIN_ALLOCATION_PERCENT = 0
MAX_ATTEMPTS = 7

# Define the acceptable range for the secret optimal percentage
OPTIMAL_RANGE_MIN = 25
OPTIMAL_RANGE_MAX = 75

# --- 2. CORE GAME STATE INITIALIZATION ---
# Generate the secret optimal percentage for the current project phase (e.g., R&D)
# This uses the random module to ensure variability.
SECRET_OPTIMAL_PERCENTAGE = random.randint(OPTIMAL_RANGE_MIN, OPTIMAL_RANGE_MAX)

# Initialize control variables
attempts_left = MAX_ATTEMPTS
game_won = False

# --- 3. HELPER FUNCTION: Input Validation and Conversion ---
def get_valid_guess(min_val, max_val):
    """
    Prompts the user for input and ensures it is a valid integer 
    within the predefined budget percentage range (0-100).
    Uses a nested while loop to force valid input before proceeding.
    """
    while True:
        try:
            # Display attempt number and prompt
            attempt_num = MAX_ATTEMPTS - attempts_left + 1
            prompt = f"Attempt ({attempt_num}/{MAX_ATTEMPTS}): Enter budget % allocation ({min_val}-{max_val}): "
            user_input = input(prompt)
            
            # Attempt to convert the input string to an integer
            guess = int(user_input)
            
            # Check if the guess is within the allowed bounds
            if min_val <= guess <= max_val:
                return guess
            else:
                # Handle input that is numerically valid but out of bounds (e.g., 101)
                print(f"Validation Error: Allocation must be between {min_val}% and {max_val}%.")
        
        except ValueError:
            # Handle non-integer input (e.g., letters, symbols, decimals)
            print("Validation Error: Please enter a whole number percentage.")
        except EOFError:
            # Handle interruption (e.g., Ctrl+D or Ctrl+Z)
            print("\nGame interrupted. Exiting simulator.")
            sys.exit(0)

# --- 4. GAME INTRODUCTION AND RULES ---
print("-" * 70)
print("PROJECT BUDGET OPTIMIZATION SIMULATOR: Phase X Allocation")
print(f"Goal: Guess the optimal budget percentage (between {OPTIMAL_RANGE_MIN}% and {OPTIMAL_RANGE_MAX}%)")
print(f"You have {MAX_ATTEMPTS} chances to allocate the funds correctly to ensure project success.")
print("-" * 70)

# --- 5. MAIN GAME LOOP (Iterative Control Flow) ---
# The loop continues as long as attempts remain AND the game has not been won.
while attempts_left > 0 and not game_won:
    
    # Get validated input from the user using the helper function
    current_guess = get_valid_guess(MIN_ALLOCATION_PERCENT, MAX_ALLOCATION_PERCENT)
    
    # Decrement the attempt counter AFTER successful input validation
    attempts_left -= 1
    
    # --- Conditional Logic (If/Elif/Else) for Feedback ---
    
    if current_guess == SECRET_OPTIMAL_PERCENTAGE:
        # Success condition: Perfect match
        game_won = True
        
    elif current_guess > SECRET_OPTIMAL_PERCENTAGE:
        # Feedback for high guess (Over-allocation risk)
        # We use f-strings for dynamic feedback based on the guess variable
        print(f"Feedback: {current_guess}% is too high. Budget is over-allocated, risking efficiency loss.")
        
    else: # This implicitly means current_guess < SECRET_OPTIMAL_PERCENTAGE
        # Feedback for low guess (Under-allocation risk)
        print(f"Feedback: {current_guess}% is too low. Risk of under-resourcing this critical phase.")
        
    # Provide remaining attempts status, but only if the game is still active
    if not game_won and attempts_left > 0:
        print(f"Remaining attempts: {attempts_left}\n")
    elif not game_won and attempts_left == 0:
        print("\n--- Project Budget Deadline Reached ---")


# --- 6. GAME CONCLUSION ---
print("=" * 70)
if game_won:
    # Calculate performance metric based on remaining attempts
    attempts_used = MAX_ATTEMPTS - attempts_left
    score = (MAX_ATTEMPTS - attempts_used + 1) * 20 # Higher score for fewer attempts
    print(f"SUCCESS! Optimal Allocation Found: {SECRET_OPTIMAL_PERCENTAGE}%")
    print(f"You optimized the budget in {attempts_used} attempts. Optimization Score: {score} points.")
    print("Project Phase X is green-lit and fully funded.")
else:
    print("FAILURE. The project failed due to improper resource allocation.")
    print(f"The required optimal percentage was: {SECRET_OPTIMAL_PERCENTAGE}%.")
    print("The simulation concludes that the project ran out of time before budget alignment.")
print("=" * 70)

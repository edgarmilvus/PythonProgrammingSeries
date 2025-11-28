
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

import random

# --- 1. Input and Validation for Dynamic Range ---
print("--- Dynamic Range Setup ---")
while True:
    try:
        # Prompt for bounds and convert immediately to integer
        lower_bound = int(input("Enter the lower bound of the range (e.g., 1): "))
        upper_bound = int(input("Enter the upper bound of the range (e.g., 100): "))

        # 2. Validation Check
        if lower_bound < upper_bound:
            # Valid bounds provided, break the setup loop
            break
        else:
            print("Error: The lower bound must be strictly less than the upper bound. Try again.")
    except ValueError:
        # Handle non-integer input during setup
        print("Error: Please enter valid whole numbers for the bounds.")


# 3. Secret Number Generation
# random.randint includes both the lower and upper bounds
secret_number = random.randint(lower_bound, upper_bound)
attempts = 0
guess = None

print(f"\nGame started! I'm thinking of a number between {lower_bound} and {upper_bound}.")

# 4. Game Loop
while guess != secret_number:
    try:
        guess = int(input("Enter your guess: "))
        attempts += 1
        
        # 5. Feedback
        if guess < secret_number:
            print("Too Low!")
        elif guess > secret_number:
            print("Too High!")
        else:
            print(f"\n*** Congratulations! ***")
            print(f"You guessed the number {secret_number} in {attempts} attempts.")

    except ValueError:
        # Handle non-integer input during the game
        print("Invalid input. Please enter a whole number.")
        # Do not increment attempts if input was invalid
        continue

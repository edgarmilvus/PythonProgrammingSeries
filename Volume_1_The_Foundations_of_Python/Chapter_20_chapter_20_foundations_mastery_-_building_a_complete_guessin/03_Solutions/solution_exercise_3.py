
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

import random

# 1. Define Constants
MAX_ATTEMPTS = 7
RANGE_MAX = 20 # Fixed range for simplicity
secret_number = random.randint(1, RANGE_MAX)

# 2. Attempt Counter
attempts_used = 0
guess = -1 # Initialize guess to guarantee loop starts

print(f"I'm thinking of a number between 1 and {RANGE_MAX}. You have {MAX_ATTEMPTS} attempts.")

# 3. Loop Condition: Continue if guess is incorrect AND attempts remain
while guess != secret_number and attempts_used < MAX_ATTEMPTS:
    
    # Calculate and print remaining attempts
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    print(f"\nAttempts remaining: {attempts_remaining}")
    
    # Get user input (using simple input for this exercise)
    try:
        guess = int(input("Enter your guess: "))
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        continue # Skip the rest of the loop and don't count the attempt
        
    # Provide feedback
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
        
    # 4. Increment attempt counter
    attempts_used += 1

# 5. Post-Loop Result Check (Win or Loss)
if guess == secret_number:
    print(f"\n--- VICTORY! ---")
    print(f"You guessed the number {secret_number} in {attempts_used} attempts!")
else:
    # Loop ended because attempts_used reached MAX_ATTEMPTS
    print(f"\n--- GAME OVER! ---")
    print(f"You ran out of attempts ({MAX_ATTEMPTS}).")
    print(f"The secret number was {secret_number}.")

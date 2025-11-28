
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

import random

# --- Function for Robust Input Handling (E 20.2) ---
def get_safe_guess(prompt):
    """Safely prompts the user for a positive integer input."""
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Error: Invalid input. Please enter a positive whole number.")

# --- Core Game Logic Function (E 20.4 & E 20.5) ---
def run_guessing_game():
    """Runs a single round of the guessing game with dynamic difficulty."""
    print("\n--- Starting New Game Round ---")
    
    # 1. Difficulty Setup (E 20.4)
    range_max = 0
    max_attempts = 0
    
    # Input validation loop for difficulty choice
    while True:
        choice = input("Select difficulty (E: 1-20/8 attempts, M: 1-50/6 attempts, H: 1-100/5 attempts): ").upper()
        
        # 2. Difficulty Mapping
        if choice == 'E':
            range_max = 20
            max_attempts = 8
            break
        elif choice == 'M':
            range_max = 50
            max_attempts = 6
            break
        elif choice == 'H':
            range_max = 100
            max_attempts = 5
            break
        else:
            print("Invalid selection. Please choose E, M, or H.")

    # 3. Game Initialization
    secret_number = random.randint(1, range_max)
    attempts_used = 0
    guess = -1
    
    print(f"\nDifficulty: {choice}. Range: 1 to {range_max}.")
    print(f"You have {max_attempts} attempts.")

    # 4. Main Game Loop (E 20.3 Logic)
    while guess != secret_number and attempts_used < max_attempts:
        
        attempts_remaining = max_attempts - attempts_used
        print(f"\nAttempts remaining: {attempts_remaining}")
        
        # Use the robust input function (E 20.2)
        guess = get_safe_guess("Enter your guess: ")
        
        # Optional: Range validation feedback
        if guess < 1 or guess > range_max:
            print(f"Warning: Your guess is outside the range (1-{range_max}).")
            continue
            
        # Provide feedback
        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        
        # Increment attempt counter
        attempts_used += 1

    # 5. Post-Loop Result Check
    if guess == secret_number:
        print(f"\n--- VICTORY! ---")
        print(f"You guessed the number {secret_number} in {attempts_used} attempts!")
    else:
        print(f"\n--- GAME OVER! ---")
        print(f"You ran out of attempts.")
        print(f"The secret number was {secret_number}.")


# --- Main Application Control (E 20.5) ---
if __name__ == "__main__":
    print("Welcome to the Comprehensive Python Foundations Guessing Game!")
    
    # Main control loop for replayability
    while True:
        # 3. Execution: Run a single round of the game
        run_guessing_game()
        
        # 4. Replay Prompt
        replay_choice = input("\nDo you want to play another round? (Y/N): ").upper()
        
        # 5. Conditional Exit
        if replay_choice == 'N':
            print("\nThank you for playing. Exiting program.")
            break
        elif replay_choice != 'Y':
            # Handle invalid input gracefully, continuing the loop
            print("Invalid choice detected. Assuming 'Yes' and starting new game...")

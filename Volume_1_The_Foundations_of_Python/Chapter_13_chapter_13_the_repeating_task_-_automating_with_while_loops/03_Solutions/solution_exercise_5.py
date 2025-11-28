
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# Game constants
SECRET_NUMBER = 42
MAX_ATTEMPTS = 5

# Outer loop control flag
playing_game = True

print("Welcome to the Number Guessing Game!")

# Outer loop: Controls multiple rounds of the game
while playing_game:
    print(f"\n--- New Round Started (Secret number is {SECRET_NUMBER}) ---")
    
    # State variables reset for the inner loop
    attempts = 0
    guessed_correctly = False

    # Inner loop: Controls the guessing process (attempts)
    while attempts < MAX_ATTEMPTS and not guessed_correctly:
        attempts += 1
        
        # Input handling for the guess
        try:
            user_guess = int(input(f"Attempt {attempts}/{MAX_ATTEMPTS}. Guess the number: "))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            # Decrement attempt counter so invalid input doesn't count
            attempts -= 1 
            continue

        if user_guess == SECRET_NUMBER:
            guessed_correctly = True
            break  # Exit inner loop immediately on success
        elif user_guess < SECRET_NUMBER:
            print("Too low.")
        else:
            print("Too high.")
            
    # Check game outcome after inner loop terminates
    if guessed_correctly:
        print(f"Congratulations! You guessed {SECRET_NUMBER} in {attempts} attempts.")
    else:
        print(f"Game Over. You ran out of attempts. The number was {SECRET_NUMBER}.")

    # Outer loop control: Ask to play again (using validation loop)
    while True:
        play_again_input = input("Play another round? (yes/no): ").strip().lower()
        
        if play_again_input == 'no':
            playing_game = False
            print("Thanks for playing!")
            break  # Exit the validation loop, leading to outer loop termination
            
        elif play_again_input == 'yes':
            print("Starting new game...")
            break  # Exit the validation loop, outer loop continues
            
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

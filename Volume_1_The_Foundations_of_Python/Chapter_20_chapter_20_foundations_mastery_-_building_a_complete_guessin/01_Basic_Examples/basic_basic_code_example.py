
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

import sys

# 1. Define the fixed secret number (The combination of the safe)
SECRET_NUMBER = 7

# 2. Initialize a sentinel variable to store the user's current guess
# We use -1, a value outside the expected range, to ensure the while loop starts
guess = -1 

# Display a welcome message
print("--- Mini Combination Lock Challenge ---")
print("Guess the secret number between 1 and 10.")

# 3. Start the main game loop
# The loop continues as long as the user's guess is NOT equal to the secret number
while guess != SECRET_NUMBER:
    
    # 4. Prompt the user for input
    user_input = input("Enter your guess: ")

    # 5. Handle potential non-numeric input gracefully (Basic error handling)
    try:
        # Attempt to convert the input string into an integer
        guess = int(user_input)
    except ValueError:
        # If conversion fails (e.g., user types 'hello'), print an error
        print("Invalid input. Please enter a whole number.")
        # We use 'continue' to skip the rest of the loop body and restart the loop
        continue 

    # 6. Check the guess using conditional logic (The core decision tree)
    if guess < SECRET_NUMBER:
        # This condition is met if the guess is too low
        print("Too low! The combination is higher.")
    
    elif guess > SECRET_NUMBER:
        # This condition is checked only if the 'if' condition (guess < SECRET_NUMBER) was False
        print("Too high! The combination is lower.")
    
    else:
        # This 'else' block executes only if the guess is neither less than nor greater than the secret number
        # Meaning: guess MUST equal SECRET_NUMBER
        print("Access Granted! You successfully entered the combination 7.")
        # Note: The loop will automatically terminate upon returning to the 'while' check

# 7. Code execution continues here after the while loop condition becomes False
print("--- Challenge Complete. Safe is Open. ---")

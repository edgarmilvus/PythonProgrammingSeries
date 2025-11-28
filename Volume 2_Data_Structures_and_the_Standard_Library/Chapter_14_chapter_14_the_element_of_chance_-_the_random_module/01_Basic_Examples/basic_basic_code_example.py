
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

import random

# --- 1. Setting the Stage: Constants and Lists ---
# Define the boundaries for the dice roll. Using constants improves readability.
MIN_DICE_VALUE = 1
MAX_DICE_VALUE = 6

# A list representing potential outcomes or prizes.
PRIZE_POOL = ["A Free Coffee", "A Mystery Box", "A Discount Coupon", "Better Luck Next Time"]

print("--- Chapter 14: Basic Randomness Demonstration ---")

# --- 2. Generating a Discrete Integer (Simulating a Dice Roll) ---
# random.randint(a, b) generates an integer N such that a <= N <= b (inclusive).
dice_roll_result = random.randint(MIN_DICE_VALUE, MAX_DICE_VALUE)
print(f"\n[Action 1: Dice Roll] We asked for a number between 1 and 6, inclusive.")
print(f"You rolled a: {dice_roll_result}")

# --- 3. Generating a Continuous Float (Simulating a Weighted Coin Flip) ---
# random.random() returns a float N such that 0.0 <= N < 1.0 (exclusive of 1.0).
# We simulate a weighted coin where a value less than 0.7 means "Success".
SUCCESS_THRESHOLD = 0.7
coin_flip_value = random.random()
is_success = coin_flip_value < SUCCESS_THRESHOLD

print(f"\n[Action 2: Weighted Probability Check] Random float generated: {coin_flip_value:.4f}")

if is_success:
    print(f"Result: Success! (Value {coin_flip_value:.4f} was less than {SUCCESS_THRESHOLD})")
else:
    print(f"Result: Failure. (Value {coin_flip_value:.4f} was {SUCCESS_THRESHOLD} or greater)")

# --- 4. Selecting a Random Element from a Sequence (Prize Selection) ---
# random.choice() selects one item uniformly at random from the provided sequence.
selected_prize = random.choice(PRIZE_POOL)
print(f"\n[Action 3: Prize Selection] The computer randomly selected your prize:")
print(f"*** Your Prize: {selected_prize} ***")

# --- 5. Demonstrating Seeding (Controlling Randomness) ---
# We set a specific seed value (42 is often used in examples).
# This resets the internal state of the generator, making the next output predictable.
random.seed(42)
reproducible_roll_1 = random.randint(1, 1000)
random.seed(42) # Re-seeding with the same value
reproducible_roll_2 = random.randint(1, 1000)

print(f"\n[Action 4: Seeding Test] Demonstrating control over the generator.")
print(f"First roll after seed(42): {reproducible_roll_1}")
print(f"Second roll after re-seed(42): {reproducible_roll_2}")

# These two numbers will always be identical across different runs of the program.


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
import string
from typing import List, Tuple, Optional

# --- Exercise 1: The Weighted Dice Roll Simulator ---

def simulate_dice_rolls(trials: int = 10000):
    """
    Simulates rolling two 6-sided dice for a specified number of trials
    and calculates the frequency and probability of each sum (2 through 12).
    """
    print("## Exercise 1: The Weighted Dice Roll Simulator")
    
    NUM_TRIALS = trials
    
    # 1 & 2. Initialize dictionary for sums 2 through 12
    # Dictionary comprehension is efficient for pre-allocating keys.
    roll_counts = {i: 0 for i in range(2, 13)}

    # 3. Implement the loop
    for _ in range(NUM_TRIALS):
        # 4. Simulate rolling two dice using random.randint(1, 6)
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        current_sum = die1 + die2
        
        # 5. Increment the count for that sum
        roll_counts[current_sum] += 1

    # 6. Print the results
    print(f"Simulation completed with {NUM_TRIALS:,} trials.")
    print("Sum | Count | Observed Probability")
    print("-" * 35)
    
    # Calculate and display probabilities
    for sum_val, count in sorted(roll_counts.items()):
        probability = count / NUM_TRIALS
        print(f"{sum_val:3} | {count:5,} | {probability:.4f}")
    print("-" * 35)

# Execute Exercise 1
simulate_dice_rolls(trials=50000)


# --- Exercise 2: Secure Password Generation with Constraints ---

def generate_secure_password(length: int = 12) -> str:
    """
    Generates a secure password guaranteeing at least one char from four required sets.
    """
    print("\n## Exercise 2: Secure Password Generation with Constraints")
    
    # 1. Define character pools using the 'string' module constants
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = string.punctuation
    
    # Combine all pools for the bulk of the password
    ALL_CHARS = LOWERCASE + UPPERCASE + DIGITS + SYMBOLS
    
    # Check minimum length requirement for constraints
    if length < 4:
        raise ValueError("Password length must be at least 4 to meet all constraints.")
    
    # 2. Select mandatory characters (one from each required pool)
    mandatory_chars: List[str] = []
    mandatory_chars.append(random.choice(LOWERCASE))
    mandatory_chars.append(random.choice(UPPERCASE))
    mandatory_chars.append(random.choice(DIGITS))
    mandatory_chars.append(random.choice(SYMBOLS))
    
    # Calculate how many remaining characters are needed
    remaining_length = length - len(mandatory_chars)
    
    # 3. Select the remaining characters from the combined pool
    # Use random.choices for efficient selection of multiple items with replacement
    random_fill = random.choices(ALL_CHARS, k=remaining_length)
    
    # Combine mandatory and random characters
    password_list = mandatory_chars + random_fill
    
    # 4. Shuffle the entire list in-place to randomize the mandatory characters' positions
    random.shuffle(password_list)
    
    # 5. Join the list into a final string
    password = "".join(password_list)
    
    print(f"Generated Password (Length {len(password)}): {password}")
    return password

# Execute Exercise 2
generate_secure_password(length=16)
generate_secure_password(length=10)


# --- Exercise 3: The Lottery Picker and Sampling Without Replacement ---

def run_lottery_draw():
    """
    Simulates a lottery draw and a bonus draw using random.sample()
    for unique selection (sampling without replacement).
    """
    print("\n## Exercise 3: The Lottery Picker and Sampling Without Replacement")
    
    # 1. Generate the pool of lottery numbers (1 through 49 inclusive)
    lottery_pool = list(range(1, 50))
    
    # 2. Use random.sample() to select 6 unique winning numbers
    # k=6 specifies the number of items to sample
    winning_numbers = random.sample(lottery_pool, k=6)
    
    # Sort for display purposes
    winning_numbers.sort()
    
    print(f"Official Winning Lottery Numbers (6 unique from 49): {winning_numbers}")
    
    # 3. Create a list of 20 fictional participant names
    participants = [f"Participant_{chr(65 + i)}" for i in range(20)] # Names A through T
    
    # 4. Use random.sample() again to select 3 unique winners
    bonus_winners = random.sample(participants, k=3)
    
    print(f"\nTotal participants registered: {len(participants)}")
    print(f"Bonus Prize Winners (3 unique names): {bonus_winners}")

# Execute Exercise 3
run_lottery_draw()


# --- Exercise 4: Interactive Challenge: Controlling the Simulation State ---

def run_simulation(seed_value: Optional[int] = None, trials: int = 5) -> Tuple[float, float, str]:
    """
    A simple simulation function demonstrating seed control.
    Generates random floats and calculates their average.
    """
    
    if seed_value is not None:
        # CRITICAL: Setting the seed resets the internal state to a known starting point.
        random.seed(seed_value)
        seed_status = f"Seed Set: {seed_value}"
    else:
        # If no seed is set, the system time is typically used.
        seed_status = "Seed Not Set (Truly Random)"

    results = []
    
    for _ in range(trials):
        # Generate a random float between 0.0 and 1.0
        results.append(random.random())
        
    average = sum(results) / len(results)
    
    # Return the first generated number and the average for easy comparison
    return results[0], average, seed_status

# --- Execution of Challenge Demonstrating Seed Control ---
print("\n## Exercise 4: Interactive Challenge: Controlling the Simulation State")

# Test A: Run twice without seed (Results must differ)
print("\n--- Test A: Running without Seed (Expected: Different Results) ---")
r_a1_first, r_a1_avg, s_a1 = run_simulation(trials=5)
print(f"Run 1 ({s_a1}): First Num={r_a1_first:.6f}, Avg={r_a1_avg:.6f}")

r_a2_first, r_a2_avg, s_a2 = run_simulation(trials=5)
print(f"Run 2 ({s_a2}): First Num={r_a2_first:.6f}, Avg={r_a2_avg:.6f}")

print(f"Comparison: R1 First Num == R2 First Num? {r_a1_first == r_a2_first}")
print("The internal state was advanced by Run 1, and Run 2 started from a new, unknown state.")
print("-" * 50)


# Test B: Run twice with the SAME seed (Expected: Identical Results)
SEED_VAL = 42
print(f"\n--- Test B: Running with Seed={SEED_VAL} (Expected: Identical Results) ---")

# Run 1: Set seed 42
r_b1_first, r_b1_avg, s_b1 = run_simulation(seed_value=SEED_VAL, trials=5)
print(f"Run 1 ({s_b1}): First Num={r_b1_first:.6f}, Avg={r_b1_avg:.6f}")

# Run 2: MUST reset seed 42 before running again to restart the sequence
r_b2_first, r_b2_avg, s_b2 = run_simulation(seed_value=SEED_VAL, trials=5)
print(f"Run 2 ({s_b2}): First Num={r_b2_first:.6f}, Avg={r_b2_avg:.6f}")

print(f"Comparison: R1 First Num == R2 First Num? {r_b1_first == r_b2_first}")
print("Setting the same seed before each run guarantees the exact same deterministic sequence.")
print("-" * 50)


# Test C: Run with a DIFFERENT seed (Expected: Different Results from Test B)
SEED_VAL_2 = 100
print(f"\n--- Test C: Running with Seed={SEED_VAL_2} (Expected: Different from Test B) ---")

r_c1_first, r_c1_avg, s_c1 = run_simulation(seed_value=SEED_VAL_2, trials=5)
print(f"Run 3 ({s_c1}): First Num={r_c1_first:.6f}, Avg={r_c1_avg:.6f}")

print(f"Comparison: Test B (R1) First Num == Test C (R3) First Num? {r_b1_first == r_c1_first}")
print("A new seed generates a new, but still deterministic, sequence.")
print("-" * 50)

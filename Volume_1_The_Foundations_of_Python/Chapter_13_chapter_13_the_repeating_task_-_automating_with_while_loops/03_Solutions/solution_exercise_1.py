
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

# Initial setup for the simulation
TARGET_AMOUNT = 5000
current_balance = 500  # Note: Renamed from initial_balance to reflect the changing state
monthly_contribution = 150
months_elapsed = 0

print(f"Goal: ${TARGET_AMOUNT}. Starting Balance: ${current_balance}. Monthly Deposit: ${monthly_contribution}")

# Loop continues as long as the current balance is less than the target
while current_balance < TARGET_AMOUNT:
    # Simulate one month: add the deposit
    current_balance += monthly_contribution
    
    # Increment the month counter
    months_elapsed += 1
    
    # Optional: Print monthly status (commented out for cleaner final output)
    # print(f"Month {months_elapsed}: Balance is now ${current_balance}")

# After the loop terminates, the target has been reached or exceeded
print("\n--- Simulation Complete ---")
print(f"Target reached in {months_elapsed} months.")
print(f"Final Balance: ${current_balance:.2f}")


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

# 1. Define the total amount
total_amount = 47.88

# 2. Convert to total cents (integer) to ensure precision
# We use round() to handle potential floating-point inaccuracies (e.g., 47.88 * 100 = 4787.999...)
total_cents = round(total_amount * 100)

# Denomination values (in Cents)
TWENTY = 2000
ONE = 100
QUARTER = 25
DIME = 10
NICKEL = 5
PENNY = 1

# Variable to track the remaining amount in cents
remaining_cents = total_cents

# --- 3. Calculate Denominations Sequentially ---

# 3a. Twenties ($20.00 / 2000 cents)
twenties = remaining_cents // TWENTY
remaining_cents = remaining_cents % TWENTY

# 3b. One Dollars ($1.00 / 100 cents)
ones = remaining_cents // ONE
remaining_cents = remaining_cents % ONE

# 3c. Quarters (25 cents)
quarters = remaining_cents // QUARTER
remaining_cents = remaining_cents % QUARTER

# 3d. Dimes (10 cents)
dimes = remaining_cents // DIME
remaining_cents = remaining_cents % DIME

# 3e. Nickels (5 cents)
nickels = remaining_cents // NICKEL
remaining_cents = remaining_cents % NICKEL

# 3f. Pennies (1 cent)
# The final remaining amount should be the number of pennies
pennies = remaining_cents // PENNY
# We don't need a final modulus operation as 'pennies' is the final remainder

# --- 4. Print Results ---
print(f"Total Amount to Dispense: ${total_amount:.2f} ({total_cents} cents)")
print("-" * 35)
print(f" $20 Bills: {twenties}")
print(f" $1 Bills:  {ones}")
print(f" Quarters:  {quarters}")
print(f" Dimes:     {dimes}")
print(f" Nickels:   {nickels}")
print(f" Pennies:   {pennies}")
print("-" * 35)

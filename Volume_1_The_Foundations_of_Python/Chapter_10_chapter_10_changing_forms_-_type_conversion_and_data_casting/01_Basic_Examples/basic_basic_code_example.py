
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

# 1. Setting up the initial data types
# User input is often read as a string, even if it contains only numbers.
raw_score_input = "45"
# The bonus factor is already a float, requiring precise multiplication.
raw_bonus_factor = 2.5

# --- Part 1: String to Integer Conversion (S -> I) ---
print("--- Conversion Step 1: String to Integer ---")
# We use a try/except block to safely handle potential conversion errors.
try:
    # int() attempts to interpret the string contents as a whole number.
    current_score = int(raw_score_input)
    
    # Verification: Use type() to inspect the data type before and after conversion.
    print(f"Original Type (raw_score_input): {type(raw_score_input)}")
    print(f"Converted Type (current_score): {type(current_score)}")
    print(f"Current score value: {current_score}")

except ValueError as e:
    # This block executes if raw_score_input contained non-numeric characters.
    print(f"Error converting score: {e}. Falling back to 0.")
    current_score = 0 # Safety fallback to prevent program crash

# --- Part 2: Integer to Float Conversion (I -> F) ---
print("\n--- Conversion Step 2: Integer to Float & Calculation ---")
# We convert the integer score to a float to ensure the calculation result
# maintains decimal precision when multiplied by the float bonus factor.
score_as_float = float(current_score)

# Perform the calculation. The result of (float * float) is always a float.
final_calculated_score = score_as_float * raw_bonus_factor

print(f"Score as Float value: {score_as_float}")
print(f"Final Calculated Score value: {final_calculated_score}")
print(f"Type after calculation: {type(final_calculated_score)}")

# --- Part 3: Float to String Conversion (F -> S) ---
print("\n--- Conversion Step 3: Float to String for Display ---")
# Data must be converted back to a string before it can be reliably
# concatenated (joined) with other text messages for output.
display_message = "Your final adjusted score is: "
final_score_string = str(final_calculated_score)

# Concatenate the string message with the converted score string
full_output_message = display_message + final_score_string

print(f"Final Display Output: {full_output_message}")
print(f"Type of final output: {type(full_output_message)}")

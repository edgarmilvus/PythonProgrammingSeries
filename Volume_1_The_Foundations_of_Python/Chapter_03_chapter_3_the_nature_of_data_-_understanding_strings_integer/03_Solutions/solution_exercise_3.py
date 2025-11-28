
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

# 1. Input Simulation (All inputs are initially strings)
input_a = "42"          # Target: Integer
input_b = "98.6"        # Target: Float
input_c = "Python_3000" # Target: Remain String

# --- Processing Input A: Integer Conversion ---
print("\n--- Processing Input A ---")
print(f"Initial Value: {input_a}")
print(f"Initial Type: {type(input_a)}")

# Explicitly casting the string to an integer
converted_a = int(input_a)
print(f"Converted Value: {converted_a}")
print(f"New Type: {type(converted_a)}")

# --- Processing Input B: Float Conversion ---
print("\n--- Processing Input B ---")
print(f"Initial Value: {input_b}")
print(f"Initial Type: {type(input_b)}")

# Explicitly casting the string to a float
converted_b = float(input_b)
print(f"Converted Value: {converted_b}")
print(f"New Type: {type(converted_b)}")

# --- Processing Input C: String Retention ---
print("\n--- Processing Input C ---")
print(f"Initial Value: {input_c}")
print(f"Initial Type: {type(input_c)}")

# Conversion logic: Since the string contains non-numeric characters, 
# direct conversion to int or float would raise an error (ValueError).
# We retain the string type.
converted_c = input_c
print("Conversion Failed. Retaining String Type.")
print(f"Final Type: {type(converted_c)}")

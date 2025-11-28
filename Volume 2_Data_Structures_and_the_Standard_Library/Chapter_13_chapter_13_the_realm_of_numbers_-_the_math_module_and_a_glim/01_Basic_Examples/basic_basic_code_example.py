
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

import math # Import the 'math' module to access constants and functions

# --- 1. Setup and Definition ---
# Define the radius of the circle, using a float for necessary precision
radius = 7.5 

# --- 2. Accessing Constants and Calculation ---
# Retrieve the precise value of Pi from the math module
pi_value = math.pi

# Calculate the Circumference (C = 2 * pi * r)
# We use the standard multiplication operator (*)
circumference = 2 * pi_value * radius

# Calculate the Area (A = pi * r^2)
# We use math.pow(base, exponent) for robust exponentiation
area = pi_value * math.pow(radius, 2)

# --- 3. Precision Control (Floor and Ceil) ---
# Use math.floor() to round the circumference down to the nearest whole number
circumference_floor = math.floor(circumference)

# Use math.ceil() to round the area up to the nearest whole number
area_ceil = math.ceil(area)

# --- 4. Output Results ---
print(f"--- Circle Calculation Summary ---")
print(f"Radius (r): {radius} units")
print(f"Value of Pi (math.pi): {pi_value}")
print("-" * 40)
print(f"1. Calculated Circumference (C): {circumference:.6f} units")
print(f"2. Circumference Rounded Down (Floor): {circumference_floor} units")
print(f"3. Calculated Area (A): {area:.6f} square units")
print(f"4. Area Rounded Up (Ceil): {area_ceil} square units")

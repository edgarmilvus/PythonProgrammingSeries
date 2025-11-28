
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

# 1. Setup the initial data source
# We use range(1, 6) to generate numbers 1, 2, 3, 4, and 5.
initial_numbers = range(1, 6)

# --- METHOD 1: Traditional For Loop (Imperative Approach) ---
# This method requires three explicit steps: initialization, iteration, and appending.
squared_list_loop = [] # Step A: Initialize an empty list to store results

# Step B: Iterate through the source data
for number in initial_numbers:
    # Step C: Perform the calculation and append the result
    square = number * number
    squared_list_loop.append(square)

# --- METHOD 2: List Comprehension (Declarative/Pythonic Approach) ---
# Syntax: [expression for item in iterable]
# This achieves the same result in a single, self-contained line.
squared_list_comp = [n * n for n in initial_numbers]

# Display results for verification
print(f"Original sequence: {list(initial_numbers)}")
print("-" * 30)
print(f"Result via For Loop: {squared_list_loop}")
print(f"Result via List Comprehension: {squared_list_comp}")

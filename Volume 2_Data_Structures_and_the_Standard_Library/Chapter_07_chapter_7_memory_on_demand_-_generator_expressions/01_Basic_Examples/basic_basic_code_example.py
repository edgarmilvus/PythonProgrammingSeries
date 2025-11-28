
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

# Define a small input range for demonstration purposes (1 to 5)
data_range = range(1, 6) 

# --- Part 1: List Comprehension (Eager Evaluation) ---
print("--- 1. List Comprehension (Eager Storage) ---")

# LC uses square brackets [] and calculates all results immediately
eager_results = [x * x for x in data_range]

# Check the type and content
print(f"Type of eager_results: {type(eager_results)}")
print(f"Content (fully stored): {eager_results}")


# --- Part 2: Generator Expression (Lazy Evaluation) ---
print("\n--- 2. Generator Expression (Lazy Generation) ---")

# GE uses parentheses () and computes nothing yet; it creates an iterator (a recipe)
lazy_generator = (x * x for x in data_range)

# Check the type and initial state
print(f"Type of lazy_generator: {type(lazy_generator)}")
# Note: Printing the generator object shows its memory location/state, not its content
print(f"Initial state (object reference, not data): {lazy_generator}")

# Accessing values forces calculation, one by one, on demand
print("\n3. Iterating through the Generator (Forcing Calculation):")
for result in lazy_generator:
    print(f"Generated value: {result}")

# --- Part 3: Demonstrating Exhaustion ---
print("\n4. Generator Exhaustion Check:")
# Attempting to iterate again on the same generator
re_iteration_attempt = list(lazy_generator)
print(f"Attempted re-iteration results: {re_iteration_attempt}")

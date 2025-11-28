
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

import time
import sys
import random

# --- Exercise 7-1: Syntax Conversion and Type Inspection ---

# 1. List Comprehension (Immediate Execution)
cubes_list = [x**3 for x in range(1, 26)]

# 2. Generator Expression (Lazy Iterator)
cubes_generator = (x**3 for x in range(1, 26))

print("--- Exercise 7-1 Results ---")
# 3. Print the type of the resulting objects
print(f"Type of cubes_list: {type(cubes_list)}")
print(f"Type of cubes_generator: {type(cubes_generator)}")

# 4. Print the first five elements of the list
print("\nList Elements (Accessed via indexing):")
print(cubes_list[:5])

# 5. Print the first five elements of the generator using next()
print("\nGenerator Elements (Accessed via next()):")
print(f"Next 1: {next(cubes_generator)}")
print(f"Next 2: {next(cubes_generator)}")
print(f"Next 3: {next(cubes_generator)}")
print(f"Next 4: {next(cubes_generator)}")
print(f"Next 5: {next(cubes_generator)}")


# --- Exercise 7-2: Scaling Challenge ---

MILLION = 10_000_000
DIVISOR = 99999

def filter_list_comp():
    """Uses a List Comprehension to filter 10 million items."""
    # This executes immediately, calculating and storing the result list.
    return [i for i in range(1, MILLION + 1) if i % DIVISOR == 0]

def filter_generator_exp():
    """Uses a Generator Expression to define the filtering logic lazily."""
    # This executes instantly, returning only the iterator object.
    return (i for i in range(1, MILLION + 1) if i % DIVISOR == 0)

print("\n--- Exercise 7-2 Results (Scaling) ---")

# Timing the List Comprehension creation
start_lc = time.perf_counter()
result_list = filter_list_comp()
end_lc = time.perf_counter()
lc_time = end_lc - start_lc

print(f"List Comp Creation Time: {lc_time:.4f} seconds")
print(f"List Comp Result Count: {len(result_list)}")
# Note: The list is fully calculated and stored in memory at this point.

# Timing the Generator Expression creation
start_ge = time.perf_counter()
result_generator = filter_generator_exp()
end_ge = time.perf_counter()
ge_time = end_ge - start_ge

print(f"Generator Exp Creation Time: {ge_time:.8f} seconds (Near instantaneous)")
# Note: The generator is not yet calculated. We must iterate to see results.

# Forcing the generator to execute and printing results
print("\nGenerator results (forcing execution via iteration):")
# We use list() here only to quickly iterate and print the results
# In a real-world scenario, we would stream these results.
generator_results = list(result_generator)
print(generator_results)
print(f"Generator Result Count: {len(generator_results)}")


# --- Exercise 7-3: Chaining and Conditionals ---

readings = [
    -1.5, 3.1, 0.0, 4.2, 1.1, 5.0, -2.0, 2.5, 2.6, 6.0, 1.9, 3.0
]

# Generator Expression with two sequential filters
# 1. Filter: x > 0 (Positive)
# 2. Filter: x > 2.5 (Greater than threshold)
# Expression: x**2 (Square the result)
squared_sum_generator = (
    x**2 
    for x in readings 
    if x > 0 
    if x > 2.5
)

# Use sum() to consume the generator in a single pass
final_sum = sum(squared_sum_generator)

print("\n--- Exercise 7-3 Results (Chaining) ---")
print(f"Original Readings: {readings}")
print(f"Calculated Sum of Squares (x > 2.5 and x > 0): {final_sum:.2f}")


# --- Exercise 7-4: Interactive Challenge - Data Sanitization ---

SENSITIVE_ID = 'USER_ID_######'
REDACTED_TOKEN = '[REDACTED]'
LOG_COUNT = 500_000

def simulate_log_lines(count):
    """Simulates yielding log lines, some containing sensitive data."""
    for i in range(count):
        if i % 10 == 0:
            # Simulate a line that needs sanitization
            yield f"Timestamp: {i} - CRITICAL ERROR - ID: {SENSITIVE_ID} occurred."
        else:
            # Simulate a normal log line
            yield f"Timestamp: {i} - Info message processed successfully."

# 1. Define the Generator Expression to calculate lengths lazily
# The expression calculates the length of the string after sanitization.
sanitized_lengths = (
    len(line.replace(SENSITIVE_ID, REDACTED_TOKEN))
    for line in simulate_log_lines(LOG_COUNT)
)

# 2. Use sum() to aggregate the lengths without storing any intermediate list
total_characters = sum(sanitized_lengths)

print("\n--- Exercise 7-4 Results (Interactive Challenge) ---")
print(f"Processed {LOG_COUNT:,} simulated log lines.")
print(f"Total characters of all sanitized logs (calculated via generator sum): {total_characters:,}")


# --- Exercise 7-5: Benchmarking Generator vs. List Performance ---

SIZE = 500_000
data_range = range(SIZE)

# 1. Define List Comprehension (Immediate calculation)
start_list_creation = time.perf_counter()
squares_list = [x * x for x in data_range]
end_list_creation = time.perf_counter()

print("\n--- Exercise 7-5 Results (Benchmarking) ---")
print(f"Time to CREATE List Comp: {end_list_creation - start_list_creation:.6f} s")

# 3. Measure time for two iterations on the List
start_list_iter = time.perf_counter()
sum1_list = sum(squares_list) # Iteration 1
sum2_list = sum(squares_list) # Iteration 2 (Fast, data is already in RAM)
end_list_iter = time.perf_counter()
list_total_time = end_list_iter - start_list_iter

print(f"List Comp Iteration 1 Sum: {sum1_list}")
print(f"List Comp Total Time (2 iterations): {list_total_time:.6f} s")

# 2. Define Generator Expression (Lazy definition)
start_gen_creation = time.perf_counter()
squares_gen_1 = (x * x for x in data_range)
end_gen_creation = time.perf_counter()

print(f"\nTime to CREATE Generator Exp: {end_gen_creation - start_gen_creation:.6f} s (Significantly faster)")

# 4. Measure time for two iterations on the Generator
start_gen_iter = time.perf_counter()

# Iteration 1: Calculation happens now
sum1_gen = sum(squares_gen_1) 

# Iteration 2: The generator is exhausted. We must redefine it.
squares_gen_2 = (x * x for x in data_range) 
sum2_gen = sum(squares_gen_2) 

end_gen_iter = time.perf_counter()
gen_total_time = end_gen_iter - start_gen_iter

print(f"Generator Exp Iteration 1 Sum: {sum1_gen}")
print(f"Generator Exp Total Time (2 iterations, including re-creation): {gen_total_time:.6f} s")

print("\n--- Comparison Summary ---")
print(f"List Comp (Creation + 2 Iterations): {(end_list_creation - start_list_creation) + list_total_time:.6f} s")
print(f"Generator Exp (Creation + 2 Iterations): {(end_gen_creation - start_gen_creation) + gen_total_time:.6f} s")

# Explanation of the observed difference
if list_total_time < gen_total_time:
    print("\nObservation: The List Comprehension was faster for repeated access.")
else:
    print("\nObservation: The Generator Expression was faster overall (due to specific system factors or low iteration cost).")
print("Crucial takeaway: The List stores data for instant reuse, while the Generator must recalculate data for every iteration, even if its initial setup time is negligible.")

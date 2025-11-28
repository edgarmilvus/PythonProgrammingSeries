
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

import time
import sys
import random

# --- Exercise 7-1: Syntax Conversion and Type Inspection ---

# 1. Define a List Comprehension (Eager execution)
# Calculates and stores all 25 cubes immediately.
cubes_list = [x**3 for x in range(1, 26)]

# 2. Define a Generator Expression (Lazy definition)
# Creates an iterator that knows how to calculate cubes when asked.
cubes_generator = (x**3 for x in range(1, 26))

print("--- Exercise 7-1 Results: Syntax and Type Inspection ---")

# 3. Print the type of both objects
print(f"Type of cubes_list: {type(cubes_list)}")
print(f"Type of cubes_generator: {type(cubes_generator)}")

# 4. Print the first five elements of the list (using standard indexing)
print("\nList Elements (Accessed via indexing):")
print(cubes_list[:5])

# 5. Print the first five elements of the generator using next()
# Note: These values are consumed from the generator stream.
print("\nGenerator Elements (Accessed via next()):")
print(f"Next 1: {next(cubes_generator)}")
print(f"Next 2: {next(cubes_generator)}")
print(f"Next 3: {next(cubes_generator)}")
print(f"Next 4: {next(cubes_generator)}")
print(f"Next 5: {next(cubes_generator)}")


# --- Exercise 7-2: Scaling Challenge - Simulating Massive Log Processing ---

MILLION = 10_000_000
DIVISOR = 99999

def filter_list_comp():
    """Uses a List Comprehension. Execution is immediate and memory intensive."""
    # This calculation happens entirely during the function call.
    return [i for i in range(1, MILLION + 1) if i % DIVISOR == 0]

def filter_generator_exp():
    """Uses a Generator Expression. Definition is instant, calculation is lazy."""
    # Only returns a lightweight iterator object instantly.
    return (i for i in range(1, MILLION + 1) if i % DIVISOR == 0)

print("\n--- Exercise 7-2 Results: Scaling Challenge ---")

# Timing the List Comprehension creation (eager execution)
start_lc = time.perf_counter()
result_list = filter_list_comp()
end_lc = time.perf_counter()
lc_time = end_lc - start_lc

print(f"List Comp Creation Time (Eager): {lc_time:.4f} seconds")
print(f"List Comp Result Count: {len(result_list)}")

# Timing the Generator Expression creation (lazy definition)
start_ge = time.perf_counter()
result_generator = filter_generator_exp()
end_ge = time.perf_counter()
ge_time = end_ge - start_ge

print(f"Generator Exp Creation Time (Lazy): {ge_time:.8f} seconds (Near instantaneous)")

# 4. Force the generator to execute to confirm results
# Note: This is where the calculation time is actually spent for the generator.
print("\nGenerator results (forcing execution via list() conversion):")
generator_results = list(result_generator)
print(generator_results)
print(f"Generator Result Count: {len(generator_results)}")


# --- Exercise 7-3: Chaining Generators for Complex Filtering ---

readings = [
    -1.5, 3.1, 0.0, 4.2, 1.1, 5.0, -2.0, 2.5, 2.6, 6.0, 1.9, 3.0
]

# Use a single Generator Expression passed directly to sum()
# The generator performs two sequential filters and then the squaring operation.
squared_sum_generator = (
    x**2 
    for x in readings 
    if x > 0       # Filter 1: Must be positive
    if x > 2.5     # Filter 2: Must be greater than 2.5
)

# Use sum() to consume the generator in a single, memory-efficient pass
final_sum = sum(squared_sum_generator)

print("\n--- Exercise 7-3 Results: Chaining Generators ---")
print(f"Original Readings: {readings}")
print(f"Calculated Sum of Squares (x > 2.5): {final_sum:.2f}")


# --- Exercise 7-4: Interactive Challenge - Enhancing the Data Sanitizer ---

SENSITIVE_ID = 'USER_ID_######'
REDACTED_TOKEN = '[REDACTED]'
LOG_COUNT = 500_000

def simulate_log_lines(count):
    """Simulates yielding log lines."""
    for i in range(count):
        if i % 10 == 0:
            # Yield sensitive line
            yield f"Timestamp: {i} - CRITICAL ERROR - ID: {SENSITIVE_ID} occurred."
        else:
            # Yield normal line
            yield f"Timestamp: {i} - Info message processed successfully."

# 1. Create a Generator Expression that calculates the length of the sanitized line
# The generator performs sanitization and then yields the length (an integer).
sanitized_lengths = (
    len(line.replace(SENSITIVE_ID, REDACTED_TOKEN))
    for line in simulate_log_lines(LOG_COUNT)
)

# 2. Use sum() to aggregate the lengths in a single pass, avoiding list creation.
total_characters = sum(sanitized_lengths)

print("\n--- Exercise 7-4 Results: Data Sanitization ---")
print(f"Processed {LOG_COUNT:,} simulated log lines.")
print(f"Total characters of all sanitized logs: {total_characters:,}")


# --- Exercise 7-5: Benchmarking Generator vs. List Performance ---

SIZE = 500_000
data_range = range(SIZE)

# 1. Define List Comprehension (Eager calculation)
start_list_creation = time.perf_counter()
squares_list = [x * x for x in data_range]
end_list_creation = time.perf_counter()

print("\n--- Exercise 7-5 Results: Benchmarking Performance ---")
print(f"Time to CREATE List Comp: {end_list_creation - start_list_creation:.6f} s")

# 3. Measure time for two iterations on the List
start_list_iter = time.perf_counter()
sum1_list = sum(squares_list) # Iteration 1 (Reading from memory)
sum2_list = sum(squares_list) # Iteration 2 (Reading from memory, very fast)
end_list_iter = time.perf_counter()
list_total_time = end_list_iter - start_list_iter

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

# Iteration 2: Generator is exhausted. Must redefine the expression.
squares_gen_2 = (x * x for x in data_range) 
sum2_gen = sum(squares_gen_2) 

end_gen_iter = time.perf_counter()
gen_total_time = end_gen_iter - start_gen_iter

print(f"Generator Exp Total Time (2 iterations, including re-creation): {gen_total_time:.6f} s")

print("\n--- Summary of Trade-offs ---")
print("List Comp (Fast repeated access, high initial memory/time cost).")
print("Generator Exp (Slow repeated access, zero initial memory/time cost).")

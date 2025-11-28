
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

import cProfile
import time
import sys
import pstats
from io import StringIO

# Increase recursion limit for the deep Fibonacci calls
# This is necessary when calculating Fib(35) recursively.
sys.setrecursionlimit(2000)

# 1. The deliberately inefficient function
def calculate_fibonacci(n):
    """
    Calculates the n-th Fibonacci number recursively.
    This function is intentionally inefficient (O(2^n)) to demonstrate profiling.
    """
    if n <= 1:
        return n
    # The costly part: two recursive calls leading to exponential redundancy
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

# 2. The workload function that encapsulates the expensive operation
def run_simulation(max_n=35):
    """
    Runs the expensive calculation once to generate sufficient load
    for the profiler to capture meaningful data.
    """
    start_time = time.perf_counter()
    print(f"Calculating Fibonacci({max_n})... This may take a moment.")
    
    # Execute the function we suspect is the bottleneck
    result = calculate_fibonacci(max_n)
    
    end_time = time.perf_counter()
    print(f"Result: {result}")
    print(f"Total execution time (unprofiled): {end_time - start_time:.4f} seconds")
    return result

# 3. Main execution block for profiling setup and analysis
if __name__ == "__main__":
    
    # Define the profiler object
    profiler = cProfile.Profile()
    
    # Start the profiler, execute the target function, and stop the profiler
    profiler.enable()
    run_simulation(35) 
    profiler.disable()
    
    # --- Analysis and Reporting ---
    
    # Create an in-memory stream to capture the profiling statistics
    s = StringIO()
    
    # Create a Stats object from the profiler data
    # The 'stream=s' directs the output to our in-memory buffer
    stats = pstats.Stats(profiler, stream=s)
    
    # Sort the statistics. We often sort by 'cumulative time' (cumtime) 
    # to find the functions that take the longest overall, including sub-calls.
    stats.sort_stats('cumtime')
    
    # Print the top 10 lines of the report
    print("\n--- PERFORMANCE PROFILE REPORT (Top 10 by Cumulative Time) ---")
    stats.print_stats(10)
    
    # Print the results captured in the StringIO buffer
    print(s.getvalue())
    
    # Optional: Save the raw data to a file for later, deeper analysis
    profiler.dump_stats('fibonacci_profile_data.prof')
    print("\nRaw profiling data saved to 'fibonacci_profile_data.prof'.")


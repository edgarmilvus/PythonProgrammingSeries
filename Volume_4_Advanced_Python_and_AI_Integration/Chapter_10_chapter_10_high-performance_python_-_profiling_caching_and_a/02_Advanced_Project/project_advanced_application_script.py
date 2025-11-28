
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import time
import math
import functools
import cProfile
import pstats
import io

# --- 1. Core Optimization: Caching (Memoization) ---

@functools.lru_cache(maxsize=512)
def fibonacci_optimized(n: int) -> int:
    """
    Calculates the nth Fibonacci number using recursion. 
    The @lru_cache decorator ensures that results for 'n' are stored, 
    preventing exponential recalculation when the function is called 
    with the same input 'n' multiple times, both externally and internally.
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    # Recursive calls automatically check the cache before computing
    return fibonacci_optimized(n - 1) + fibonacci_optimized(n - 2)

# --- 2. Baseline Slow Function (Uncached Bottleneck) ---

def calculate_prime_factors(number: int) -> list[int]:
    """
    Finds all prime factors of a number. This function is CPU-intensive 
    and serves as the unavoidable, non-cacheable part of the calculation.
    """
    factors = []
    d = 2
    temp = number
    # Standard trial division algorithm
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    # Simulate minor IO/processing overhead to make profiling results clearer
    time.sleep(0.00005 * len(factors)) 
    return factors

# --- 3. Orchestrator Function ---

def get_complexity_score(transaction_id: int) -> tuple[int, int]:
    """
    Calculates a composite score, chaining the expensive factor calculation 
    with the potentially cached Fibonacci calculation.
    """
    # Step A: Calculate prime factors (always executed)
    factors = calculate_prime_factors(transaction_id)
    factor_sum = sum(factors)
    
    # Step B: Calculate Fibonacci based on factor sum (highly cacheable input)
    # We use a modulo operation to ensure the index stays within a reasonable, 
    # frequently repeating range for effective caching demonstration.
    fib_index = factor_sum % 30 
    fib_value = fibonacci_optimized(fib_index)
    
    return factor_sum, fib_value

# --- 4. Simulation Driver and Profiling Wrapper ---

def run_simulation(data_inputs: list[int], profile_name: str):
    """
    Executes the scoring simulation, timing the overall process, and capturing 
    detailed statistics using cProfile.
    """
    print(f"\n{'='*50}\n--- Starting Simulation: {profile_name} ---\n{'='*50}")
    
    results = []
    
    # Initialize profiler and enable tracing
    pr = cProfile.Profile()
    pr.enable()
    
    start_time = time.perf_counter()
    
    # Main loop execution
    for tx_id in data_inputs:
        score, fib = get_complexity_score(tx_id)
        results.append((tx_id, score, fib))
        
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    pr.disable()
    
    # --- 5. Profiling Reporting ---
    
    # Use StringIO to capture the output of pstats in memory
    s = io.StringIO()
    # Create statistics object, sort by cumulative time, print top 15 lines
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(15) 
    
    print(f"\nTotal Execution Time: {duration:.4f} seconds")
    print(f"Total Transactions Processed: {len(data_inputs)}")
    print("\n--- Top 15 Profiling Results (Sorted by Cumulative Time) ---")
    print(s.getvalue())
    
    # Report cache status
    cache_info = fibonacci_optimized.cache_info()
    print(f"Fibonacci Cache Status: {cache_info}")
    
    # Calculate and display the hit rate
    total_calls = cache_info.hits + cache_info.misses
    if total_calls > 0:
        hit_rate = (cache_info.hits / total_calls) * 100
        print(f"Cache Hit Rate: {hit_rate:.2f}%")
    else:
        print("Cache Hit Rate: N/A (No calls recorded)")


# --- 6. Main Execution Block ---

if __name__ == "__main__":
    
    # Define a dataset with 90 transactions, featuring many repetitions 
    # and inputs that yield the same factor sum (e.g., 154 and 308/2).
    base_data = [
        154, 154, 308, 155, 154, 155, 155, 100, 100, 
        210, 210, 210, 154, 155, 100, 100, 100, 155, 
        420, 420, 154, 155, 154, 155, 100, 100, 155, 
        154, 154, 308, 155, 154, 155, 155, 100, 100, 
        210, 210, 210, 154, 155, 100, 100, 100, 155, 
        420, 420, 154, 155, 154, 155, 100, 100, 155, 
        154, 154, 308, 155, 154, 155, 155, 100, 100, 
        210, 210, 210, 154, 155, 100, 100, 100, 155, 
        420, 420, 154, 155, 154, 155, 100, 100, 155, 
    ]
    
    # Run 1: Cold Cache Initialization (High recursive overhead expected)
    run_simulation(base_data, "Run 1: Cold Cache Initialization (Baseline)")
    
    # Run 2: Warm Cache Optimization Test (Significant speedup expected)
    run_simulation(base_data, "Run 2: Warm Cache Optimization Test (Optimized)")

    # Final verification of cache status
    print("\n--- Final Cache State Verification ---")
    print(f"Final Fibonacci Cache Status: {fibonacci_optimized.cache_info()}")


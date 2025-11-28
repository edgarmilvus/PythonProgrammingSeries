
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

import cProfile
import pstats
import io
import time
import functools
import math
import random
import os
import sys

# --- Helper function for profiling output formatting ---
def profile_run(func, *args, **kwargs):
    """Runs a function using cProfile and prints sorted results."""
    pr = cProfile.Profile()
    pr.enable()
    func(*args, **kwargs)
    pr.disable()
    
    s = io.StringIO()
    # Sort by cumulative time for easy bottleneck identification
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(15) # Print top 15 results
    
    print("\n--- cProfile Analysis (Top 15 Cumulative Time) ---")
    print(s.getvalue())

# ==============================================================================
# Exercise 1: Profiling a Complex Numerical Simulation
# ==============================================================================

def matrix_iteration(size, iterations):
    """Simulates heavy, repeated matrix calculation."""
    result = 0.0
    for i in range(iterations):
        for j in range(size):
            # Complex float arithmetic
            result += math.sin(i * j / 1000.0) * math.cos(j / 500.0)
    return result

def calculate_system_stability():
    """Wrapper function simulating a complex workload."""
    print("Running Stability Calculation...")
    
    # Workload 1: Small iterations, large size
    res1 = matrix_iteration(500, 1000)
    
    # Workload 2: Large iterations, medium size (The expected bottleneck)
    res2 = matrix_iteration(300, 5000)
    
    # Workload 3: Quick check
    res3 = matrix_iteration(100, 100)
    
    return res1 + res2 + res3

print("--- Running Exercise 1: Profiling ---")
profile_run(calculate_system_stability)

# Analysis Conclusion:
# The 'matrix_iteration' function consumes the vast majority of the total time (tottime and cumtime), 
# confirming it as the primary CPU bottleneck requiring optimization.

# ==============================================================================
# Exercise 2: Caching the Weighted Path Sum
# ==============================================================================

def weighted_path_sum_inefficient(n):
    """Recursive function without caching."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    # f(n) = f(n-1) + 2*f(n-2)
    return weighted_path_sum_inefficient(n - 1) + 2 * weighted_path_sum_inefficient(n - 2)

@functools.lru_cache(maxsize=None)
def cached_weighted_path_sum(n):
    """Recursive function with LRU caching."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    # f(n) = f(n-1) + 2*f(n-2)
    return cached_weighted_path_sum(n - 1) + 2 * cached_weighted_path_sum(n - 2)

N_TARGET = 30
print("\n--- Running Exercise 2: Caching Comparison ---")

# Baseline timing
start_time_ineff = time.perf_counter()
result_ineff = weighted_path_sum_inefficient(N_TARGET)
end_time_ineff = time.perf_counter()
time_ineff = end_time_ineff - start_time_ineff
print(f"Inefficient Sum ({N_TARGET}): {result_ineff}")
print(f"Inefficient Time: {time_ineff:.4f} seconds")

# Cached timing
start_time_cached = time.perf_counter()
result_cached = cached_weighted_path_sum(N_TARGET)
end_time_cached = time.perf_counter()
time_cached = end_time_cached - start_time_cached
print(f"Cached Sum ({N_TARGET}): {result_cached}")
print(f"Cached Time: {time_cached:.8f} seconds")

if time_cached > 0 and time_ineff > 0:
    speedup = time_ineff / time_cached
    print(f"Speedup Factor: {speedup:.2f}x (Expected: Thousands of times)")
else:
    print("Speedup calculation skipped (timing error or time too small).")


# ==============================================================================
# Exercise 3: Hybrid Optimization Challenge (I/O vs. Computation)
# ==============================================================================

def heavy_calculation(limit):
    """A CPU-bound function."""
    total = 0
    for i in range(limit):
        total += i * i
    return total

def fetch_and_process_data_uncached(key):
    """Hybrid function: I/O sleep followed by computation."""
    # Simulated I/O latency (I/O-bound part)
    time.sleep(0.05) 
    # CPU calculation (CPU-bound part)
    result = heavy_calculation(100000)
    return result + key

@functools.lru_cache(maxsize=10)
def fetch_and_process_data_cached(key):
    """Hybrid function with caching applied."""
    # Simulated I/O latency
    time.sleep(0.05) 
    # CPU calculation
    result = heavy_calculation(100000)
    return result + key

def run_hybrid_test(func, num_runs):
    """Runs the hybrid function multiple times with the same key."""
    # Clear cache before running cached test to ensure first call runs fully
    if hasattr(func, 'cache_clear'):
        func.cache_clear()
        
    start_time = time.perf_counter()
    for _ in range(num_runs):
        func(key=42) # Use the same key repeatedly
    end_time = time.perf_counter()
    return end_time - start_time

NUM_RUNS = 10
print("\n--- Running Exercise 3: Hybrid Optimization ---")

# 1. Profiling Baseline (Uncached)
print("1. Profiling Uncached Run (10 calls):")
profile_run(run_hybrid_test, fetch_and_process_data_uncached, NUM_RUNS)

# 2. Timing Uncached
time_uncached = run_hybrid_test(fetch_and_process_data_uncached, NUM_RUNS)
print(f"Uncached Total Time: {time_uncached:.4f} seconds")

# 3. Timing Cached
time_cached = run_hybrid_test(fetch_and_process_data_cached, NUM_RUNS)
print(f"Cached Total Time: {time_cached:.4f} seconds")

# Conclusion:
# The cached run is drastically faster because the cache bypasses both the heavy CPU calculation 
# and the time.sleep I/O simulation for all calls after the first one.

# ==============================================================================
# Exercise 4: Cythonizing a Numerical Aggregation Loop (Simulation)
# ==============================================================================

def py_euclidean_distance(v1, v2):
    """Pure Python implementation of Euclidean distance."""
    if len(v1) != len(v2):
        raise ValueError("Vectors must have the same length.")
    
    sum_sq = 0.0
    for i in range(len(v1)):
        diff = v1[i] - v2[i]
        sum_sq += diff * diff
    return math.sqrt(sum_sq)

# --- Simulation of the Compiled Cython Function ---
# In a real environment, this function would be imported from a compiled .so or .pyd file.
def cy_euclidean_distance_SIMULATED(v1, v2):
    """Placeholder for the compiled Cython function."""
    # For timing simulation, we run the Python version but adjust the final time.
    return py_euclidean_distance(v1, v2) 

VECTOR_SIZE = 100000
NUM_TESTS = 50
VEC_A = [random.random() for _ in range(VECTOR_SIZE)]
VEC_B = [random.random() for _ in range(VECTOR_SIZE)]

print("\n--- Running Exercise 4: Cython Timing Simulation ---")

# Timing Pure Python
start_py = time.perf_counter()
for _ in range(NUM_TESTS):
    py_euclidean_distance(VEC_A, VEC_B)
end_py = time.perf_counter()
time_py = end_py - start_py
print(f"Pure Python Total Time: {time_py:.4f} s")

# Timing Cython (Simulated speedup factor of 5x)
start_cy_sim = time.perf_counter()
for _ in range(NUM_TESTS):
    cy_euclidean_distance_SIMULATED(VEC_A, VEC_B)
end_cy_sim = time.perf_counter()

# Apply the simulated speedup factor to the measured time
time_cy_sim = (end_cy_sim - start_cy_sim) / 5.0 
print(f"Cython (Simulated) Total Time: {time_cy_sim:.4f} s")

if time_cy_sim > 0:
    speedup_simulated = time_py / time_cy_sim
    print(f"Simulated Speedup Factor: {speedup_simulated:.2f}x")


# ==============================================================================
# Exercise 5: Interactive Challenge - Optimizing the LLM Feature Extractor
# ==============================================================================

# 1. Simulate the Slow Function (Uncached)
def feature_extract_and_normalize_uncached(text_chunk):
    """Simulates an expensive, non-cached feature extraction process."""
    # Heavy CPU load
    for _ in range(50000):
        _ = math.sqrt(random.random())
        
    # Simulated I/O or model lookup
    time.sleep(0.005) 
    
    # Return a simple hash to simulate the feature vector
    return hash(text_chunk) % 1000

# 2. Optimization: Apply Caching
@functools.lru_cache(maxsize=256)
def feature_extract_and_normalize_cached(text_chunk):
    """The optimized feature extractor using LRU cache."""
    # Heavy CPU load
    for _ in range(50000):
        _ = math.sqrt(random.random())
        
    # Simulated I/O or model lookup
    time.sleep(0.005) 
    
    # Return a simple hash to simulate the feature vector
    return hash(text_chunk) % 1000

def create_redundant_batch(size=100, redundancy_percent=0.5):
    """Creates a batch where a portion of the data is duplicated."""
    # 50 unique chunks, 50 duplicates
    unique_size = int(size * (1 - redundancy_percent))
    
    unique_chunks = [f"Text chunk {i} for LLM processing." for i in range(unique_size)]
    
    # Fill the rest with duplicates
    batch = unique_chunks + random.choices(unique_chunks, k=size - unique_size)
    random.shuffle(batch)
    return batch

def process_batch(extractor_func, batch):
    """Processes the entire batch using the given extractor function."""
    results = []
    for chunk in batch:
        results.append(extractor_func(chunk))
    return results

BATCH_SIZE = 100
REDUNDANCY = 0.5
test_batch = create_redundant_batch(BATCH_SIZE, REDUNDANCY)

print("\n--- Running Exercise 5: LLM Feature Extractor Optimization ---")

# Baseline Run (Profiling)
print("1. Profiling Uncached Batch Processing:")
profile_run(process_batch, feature_extract_and_normalize_uncached, test_batch)

start_time_uncached = time.perf_counter()
process_batch(feature_extract_and_normalize_uncached, test_batch)
end_time_uncached = time.perf_counter()
time_uncached = end_time_uncached - start_time_uncached
print(f"Uncached Processing Time: {time_uncached:.4f} seconds")

# Optimized Run (Timing)
start_time_cached = time.perf_counter()
process_batch(feature_extract_and_normalize_cached, test_batch)
end_time_cached = time.perf_counter()
time_cached = end_time_cached - start_time_cached
print(f"Cached Processing Time: {time_cached:.4f} seconds")

if time_cached > 0:
    speedup_factor = time_uncached / time_cached
    print(f"Speedup Factor observed: {speedup_factor:.2f}x (Targeting ~2.0x for 50% redundancy)")

# Verification: Clear the cache for clean re-runs if needed
feature_extract_and_normalize_cached.cache_clear()

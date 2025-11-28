
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

import math
import time
import random

def measure_scalar_performance(N: int):
    """
    Measures the time taken to calculate the square root of N numbers using standard Python scalar operations.
    
    Args:
        N: The number of elements in the dataset (integer).
    """
    
    print("\n--- Exercise 5: Efficiency Spotlight ---")
    print(f"Generating {N:,} random numbers...")
    
    # 1. Generate a large list of random floats
    # This generation time is excluded from the measurement
    data = [random.uniform(1.0, 1000.0) for _ in range(N)]
    results = []
    
    print("Starting scalar square root calculation...")
    
    # 2. Record start time
    start_time = time.time()
    
    # 3. Iterate through the list and calculate square root using math.sqrt (scalar operation)
    for number in data:
        results.append(math.sqrt(number))
        
    # 4. Record end time
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    # 5. Print results
    print(f"Calculation finished. Processed {len(results):,} results.")
    print(f"Total elapsed time: {elapsed_time:.3f} seconds")
    
    # 6. Conclusion explaining the bottleneck
    print("\n--- Efficiency Context ---")
    print("The measured time is dominated by the overhead of the Python 'for' loop.")
    print("A vectorized library (NumPy) avoids this overhead by performing the")
    print("square root operation on the entire array simultaneously at C-speed,")
    print("resulting in execution orders of magnitude faster.")

# Test case
measure_scalar_performance(1_000_000)

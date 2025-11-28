
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

import math

def calculate_storage_needs(N: int):
    """
    Calculates permutations (N!) and estimates storage needs using math.ceil and math.floor.
    
    Args:
        N: The number of items to permute (integer).
    """
    # 1. Calculate total permutations P = N!
    permutations = math.factorial(N)
    
    # Define storage capacity per unit (use float for division)
    UNIT_CAPACITY = 1_000_000.0
    
    # 2. Calculate raw storage units needed
    raw_units = permutations / UNIT_CAPACITY
    
    # 3. Determine minimum safe integer units (must round UP using ceil)
    safe_units_ceil = math.ceil(raw_units)
    
    # 4. Determine maximum number of full units (must round DOWN using floor)
    full_units_floor = math.floor(raw_units)
    
    print("\n--- Exercise 3: Storage Estimation ---")
    print(f"Permutation Set Size (N): {N}")
    # Use comma formatting for readability of large numbers
    print(f"Total Permutations (P):   {permutations:,}")
    print(f"Raw Storage Units Needed: {raw_units:.4f}")
    # Convert back to integer for printing, using comma formatting
    print(f"Minimum Safe Units (ceil): {int(safe_units_ceil):,}")
    print(f"Maximum Full Units (floor): {int(full_units_floor):,}")

# Test case
calculate_storage_needs(14)

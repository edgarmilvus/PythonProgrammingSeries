
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

import math

def is_prime_optimized(n):
    """
    Checks if a number N is prime using optimization and the for...else construct.
    Returns True if prime, False otherwise.
    """
    # Requirement 1: Handle edge cases
    if n <= 1:
        return False
    
    # 2 is the only even prime number
    if n == 2:
        return True

    # Optimization: Skip all even numbers greater than 2
    if n % 2 == 0:
        return False
    
    # Requirement 2 & 3: Iterate through potential odd divisors up to the square root
    # We use int(math.sqrt(n)) + 1 to ensure we check the boundary divisor
    limit = int(math.sqrt(n))
    
    # Iterate only over odd numbers (step of 2)
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            # Requirement 4: Divisor found, stop immediately and return False
            # Returning False implicitly terminates the loop and prevents the else block execution
            print(f"DEBUG: Found divisor {i} for {n}. Search terminated.")
            return False
            
    # Requirement 5: The else block executes only if the loop completed naturally 
    # (i.e., no divisors were found, and no return False was executed).
    else:
        return True

print("--- Exercise 1: Prime Detector ---")
print(f"Is 29 prime? {is_prime_optimized(29)}")
print(f"Is 100 prime? {is_prime_optimized(100)}")
print(f"Is 97 prime? {is_prime_optimized(97)}")
print(f"Is 9 prime? {is_prime_optimized(9)}")

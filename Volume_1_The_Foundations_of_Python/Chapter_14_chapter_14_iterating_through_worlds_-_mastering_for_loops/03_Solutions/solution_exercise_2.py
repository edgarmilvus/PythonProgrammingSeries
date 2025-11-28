
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

def generate_fibonacci(N):
    """
    Generates the first N numbers of the Fibonacci sequence, controlled by range().
    """
    # Handle base cases N=0 and N=1
    if N <= 0:
        return []
    if N == 1:
        return [0]

    # Initialization of the first two numbers and the result list
    a, b = 0, 1
    fib_sequence = [a, b]
    
    # We use range(2, N) because we have already initialized 2 elements.
    # This ensures the loop runs exactly N-2 times, resulting in N total elements.
    for i in range(2, N): 
        # Calculate the next Fibonacci number
        next_fib = a + b
        fib_sequence.append(next_fib)
        
        # Update a and b using simultaneous assignment (a, b becomes b, a+b)
        a, b = b, next_fib
        
    return fib_sequence

N_target = 10
result = generate_fibonacci(N_target)
print("\n--- Exercise 2: Fibonacci Sequence Generation ---")
print(f"N = {N_target}")
print(f"Fibonacci sequence: {result}")

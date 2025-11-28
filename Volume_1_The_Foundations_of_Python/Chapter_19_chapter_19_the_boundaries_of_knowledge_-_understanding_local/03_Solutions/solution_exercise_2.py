
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

# Exercise 2: Nested Functions and Variable Shadowing

# 1. Global Scope (G)
default_timeout = 30  # Global timeout

def process_data():
    # 2. Enclosing Scope (E)
    default_timeout = 15  # Enclosing scope timeout - Shadows Global

    def quick_check():
        # 4. Local Scope (L)
        default_timeout = 5  # Local scope timeout - Shadows Enclosing
        
        # 5. Print L: Python finds the variable in the immediate Local scope (5).
        print(f"    [Inside quick_check]: Timeout is {default_timeout} seconds. (L)")

    print(f"[Inside process_data - before check]: Timeout is {default_timeout} seconds. (E)")
    
    # Call the nested function
    quick_check()
    
    # 6. Print E: Python still sees the variable defined in the Enclosing scope (15).
    # The local variable created inside quick_check() has been destroyed.
    print(f"[Inside process_data - after check]: Timeout is {default_timeout} seconds. (E)")

# Execution
print("--- Starting Process Data ---")
process_data()

# 7. Print G: The global variable remains untouched (30).
print(f"\n[Global Scope]: Final default timeout is {default_timeout} seconds. (G)")

# Analysis:
# The LEGB rule ensures that the variable is resolved at the nearest scope 
# where it is defined. Each assignment created a new, independent variable 
# instance, effectively shadowing the outer scopes.


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

import inspect

def greeting_factory(style: str):
    # 1. Outer Function Definition: This function acts as the factory.
    # 'style' is a local variable of greeting_factory.
    
    def greet(name: str) -> str:
        # 2. Inner Function Definition: This is the function that will be returned.
        # It is defined *lexically* within greeting_factory's scope.
        # It accesses 'style', which is a *non-local* or *free* variable to 'greet'.
        
        # 3. Core Action: Uses the retained 'style' and the new 'name' argument.
        return f"{style}, {name}!"
    
    # 4. Return the Inner Function Object: We return the function definition itself, 
    # not the result of calling it.
    return greet

# --- Execution Phase 1: Function Creation (The Closure Formation) ---

# 5. Creation of specialized functions:
# formal_greeter now holds the 'greet' function, but its closure binds 'style' to "Welcome".
formal_greeter = greeting_factory("Welcome")

# casual_greeter holds a *different* instance of the 'greet' function, 
# whose closure binds 'style' to "Hey there".
casual_greeter = greeting_factory("Hey there")

# --- Execution Phase 2: Function Invocation (Using the Retained State) ---

# 6. Invocation: The functions are called long after greeting_factory has exited.
print(f"Formal Greeting: {formal_greeter('Dr. Evelyn Reed')}")
print(f"Casual Greeting: {casual_greeter('Jake')}")

# --- Inspection Phase 3: Proving the Closure Mechanism ---

print("\n--- Closure Inspection ---")

# 7. Accessing the __closure__ attribute: This attribute exists only if the function
# is a closure. It returns a tuple of 'cell' objects.
# We inspect the contents of the first cell (index 0).
formal_style_cell = formal_greeter.__closure__[0]
casual_style_cell = casual_greeter.__closure__[0]

print(f"Formal Greeter Retained State: {formal_style_cell.cell_contents}")
print(f"Casual Greeter Retained State: {casual_style_cell.cell_contents}")

# 8. Verifying the names of the free variables (for debugging/introspection)
print(f"Variable Name Bound: {inspect.getclosurevars(formal_greeter).nonlocals}")

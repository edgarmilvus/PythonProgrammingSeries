
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

# 1. Define the decorator function factory
def log_function_call(func):
    """
    A simple decorator that logs the start and end of a function call.
    It accepts the function to be decorated (func) as its argument.
    """
    
    # 2. Define the inner wrapper function (the closure)
    # This wrapper must accept arbitrary arguments (*args, **kwargs)
    def wrapper(*args, **kwargs):
        # 3. Logic to execute BEFORE the original function
        print("-" * 40)
        print(f"STARTING: Execution of '{func.__name__}' with arguments:")
        if args:
            print(f"  Positional Args: {args}")
        if kwargs:
            print(f"  Keyword Args: {kwargs}")
        
        # 4. Call the original function and capture its return value
        # The wrapper must pass all received arguments to the original function
        result = func(*args, **kwargs)
        
        # 5. Logic to execute AFTER the original function
        print(f"FINISHED: Execution of '{func.__name__}' completed.")
        print(f"  Return value type: {type(result).__name__}")
        print("-" * 40)
        
        # 6. The wrapper must return the result of the original function
        return result
        
    # 7. The decorator factory returns the newly created wrapper function
    return wrapper

# 8. Apply the decorator using the @ syntax
@log_function_call
def calculate_product(x, y, multiplier=1):
    """
    Calculates the product of two numbers and multiplies by a factor.
    """
    print(f"  Core Logic: Calculating ({x} * {y}) * {multiplier}...")
    return (x * y) * multiplier

# 9. Call the decorated function
print("\n--- Invoking the decorated function ---")
final_product = calculate_product(12, 5, multiplier=2)

print("\n--- Final Output ---")
print(f"The final calculated product is: {final_product}")

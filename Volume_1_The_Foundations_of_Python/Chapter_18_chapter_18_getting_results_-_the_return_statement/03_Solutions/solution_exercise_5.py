
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

def log_message(message):
    """
    Performs a side effect (printing) but has no explicit return statement.
    """
    print(f"[LOG] {message}")
    # Python implicitly executes 'return None' at the end of this function.

def get_status_report(status):
    """
    Explicitly returns a formatted string value.
    """
    # Explicit return ensures a usable value is passed back.
    return f"Status: {status}"

# 1. Calling the function with side effects
# The print() inside the function executes, but the variable captures the implicit return.
result_log = log_message("System starting...")

# 2. Calling the function that returns a value
result_status = get_status_report("OK")

print("\n--- Analysis of Returned Values ---")

# Analysis of log_message result
print(f"Result from log_message (Value): {result_log}")
print(f"Result from log_message (Type): {type(result_log)}")

# Analysis of get_status_report result
print(f"Result from get_status_report (Value): {result_status}")
print(f"Result from get_status_report (Type): {type(result_status)}")

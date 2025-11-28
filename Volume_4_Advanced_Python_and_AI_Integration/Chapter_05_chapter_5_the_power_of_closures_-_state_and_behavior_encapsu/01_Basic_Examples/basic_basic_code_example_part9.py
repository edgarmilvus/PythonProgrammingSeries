
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

# Source File: basic_basic_code_example_part9.py
# Description: Basic Code Example
# ==========================================

def make_loggers_good():
    loggers = []
    for priority_value in [1, 2, 3]:
        # Solution: Pass the loop variable as a default argument to the inner function.
        # 'p' is a new local variable, and its default value is set immediately 
        # to the current value of 'priority_value'.
        def log_message(message, p=priority_value):
            return f"[Priority {p}] {message}"
        loggers.append(log_message)
    return loggers

good_loggers = make_loggers_good()

print("\n--- Solution Demonstration ---")
print(f"Logger 1 output: {good_loggers[0]('System booting up...')}")
print(f"Logger 2 output: {good_loggers[1]('Configuration check.')}")
print(f"Logger 3 output: {good_loggers[2]('Finalizing process.')}")

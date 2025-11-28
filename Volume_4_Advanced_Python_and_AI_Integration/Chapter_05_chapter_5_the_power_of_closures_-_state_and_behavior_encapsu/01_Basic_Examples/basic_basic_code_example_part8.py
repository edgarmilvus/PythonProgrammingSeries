
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

# Source File: basic_basic_code_example_part8.py
# Description: Basic Code Example
# ==========================================

def make_loggers_bad():
    loggers = []
    # We iterate over the desired priority levels
    for priority in [1, 2, 3]:
        # Define the inner function (the closure)
        def log_message(message):
            # The inner function binds to the 'priority' variable itself, 
            # not the value 1, 2, or 3.
            return f"[Priority {priority}] {message}"
        loggers.append(log_message)
    
    # By the time the loop finishes, 'priority' holds the value 3.
    # The 'priority' variable is shared by all three closure functions.
    return loggers

bad_loggers = make_loggers_bad()

# When we call the first logger, what priority does it use?
# Principle of Least Astonishment (POLA) is violated here.
print("--- Pitfall Demonstration ---")
print(f"Logger 1 output: {bad_loggers[0]('System booting up...')}")
print(f"Logger 2 output: {bad_loggers[1]('Configuration check.')}")

# Expected output (POLA): [Priority 1] ... | [Priority 2] ...
# Actual output (The Pitfall): [Priority 3] ... | [Priority 3] ...

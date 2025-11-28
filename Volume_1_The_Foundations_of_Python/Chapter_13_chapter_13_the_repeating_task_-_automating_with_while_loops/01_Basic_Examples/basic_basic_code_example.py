
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

# 1. Initialization: Define the starting state of the loop variable (the counter)
repetition_count = 1

# 2. Define the termination condition constant (the maximum limit)
MAX_REPETITIONS = 5

# Start the 'while' loop. The code inside will execute as long as the counter
# is less than or equal to the defined maximum limit (5).
while repetition_count <= MAX_REPETITIONS:
    # 3. Action: The task performed during this specific iteration
    # We use an f-string for clear, dynamic output
    print(f"Task Log: Repetition {repetition_count} completed successfully.")

    # 4. CRITICAL State Update: Increment the loop variable
    # This is essential to ensure the condition eventually becomes False
    repetition_count = repetition_count + 1

# 5. Post-Loop Execution: This line runs only after the loop condition fails
print("---")
print(f"All scheduled repetitions ({MAX_REPETITIONS}) are complete. System ready.")

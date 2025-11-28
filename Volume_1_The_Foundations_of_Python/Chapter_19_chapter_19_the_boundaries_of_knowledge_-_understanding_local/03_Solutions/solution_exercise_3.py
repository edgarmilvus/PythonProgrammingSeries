
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

# Exercise 3: Mastering the global Keyword (Persistent State)

# 1. Initialize global state variable
LOG_ID_COUNTER = 0

def generate_log_id(log_message):
    """
    Generates a sequential log ID by modifying the global counter.
    """
    # 2a. Critical step: Declare intent to modify the global variable
    global LOG_ID_COUNTER
    
    # 2b. Modify the global variable (this change persists)
    LOG_ID_COUNTER += 1
    
    # 2c. Print the result
    print(f"--- Log Entry {LOG_ID_COUNTER:04d} ---")
    print(f"Message: {log_message}")

# 3. Call the function multiple times
print("Starting Log Generation:")
generate_log_id("Database connection failed due to timeout.")
generate_log_id("User attempted unauthorized access.")
generate_log_id("Service restart initiated successfully.")

print("\n-------------------------------------")

# 4. Verify global state change
print(f"Final Global LOG_ID_COUNTER value: {LOG_ID_COUNTER}")

# Analysis: The 'global' keyword allowed the function to reach outside its 
# local scope and permanently modify the integer object stored in the global 
# namespace, ensuring the counter persists across calls.

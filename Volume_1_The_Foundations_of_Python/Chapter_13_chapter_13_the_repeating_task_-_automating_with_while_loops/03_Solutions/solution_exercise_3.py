
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

readings = [10, 25, 999, 15, 30, 999, 5, 40]
total_sum = 0
faulty_count = 0
index = 0
list_length = len(readings)
ERROR_CODE = 999

print(f"Processing data points: {readings}")

# Loop through the list using the index counter
while index < list_length:
    current_value = readings[index]
    
    # Check for faulty data
    if current_value == ERROR_CODE:
        faulty_count += 1
        
        # CRITICAL: Must advance the index before continuing, 
        # otherwise the loop will stick on the faulty item forever.
        index += 1  
        
        # Skip the rest of the loop body (the summation step)
        continue    
        
    # Process valid data
    total_sum += current_value
    
    # Advance the index for valid data as well
    index += 1
    
print("\n--- Processing Results ---")
print(f"Total Valid Sum: {total_sum}")
print(f"Faulty Readings Ignored: {faulty_count}")

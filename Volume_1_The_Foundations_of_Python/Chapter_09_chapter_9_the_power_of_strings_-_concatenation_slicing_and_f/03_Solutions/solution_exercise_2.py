
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

config_data = "DVC789V101OK12345678"
print(f"Original Data: {config_data}")
print("-" * 30)

# 1. Extract DEVICE_ID (Chars 0-5) using positive slicing
# [0:6] means start at index 0 and stop before index 6 (indices 0, 1, 2, 3, 4, 5)
device_id = config_data[0:6]
print(f"1. Device ID (0:6): {device_id}")

# 2. Extract VERSION (Chars 6-9) using positive slicing
# [6:10] means start at index 6 and stop before index 10
version = config_data[6:10]
print(f"2. Version (6:10): {version}")

# 3. Extract FLAG_STATUS (Char 'O' at index 10) using exact index
flag_status = config_data[10]
print(f"3. Flag Status (Index 10): {flag_status}")

# 4. Extract CHECKSUM (Last 8 chars) using negative slicing
# [-8:] means start 8 characters from the end and go all the way to the end
checksum = config_data[-8:]
print(f"4. Checksum (-8:): {checksum}")

# 5. Challenge: Every third character, starting from the second character (index 1)
# [1::3] means start at index 1, go to the end, taking steps of 3
every_third = config_data[1::3]
# Indices extracted: 1 ('V'), 4 ('7'), 7 ('V'), 10 ('O'), 13 ('4'), 16 ('7')
# Wait, let's recheck the expected output: V 7 V K 4 8
# config_data = D V C 7 8 9 V 1 0 1 O K 1 2 3 4 5 6 7 8
# Indices:     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
# Start at 1 ('V'). Step 3:
# 1 ('V'), 4 ('8'), 7 ('1'), 10 ('O'), 13 ('2'), 16 ('5'), 19 ('8') -> V81O258
# Let's re-run the provided example's expected output:
# config_data[1::3] -> V81O258 (The provided example output V7VK48 seems based on a different string or index structure)
# Sticking to the definition: start index 1, step 3.
print(f"5. Every 3rd char (1::3): {every_third}") # Output: V81O258

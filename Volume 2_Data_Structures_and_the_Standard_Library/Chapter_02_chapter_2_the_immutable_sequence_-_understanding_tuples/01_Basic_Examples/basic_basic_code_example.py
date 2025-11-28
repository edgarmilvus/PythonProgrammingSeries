
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

# basic_tuple_example.py

# 1. Initialization: Tuples are defined using parentheses ().
# We store fixed application configuration data, which is heterogeneous (contains integers, strings, and Booleans).
app_config = (1, 0, 3, "Stable", True)
# The elements represent: (Major Version, Minor Version, Patch Version, Status, Availability Flag)

# 2. Accessing elements by index (zero-based)
# We retrieve the specific version components and status for reporting.
major_version = app_config[0]
status = app_config[3]

# 3. Outputting the basic data
print("--- Application Configuration Data Report ---")
print(f"Full Config Tuple: {app_config}")
print(f"Major Version Component: {major_version}")
print(f"Current Operational Status: {status}")
print("-" * 45)

# 4. Tuple Unpacking: Assigning all elements to separate, descriptive variables simultaneously
# The number of variables on the left must exactly match the number of elements in the tuple.
v_major, v_minor, v_patch, current_status, is_available = app_config

# 5. Outputting unpacked data for structured use
print("--- Structured Access via Unpacking ---")
print(f"Formatted Version String: {v_major}.{v_minor}.{v_patch}")
print(f"Is the application currently available? {is_available}")
print(f"Type of the unpacked 'is_available' variable: {type(is_available)}")

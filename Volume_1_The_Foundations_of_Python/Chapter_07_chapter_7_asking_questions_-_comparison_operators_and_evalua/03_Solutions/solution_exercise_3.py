
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

# Exercise 7.4.3 Setup
# 1 & 2. Define variables with different types
numeric_id = 42
string_id = '42'

# 3. Compare values only
# Python determines these are numerically equivalent, resulting in True.
value_equal = (numeric_id == string_id)

# 4. Compare types only (using the type() function)
# type(42) is <class 'int'>, type('42') is <class 'str'>. This results in False.
type_equal = (type(numeric_id) == type(string_id))

# 5. Determine Strict Equality (Value AND Type)
# Strict equality requires both the value comparison AND the type comparison to be True.
strictly_equal = value_equal and type_equal

# 6. Print Results
print(f"Numeric ID Type: {type(numeric_id)}")
print(f"String ID Type: {type(string_id)}")
print("-" * 30)
print(f"Value comparison (42 == '42'): {value_equal}")
print(f"Type comparison (int == str): {type_equal}")
print(f"Strict equality (Value AND Type): {strictly_equal}")

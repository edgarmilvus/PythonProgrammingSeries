
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

# basic_unpacking.py

# 1. Define the data structure (a tuple representing a student record)
# Tuples are often used for fixed records because they are immutable.
student_record = ("Alice Smith", 92, "A")

# 2. Basic sequence unpacking: assigning three variables simultaneously
# The number of variables on the LHS must exactly match the number of elements
# in the RHS sequence (3 items on both sides).
name, score, grade = student_record

# 3. Display the results to confirm successful assignment
print(f"--- Student Record Unpacking ---")
print(f"Original Record: {student_record}")
print(f"Name: {name}")
print(f"Score: {score}")
print(f"Grade: {grade}")
print("-" * 35)

# 4. Unpacking with a List (demonstrating flexibility)
# Unpacking works identically for lists, as they are also iterable sequences.
coordinates = [15.5, -23.1]
x_coord, y_coord = coordinates

print(f"Coordinates Unpacked: X={x_coord}, Y={y_coord}")
print("-" * 35)

# 5. The Pythonic Variable Swap (a powerful application of unpacking)
a = 100
b = 200
print(f"Before swap: a={a}, b={b}")

# The magic: The RHS creates a temporary tuple (b, a). This tuple is then unpacked
# back into the LHS variables (a, b), effectively swapping their values.
a, b = b, a

print(f"After swap: a={a}, b={b}")
print("-" * 35)

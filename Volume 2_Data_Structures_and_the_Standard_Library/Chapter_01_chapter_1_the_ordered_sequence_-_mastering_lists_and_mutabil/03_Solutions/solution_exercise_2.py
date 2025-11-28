
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

# 1. Create an original list
primary_data = [100, 200, 300]

print("--- Exercise 2: Proving Identity ---")
print(f"Primary Data ID: {id(primary_data)}")

# 2. Create an alias (direct assignment shares the memory address)
alias_data = primary_data
print(f"Alias Data ID: {id(alias_data)} (SAME ID - Shared Memory)")

# 3. Create a shallow copy using slicing (creates a new object)
copy_data = primary_data[:]
print(f"Copy Data ID: {id(copy_data)} (DIFFERENT ID - New Object)")

print("\n--- Step 5 & 6: Modifying the Alias ---")
# 5. Modify the first element of the alias
alias_data[0] = 999 
print(f"Alias Modified: {alias_data}")
# 6. Print primary_data: The change is visible because they share the same object
print(f"Primary Data After Alias Change: {primary_data}")

print("\n--- Step 7 & 8: Modifying the Copy ---")
# 7. Modify the first element of the copy
copy_data[0] = 111 
print(f"Copy Modified: {copy_data}")
# 8. Print primary_data: The original is unaffected because the copy is a new object
print(f"Primary Data After Copy Change: {primary_data}")

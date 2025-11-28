
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

# 1. Chained Assignment: Setting all three variables to the same initial value (5)
# This is an efficient way to initialize multiple variables to the same value.
admin_level = moderator_level = guest_level = 5

print("--- Verification 1: Initial State ---")
print(f"Admin Level: {admin_level}")
print(f"Moderator Level: {moderator_level}")
print(f"Guest Level: {guest_level}")

# 3. Independent Reassignment: Modifying only admin_level
# Because integers are immutable, this creates a new value (10) in memory,
# and only 'admin_level' is redirected to point to it.
admin_level = 10

print("\n--- Verification 2: After Admin Reassignment ---")
print(f"Admin Level: {admin_level}")
print(f"Moderator Level: {moderator_level}") # Remains 5
print(f"Guest Level: {guest_level}")        # Remains 5

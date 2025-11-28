
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

# Source File: basic_basic_code_example_part9.py
# Description: Basic Code Example
# ==========================================

from collections import defaultdict

# Initialize with int factory (default value is 0)
scores = defaultdict(int, {'Alice': 95, 'Bob': 88})
print(f"Initial size: {len(scores)}") # Output: 2

# Pitfall: Checking for a name that doesn't exist
new_student = "Charlie"
# You might think this is just a read operation, but it's not.
charlie_score = scores[new_student] 

print(f"Charlie's score (retrieved): {charlie_score}") # Output: 0
print(f"New size: {len(scores)}") # Output: 3 (Charlie was added!)
print(f"Scores dictionary content: {dict(scores)}") 
# Output: {'Alice': 95, 'Bob': 88, 'Charlie': 0}


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

# Source File: basic_basic_code_example_part5.py
# Description: Basic Code Example
# ==========================================

# random.random() returns a float N such that 0.0 <= N < 1.0 (exclusive of 1.0).
# We simulate a weighted coin where a value less than 0.7 means "Success".
SUCCESS_THRESHOLD = 0.7
coin_flip_value = random.random()
is_success = coin_flip_value < SUCCESS_THRESHOLD

print(f"\n[Action 2: Weighted Probability Check] Random float generated: {coin_flip_value:.4f}")

if is_success:
    print(f"Result: Success! (Value {coin_flip_value:.4f} was less than {SUCCESS_THRESHOLD})")
else:
    print(f"Result: Failure. (Value {coin_flip_value:.4f} was {SUCCESS_THRESHOLD} or greater)")

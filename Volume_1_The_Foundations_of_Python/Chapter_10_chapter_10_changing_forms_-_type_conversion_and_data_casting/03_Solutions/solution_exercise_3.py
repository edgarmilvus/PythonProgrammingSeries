
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

# Exercise 3 Solution
print("--- Exercise 3: Inventory Tag Generator (Number to String) ---")

def generate_tag(item_id):
    """
    Generates an inventory tag string from an integer item ID, 
    including manual zero padding to ensure a four-digit format.
    """
    prefix = "INV-"
    
    # Advanced Challenge: Manual Zero Padding Implementation
    item_str = str(item_id)
    
    if item_id < 10:
        # Pad 0-9 with three zeros (e.g., 9 -> "0009")
        item_str = "000" + item_str
    elif item_id < 100:
        # Pad 10-99 with two zeros (e.g., 45 -> "0045")
        item_str = "00" + item_str
    elif item_id < 1000:
        # Pad 100-999 with one zero (e.g., 123 -> "0123")
        item_str = "0" + item_str
    
    # 3. Use string concatenation (+) to join the prefix and the converted string ID
    final_tag = prefix + item_str
    return final_tag

# Test Cases
tag_1 = generate_tag(45)
tag_2 = generate_tag(1024)
tag_3 = generate_tag(9)
tag_4 = generate_tag(9999)

print(f"ID 45 -> Tag: {tag_1}")
print(f"ID 1024 -> Tag: {tag_2}")
print(f"ID 9 -> Tag: {tag_3}")
print(f"ID 9999 -> Tag: {tag_4}")

print("-" * 50)


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

# Source File: basic_basic_code_example_part2.py
# Description: Basic Code Example
# ==========================================

# Subsection 2/5: Basic Code Example - defaultdict

# 1. Import the necessary specialized collection type
from collections import defaultdict

# 2. Define the raw data: a list of (item, category/color) tuples
inventory_data = [
    ("Apple", "Red"),
    ("Banana", "Yellow"),
    ("Cherry", "Red"),
    ("Lemon", "Yellow"),
    ("Grape", "Purple"),
    ("Strawberry", "Red"),
    ("Plum", "Purple")
]

# 3. Initialize the defaultdict. 
# We provide 'list' as the default factory. This means any time 
# we try to access a key that doesn't exist, Python runs list() 
# and assigns the result (an empty list []) to that key.
grouped_by_color = defaultdict(list)

# 4. Iterate through the data and populate the defaultdict
print("--- Starting Grouping Process ---")
for item, color in inventory_data:
    # This is the core simplification: we append directly.
    # If 'color' is new (e.g., "Red"), defaultdict creates grouped_by_color["Red"] = [] 
    # before running .append("Apple").
    print(f"Processing item '{item}' and assigning to color '{color}'...")
    grouped_by_color[color].append(item)

# 5. Display the final result
print("\n--- Final Grouped Inventory ---")
for color, items in grouped_by_color.items():
    print(f"The color '{color}' contains: {', '.join(items)}")

# 6. Demonstrate the default behavior: accessing a non-existent key
print("\n--- Accessing Non-Existent Key Behavior ---")
missing_color = "Blue"
print(f"Attempting to access key '{missing_color}' using grouped_by_color['{missing_color}']...")

# Accessing this key automatically creates it with the default value (an empty list)
blue_fruits = grouped_by_color[missing_color] 
print(f"Value retrieved for '{missing_color}': {blue_fruits}")
print(f"Type of retrieved value: {type(blue_fruits)}")

# Show that the dictionary size has increased, proving the key was added
print(f"Total unique colors (keys) now in the dictionary: {len(grouped_by_color)}")

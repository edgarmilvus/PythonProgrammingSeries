
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

# 1. Initialization: Create a dictionary for a book profile.
# Dictionaries are defined using curly braces {}.
book_profile = {
    "title": "The Hitchhiker's Guide to the Galaxy",
    "author": "Douglas Adams",
    "year_published": 1979,
    "is_available": True  # Keys can map to various data types (string, int, bool)
}

print("--- Initial Profile ---")
print(book_profile)
print("-" * 40)

# 2. Read Operation (Accessing Values):
# Accessing the title using its key name inside square brackets.
book_title = book_profile["title"]
print(f"1. Title Retrieved: {book_title}")

# 3. Update Operation (Modifying an existing entry):
# We use the key to locate the value and assign a new value to it.
book_profile["is_available"] = False
print(f"2. Availability Updated (Checked Out): {book_profile['is_available']}")

# 4. Create Operation (Adding a new entry/key-value pair):
# Using square bracket notation on a key that does not yet exist.
book_profile["isbn"] = "978-0345391803"
print(f"3. ISBN Added: {book_profile['isbn']}")

# 5. Delete Operation (Removing a key-value pair):
# The 'del' keyword permanently removes the key and its associated value.
del book_profile["year_published"]
print("4. Year Published Deleted.")

print("-" * 40)
print("--- Final Profile ---")
print(book_profile)

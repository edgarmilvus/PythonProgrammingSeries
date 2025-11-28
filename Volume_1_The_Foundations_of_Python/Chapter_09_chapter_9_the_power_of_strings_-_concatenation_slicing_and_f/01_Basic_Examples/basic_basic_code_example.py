
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

# 1. Define foundational user data using string literals
first_name = "Elara"
last_name = "Vance"
separator = "."
greeting_prefix = "Hello, "

# 2. String Concatenation: Building a standardized internal username
# We use the '+' operator to join three separate string variables into one new string.
internal_username = first_name + separator + last_name

# 3. String Concatenation: Creating a personalized greeting message
# This combines a fixed prefix, the newly created username, and a punctuation mark.
personalized_greeting = greeting_prefix + internal_username + "!"

# 4. Basic Indexing: Extracting the first character (the initial)
# Strings are zero-indexed, meaning the first character is always at position [0].
first_initial = first_name[0]
last_initial = last_name[0]

# 5. Slicing: Extracting a specific segment using negative indexing
# [-3:] means start three characters from the end and proceed until the end of the string.
last_name_suffix = last_name[-3:]

# 6. Outputting the results using the print function
print("--- User Data Manipulation Report ---")
print(f"Original First Name: {first_name}")
print(f"Original Last Name: {last_name}")
print("-" * 30)
print(f"Generated Username: {internal_username}")
print(f"Full Greeting: {personalized_greeting}")
print(f"Extracted Initials: {first_initial}{last_initial}")
print(f"Last Name Suffix (Last 3 chars): {last_name_suffix}")

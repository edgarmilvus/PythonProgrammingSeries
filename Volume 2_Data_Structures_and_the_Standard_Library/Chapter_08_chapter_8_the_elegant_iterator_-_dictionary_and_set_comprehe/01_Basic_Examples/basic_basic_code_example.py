
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

# --- Input Data Setup ---

# 1. Define the input data for dictionary creation: (City Name, Temperature in Celsius)
celsius_temps = [
    ("NYC", 10),
    ("London", 15),
    ("Tokyo", 20),
    ("Paris", 10), # Note: Duplicate temperature 10
    ("Berlin", 5)
]

# --- Dictionary Comprehension: Celsius to Fahrenheit Conversion ---

# Goal: Create a dictionary mapping city name (key) to Fahrenheit temperature (value).
# Formula: F = C * 9/5 + 32
fahrenheit_map = {
    city: (c * 9/5 + 32)
    for city, c in celsius_temps
}

print("--- Dictionary Conversion Results ---")
print(f"Original Data: {celsius_temps}")
print(f"Fahrenheit Map: {fahrenheit_map}")
print("-" * 30)


# 2. Define the input data for set creation: Raw student test scores.
student_scores = [85, 92, 68, 75, 85, 99, 68, 70, 55, 75]
passing_threshold = 70

# --- Set Comprehension: Identifying Unique Passing Scores ---

# Goal: Create a set containing only the unique scores that meet the passing threshold.
unique_passing_scores = {
    score
    for score in student_scores
    if score >= passing_threshold
}

print("--- Set Filtering Results ---")
print(f"Original Scores: {student_scores}")
print(f"Unique Passing Scores (>= {passing_threshold}): {unique_passing_scores}")

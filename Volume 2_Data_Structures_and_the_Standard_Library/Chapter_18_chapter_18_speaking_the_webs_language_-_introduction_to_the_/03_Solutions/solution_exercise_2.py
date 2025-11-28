
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

import json
import os

FILE_NAME = "employees.json"

# 1. Define the Python list of dictionaries
employee_data = [
    {"id": "E101", "name": "Sarah Connor", "is_active": True, "role": "Engineer"},
    {"id": "E102", "name": "Kyle Reese", "is_active": True, "role": "Analyst"},
    {"id": "E103", "name": "T-800", "is_active": False, "role": "Security"}
]

print("\n--- Exercise 2 Solution ---")

# 2 & 3. Write data to the file using json.dump()
# Use 'w' mode for writing. 'indent=4' ensures readability.
try:
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        # json.dump writes directly to the file object 'f'
        json.dump(employee_data, f, indent=4)
    print(f"Successfully wrote {len(employee_data)} records to {FILE_NAME}.")
except IOError as e:
    print(f"Error writing file: {e}")

# 4 & 5. Read data back from the file using json.load()
retrieved_data = []
try:
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        # json.load reads the entire content from the file object 'f'
        retrieved_data = json.load(f)
    print(f"Successfully loaded data from {FILE_NAME}.")
except FileNotFoundError:
    print(f"Error: File {FILE_NAME} not found during read operation.")

# 6. Verification
print(f"Total records retrieved: {len(retrieved_data)}")
if retrieved_data:
    print(f"Name of the first employee: {retrieved_data[0]['name']}")

# Cleanup: Remove the generated file
if os.path.exists(FILE_NAME):
    os.remove(FILE_NAME)
    # print(f"Cleaned up {FILE_NAME}.")

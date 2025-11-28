
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

# Employee Data (List of Lists)
employee_records = [
    [101, "Alice Johnson", "Engineering", 92000.00],
    [102, "Bob Smith", "Marketing", 65000.00],
    [103, "Charlie Brown", "Engineering", 78000.00],
    [104, "Dana Scully", "R&D", 110000.00],
    [105, "Eve Harrington", "Engineering", 105000.00],
    [106, "Frank Miller", "Marketing", 81000.00],
]

high_earning_engineers = []
SALARY_THRESHOLD = 80000.00

# 2. Use a for loop to iterate through the records
for record in employee_records:
    # 3. Use indexing to access fields: Name (1), Department (2), Salary (3)
    department = record[2]
    salary = record[3]
    name = record[1]
    
    # 4. Apply conditional logic: Must be Engineering AND salary > threshold
    if department == "Engineering" and salary > SALARY_THRESHOLD:
        # 5. Collect the name
        high_earning_engineers.append(name)

print("--- Exercise 3: Nested Data Structure Parsing ---")
print(f"Filtered Engineers: {high_earning_engineers}")

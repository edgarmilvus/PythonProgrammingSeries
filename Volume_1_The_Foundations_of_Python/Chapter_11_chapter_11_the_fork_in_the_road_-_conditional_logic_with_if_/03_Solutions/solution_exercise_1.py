
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

# 1. Input Handling: Define the student's score
student_score = 85
# student_score = 105 # Test case for invalid input
# student_score = 55 # Test case for F grade

# 5. Edge Case Handling: Check for impossible scores first
if student_score < 0 or student_score > 100:
    print(f"Error: Score {student_score} is invalid. Score must be between 0 and 100.")
    grade = "INVALID"
else:
    # 2. Conditional Structure: Check grades from highest to lowest
    # 90-100: A
    if student_score >= 90:
        grade = "A (Excellent)"
    # 80-89: B (We don't need to check < 90 because the 'if' above already handled it)
    elif student_score >= 80:
        grade = "B (Good)"
    # 70-79: C
    elif student_score >= 70:
        grade = "C (Satisfactory)"
    # 60-69: D
    elif student_score >= 60:
        grade = "D (Needs Improvement)"
    # 0-59: F (The final 'else' catches everything remaining, which must be 0-59)
    else:
        grade = "F (Failure)"

# 4. Output: Print the result
if grade != "INVALID":
    print(f"Student Score: {student_score}")
    print(f"Resulting Grade: {grade}")

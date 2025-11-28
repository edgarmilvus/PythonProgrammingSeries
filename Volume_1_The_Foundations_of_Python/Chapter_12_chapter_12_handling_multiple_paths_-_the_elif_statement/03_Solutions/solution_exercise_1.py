
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

def classify_grade(score):
    """
    Converts a numerical score (0-100) into a letter grade using an if-elif-else chain.
    
    Args:
        score (int): The numerical test score.
    """
    # 1. Check for invalid input (outside 0-100 range)
    if score < 0 or score > 100:
        print(f"Score {score} is invalid. Score must be between 0 and 100.")
        return

    # 2. Grading Logic (Checking from highest to lowest)
    # If the score is 90 or above, it's an 'A'. The rest of the chain is skipped.
    if score >= 90:
        grade = 'A'
    # If the score wasn't >= 90, check if it's 80 or above.
    elif score >= 80:
        grade = 'B'
    # If the score wasn't >= 80, check if it's 70 or above.
    elif score >= 70:
        grade = 'C'
    # If the score wasn't >= 70, check if it's 60 or above.
    elif score >= 60:
        grade = 'D'
    # If none of the above conditions were met (i.e., score is 0-59).
    else:
        grade = 'F'

    print(f"Score: {score} -> Grade: {grade}")

# Example Usage:
print("--- Grading System Examples ---")
classify_grade(95)   # A
classify_grade(82)   # B
classify_grade(55)   # F
classify_grade(105)  # Invalid input
classify_grade(-10)  # Invalid input

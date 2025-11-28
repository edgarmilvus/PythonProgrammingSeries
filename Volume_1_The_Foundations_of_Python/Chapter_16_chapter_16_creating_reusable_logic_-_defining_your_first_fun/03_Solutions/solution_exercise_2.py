
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

def get_letter_grade(score):
    """
    Determines the letter grade corresponding to a numerical score (0-100).

    The function uses sequential conditional checks and returns immediately
    upon finding the matching grade range.

    Parameters:
        score (float or int): The numerical score to evaluate.

    Returns:
        str: The corresponding letter grade ('A', 'B', 'C', or 'F').
    """
    # Check the highest scores first. If score >= 90, 'A' is returned,
    # and subsequent elif blocks are skipped.
    if score >= 90:
        return 'A'
    
    # If we reach here, score is less than 90.
    elif score >= 80:
        return 'B'
    
    # If we reach here, score is less than 80.
    elif score >= 70:
        return 'C'
    
    # If none of the above conditions are met, the score must be below 70.
    else:
        return 'F'

# --- Testing the Function ---
print("\n--- Exercise 2: Grade Evaluator ---")

# Test cases covering all categories
scores_to_test = [95, 82, 75, 60, 100, 69.9]

for test_score in scores_to_test:
    grade = get_letter_grade(test_score)
    print(f"Score: {test_score} -> Grade: {grade}")

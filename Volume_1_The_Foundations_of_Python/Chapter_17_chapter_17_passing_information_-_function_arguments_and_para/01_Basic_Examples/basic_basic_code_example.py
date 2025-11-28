
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

# report_student_status.py

# Define a function to generate a status message.
# It requires three formal parameters: student_name, course_subject, and final_grade.
def generate_status(student_name, course_subject, final_grade):
    """
    Constructs and prints a formatted status report based on the provided parameters.
    """
    # Use an f-string (formatted string literal) to seamlessly combine the inputs
    message = f"{student_name} achieved a grade of {final_grade} in {course_subject}."
    
    # Output the result clearly
    print(f"--- Status Generated ---")
    print(message)
    print("------------------------")
    
    # Although we print it, returning the message allows the caller to use the string later
    return message

# --- Demonstrating different argument passing styles ---

# 1. Positional Arguments: Relying entirely on the order defined in the function signature
print("\n[CALL 1: Positional Arguments]")
# The order must match the definition exactly: (name, subject, grade)
generate_status("Alice Johnson", "Mathematics", "A")

# 2. Keyword Arguments: Explicitly naming which parameter receives which value
print("\n[CALL 2: Keyword Arguments]")
# The order of the arguments is irrelevant because we named them explicitly
generate_status(final_grade="B+", course_subject="History", student_name="Bob Smith")

# 3. Mixed Arguments: Positional arguments must always come first, followed by keywords
print("\n[CALL 3: Mixed Arguments (Positional then Keyword)]")
# "Charlie Brown" is positional (maps to student_name)
# The remaining arguments are named keywords
generate_status("Charlie Brown", final_grade="C", course_subject="Science")

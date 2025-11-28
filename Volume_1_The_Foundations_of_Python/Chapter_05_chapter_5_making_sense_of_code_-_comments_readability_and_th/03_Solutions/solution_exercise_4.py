
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

"""
cli_greeter.py

Description:
A simple command-line utility designed to greet a user based on arguments 
provided at execution. It validates that the age argument is a valid integer.

Usage Example:
To run the script, execute from the terminal providing the name and age:
$ python cli_greeter.py [NAME] [AGE]

Example Execution:
$ python cli_greeter.py Alice 25
"""

import sys

def main():
    """
    Entry point for the command-line script. 
    
    Handles argument parsing from sys.argv, validates input count and data 
    types, and prints the final greeting. Exits with status code 1 upon error.
    """
    
    # Check argument count: sys.argv must have a length of 3 (script name + 2 arguments).
    if len(sys.argv) != 3:
        print("Error: Two arguments required (Name and Age).")
        # Exit with status code 1 to indicate failure.
        sys.exit(1)
    
    # Assign arguments: sys.argv[1] is the name, sys.argv[2] is the age string.
    user_name = sys.argv[1]
    user_age_str = sys.argv[2]
    
    # Data Validation: Use a try/except block to safely convert the age string to an integer.
    try:
        user_age = int(user_age_str)
        
    # Handle ValueError if the age argument is non-numeric.
    except ValueError:
        print(f"Error: Age '{user_age_str}' must be an integer.")
        sys.exit(1)
        
    # Successful execution: Print the final output.
    print(f"Hello, {user_name}! You are {user_age} years old.")

if __name__ == "__main__":
    main()

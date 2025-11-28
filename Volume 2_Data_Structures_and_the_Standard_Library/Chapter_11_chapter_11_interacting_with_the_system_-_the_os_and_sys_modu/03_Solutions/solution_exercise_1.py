
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

# validator.py

import sys

def main():
    """
    Validates that exactly two command-line arguments are provided.
    Exits with code 1 on failure and code 0 on success.
    """
    # sys.argv includes the script name itself, so we expect a length of 3.
    required_args = 3

    if len(sys.argv) != required_args:
        # 2. Usage Message (Failure): Print error message to standard error
        usage_message = (
            "Error: This script requires exactly two arguments.\n"
            f"Usage: python {sys.argv[0]} <arg1> <arg2>\n"
        )
        sys.stderr.write(usage_message)

        # 3. Controlled Exit (Failure): Terminate with exit code 1
        sys.exit(1)
    else:
        # Arguments are at index 1 and 2
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]

        # 4. Success Output: Print arguments and their types
        print("Argument validation successful.")
        print("-" * 30)
        print(f"Argument 1: {arg1}, Type: {type(arg1).__name__}")
        print(f"Argument 2: {arg2}, Type: {type(arg2).__name__}")
        print("-" * 30)

        # 5. Controlled Exit (Success): Terminate with exit code 0
        sys.exit(0)

if __name__ == "__main__":
    main()

# Example usage (in shell):
# python validator.py hello world  # Success (Exits 0)
# python validator.py one         # Failure (Exits 1, prints to stderr)

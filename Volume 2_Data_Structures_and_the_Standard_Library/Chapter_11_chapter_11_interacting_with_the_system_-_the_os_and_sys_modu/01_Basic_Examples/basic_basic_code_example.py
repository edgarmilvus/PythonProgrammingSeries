
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

import sys
import os

# Define the core function to encapsulate the logic
def check_environment_status():
    """
    Checks and displays key information about the Python runtime (sys) 
    and the operating system environment (os).
    """

    # 1. Handling Command-Line Arguments (via sys.argv)
    # sys.argv is a list where the first element (index 0) is the script name.
    if len(sys.argv) > 1:
        # If arguments exist beyond the script name, use the first one as the user name.
        user_name = sys.argv[1]
    else:
        # If no argument is supplied, use a default identifier.
        user_name = "System Administrator"

    # Display the greeting
    print(f"--- Diagnostic Check Initiated by: {user_name} ---")
    print("\n[RUNTIME INFORMATION (sys Module)]")

    # 2. Displaying Python Version and Interpreter Path
    # sys.version provides a detailed string; we split it to get just the version number.
    print(f"Active Python Version: {sys.version.split()[0]}")
    # sys.executable points to the binary file running the script.
    print(f"Interpreter Binary Location: {sys.executable}")

    print("\n[OPERATING SYSTEM INFORMATION (os Module)]")

    # 3. Getting the Current Working Directory (CWD)
    current_directory = os.getcwd()
    print(f"Current Working Directory (CWD): {current_directory}")

    # 4. Accessing Environment Variables (via os.environ)
    # We retrieve the standard 'HOME' variable (or 'USERPROFILE' on Windows)
    # os.environ.get() safely retrieves the value or returns a default string.
    home_key = 'HOME' if sys.platform != 'win32' else 'USERPROFILE'
    user_home_dir = os.environ.get(home_key, 'Home directory variable not set.')
    
    print(f"User Home Directory ({home_key}): {user_home_dir}")
    
    # 5. Demonstrating OS Path Separator
    print(f"OS Path Separator for this system: '{os.pathsep}'")


# Standard entry point for execution
if __name__ == "__main__":
    check_environment_status()


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

# file_organizer_refactored.py

import os
import sys

def get_organization_root():
    """
    Determines the root directory for file organization based on 
    the ORGANIZE_ROOT environment variable, or defaults to the user's home directory.
    """
    # 1. Environment Check: Get value from environment
    env_root = os.getenv('ORGANIZE_ROOT')

    if env_root:
        # 3. Path Resolution: Use the environment variable path
        final_root = env_root
        source_desc = "Environment Variable (ORGANIZE_ROOT)"
    else:
        # 2. Default Path: Use cross-platform home directory
        # os.path.expanduser('~') resolves to C:\Users\User on Windows or /home/user on Linux
        final_root = os.path.expanduser('~')
        source_desc = "Default Home Directory (~)"

    # Ensure the path is absolute and normalized
    final_root = os.path.abspath(final_root)

    # 4. Directory Creation: Ensure the root path exists
    try:
        # Use exist_ok=True to prevent errors if the directory already exists
        os.makedirs(final_root, exist_ok=True)
    except OSError as e:
        print(f"Error creating organization root directory: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 6. Reporting
    print("--- Dynamic Configuration Status ---")
    print(f"Root determined via: {source_desc}")
    print(f"Final Organization Root: {final_root}")
    print("------------------------------------")

    return final_root

def simulate_organization_logic(org_root):
    """
    Simulates the refactored organization logic using the dynamic root path.
    (This replaces the actual file moving logic of the full organizer script.)
    """
    # 5. Refactoring Example: All subsequent paths are built relative to org_root
    
    # Example: Define a target directory for images
    images_dir = os.path.join(org_root, 'Organized_Images')
    
    # Ensure the target subdirectory exists
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"Simulated creation of target folder: {images_dir}")
    print("File organization would now proceed using these paths...")


if __name__ == "__main__":
    # Example setup: In a real scenario, you might pass a source directory here
    
    organization_root = get_organization_root()
    
    # Run the core logic using the dynamically determined root
    simulate_organization_logic(organization_root)

# To test setting the environment variable (in shell/bash before running):
# export ORGANIZE_ROOT=/tmp/my_files
# python file_organizer_refactored.py

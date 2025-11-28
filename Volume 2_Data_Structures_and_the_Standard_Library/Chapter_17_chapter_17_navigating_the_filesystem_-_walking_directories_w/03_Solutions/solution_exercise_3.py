
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

# --- Exercise 2 Solution ---

EXCLUSION_DIRS = ['.git', '.venv', 'node_modules']

def prune_traversal(start_path):
    """Traverses a directory, skipping specified directories by pruning."""
    print(f"\n--- Exercise 2: Pruned Traversal ---")
    print(f"Starting traversal at: {start_path}")
    
    visited_roots = []
    
    for root, dirs, files in os.walk(start_path):
        
        # Pruning logic: Modify the 'dirs' list in place (dirs[:])
        # This filters out any directory names matching the exclusion list
        dirs[:] = [d for d in dirs if d not in EXCLUSION_DIRS]
        
        # Record the directory that was successfully visited (not pruned)
        visited_roots.append(root)
        print(f"Visited: {root}")

    return visited_roots


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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

task_queue = ["Task A (Urgent)", "Task B", "Task C", "Task D", "Task E (Low)", "Task F"]

print("--- Exercise 5: List Method Sequence Mastery ---")
print(f"Initial Queue: {task_queue}")

# 1. Prioritize: Insert "Task X" immediately before "Task B"
# Step 1a: Find the index of "Task B"
b_index = task_queue.index("Task B")
# Step 1b: Insert at that index
task_queue.insert(b_index, "Task X (High Priority)")
print(f"After Insert: {task_queue}")

# 2. Process End: Remove the last task using .pop() (no argument)
processed_task_end = task_queue.pop()
print(f"After Pop: {task_queue}")

# 3. Process Specific: Remove "Task D" using .remove()
task_queue.remove("Task D")
print(f"After Remove: {task_queue}")

# 4. Peek (Negative Indexing): Print the task second to last
# Index -1 is the last element; Index -2 is the second to last element.
second_to_last_task = task_queue[-2]
print(f"Second to Last Task (Peek): {second_to_last_task}")

# 5. Final State
print(f"\nFinal Queue State: {task_queue}")
print(f"Task Processed from End: {processed_task_end}")

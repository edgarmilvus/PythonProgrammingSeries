
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

from collections import deque

# 1. Class Definition
class HistoryBuffer:
    """
    A fixed-size history buffer using collections.deque with maxlen.
    """
    def __init__(self, max_size):
        self.max_size = max_size
        # Initialize deque with the fixed size. maxlen handles automatic eviction.
        self.buffer = deque(maxlen=max_size)
        print(f"Buffer initialized with max size: {max_size}")

    # 2. add_action method
    def add_action(self, action_string):
        """Appends a new action, automatically evicting the oldest if full."""
        self.buffer.append(action_string)
        print(f"  Added action: '{action_string}'")

    # 3. get_history method
    def get_history(self):
        """Returns the current contents of the buffer as a list."""
        return list(self.buffer)

# 4. Demonstration
print("--- Exercise 3: Implementing a Fixed-Size History Buffer (deque) ---")
history = HistoryBuffer(max_size=5)

# Add 5 actions (filling the buffer)
history.add_action("Action 1: User Login")
history.add_action("Action 2: Data Query")
history.add_action("Action 3: Report Generation")
history.add_action("Action 4: System Check")
history.add_action("Action 5: Configuration Change")

print(f"\nHistory after 5 additions: {history.get_history()}")

# Add 2 more actions (demonstrating eviction)
print("\n--- Adding Actions 6 and 7 (Eviction starts) ---")
history.add_action("Action 6: API Call") # Action 1 is evicted
history.add_action("Action 7: Logout")    # Action 2 is evicted

final_history = history.get_history()
print(f"\nHistory after 7 additions (only last 5 remain):")
print(final_history)
print(f"Length check: {len(final_history)}")

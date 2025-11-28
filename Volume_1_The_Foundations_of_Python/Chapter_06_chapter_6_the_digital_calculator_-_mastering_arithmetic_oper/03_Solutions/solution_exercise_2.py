
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

# Define the total processing time in seconds
total_seconds = 15430

# --- Conversion Constants ---
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60

# 1. Calculate Hours and the remainder
hours = total_seconds // SECONDS_PER_HOUR
remaining_seconds_after_hours = total_seconds % SECONDS_PER_HOUR

# 2. Calculate Minutes from the remainder
minutes = remaining_seconds_after_hours // SECONDS_PER_MINUTE

# 3. Calculate the final remaining seconds
final_seconds = remaining_seconds_after_hours % SECONDS_PER_MINUTE

# Print the final result
print(f"{total_seconds} seconds is equal to {hours} hours, {minutes} minutes, and {final_seconds} seconds.")


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

# SKELETON CODE: Time Synchronization Utility

# --- 1. Initial Data Setup (Simulating a large time difference) ---
# This number represents the total elapsed time in seconds between two events.
total_elapsed_seconds = 345678 

# --- 2. Conversion Logic (YOUR TASK STARTS HERE) ---
# Define conversion constants
seconds_per_day = 86400
seconds_per_hour = 3600
seconds_per_minute = 60

# 2a. Calculate Days and the remaining seconds
days = total_elapsed_seconds // seconds_per_day
remaining_seconds_after_days = total_elapsed_seconds % seconds_per_day

# 2b. Calculate Hours and the remaining seconds
# Use the remainder from the day calculation
hours = remaining_seconds_after_days // seconds_per_hour
remaining_seconds_after_hours = remaining_seconds_after_days % seconds_per_hour

# 2c. Calculate Minutes and the final remaining seconds
# Use the remainder from the hour calculation
minutes = remaining_seconds_after_hours // seconds_per_minute
final_seconds = remaining_seconds_after_hours % seconds_per_minute


# --- 3. Output ---
print(f"--- Elapsed Time Breakdown ---")
print(f"Total Seconds: {total_elapsed_seconds}")
print(f"Formatted Time:")
print(f"  Days: {days}")
print(f"  Hours: {hours}")
print(f"  Minutes: {minutes}")
print(f"  Seconds: {final_seconds}")
print("-" * 30)

# Final combined output for clarity:
print(f"The elapsed time is: {days}d, {hours}h, {minutes}m, {final_seconds}s.")

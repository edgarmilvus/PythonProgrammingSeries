
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

import os

LOG_FILE = "server_log.txt"

# --- 1. Input File Creation ---
log_content = """
[INFO] System startup initiated.
[WARNING] Disk space low on partition C.
[INFO] User 'admin' logged in.
[CRITICAL] Database connection failed. Retrying...
[INFO] Configuration loaded successfully.
[WARNING] High latency detected in network traffic.
[INFO] Background task started.
[CRITICAL] Memory allocation error. Service stopping.
[INFO] Health check passed.
[WARNING] Unrecognized user attempt.
"""

# Use 'w' mode to create or overwrite the log file
with open(LOG_FILE, 'w') as f:
    f.write(log_content.strip())

# --- 2. Log Analysis and Counting ---
total_lines = 0
warning_count = 0
critical_count = 0

print(f"Analyzing log file: {LOG_FILE}\n")

# Use 'r' mode and the 'with' statement for safe reading
try:
    with open(LOG_FILE, 'r') as log_file:
        # Iterate line by line (memory efficient)
        for line in log_file:
            total_lines += 1
            
            # Check for specific log levels
            if "[WARNING]" in line:
                warning_count += 1
            elif "[CRITICAL]" in line:
                critical_count += 1

except FileNotFoundError:
    print(f"Error: The file {LOG_FILE} was not found.")
except Exception as e:
    print(f"An unexpected error occurred during reading: {e}")

# --- 3. Output Summary ---
print("--- Analysis Summary ---")
print(f"Total Lines Processed: {total_lines}")
print(f"Total WARNING Entries: {warning_count}")
print(f"Total CRITICAL Entries: {critical_count}")

# Clean up the created file (optional, but good practice for exercises)
# os.remove(LOG_FILE)

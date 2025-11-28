
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

import datetime
import os

HISTORY_FILE = "app_history.log"

def record_action(action_message):
    """
    Records an action with a timestamp, appending it to the history log.
    """
    # 1. Generate current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Format the log entry, ensuring a newline character is included
    log_entry = f"{timestamp} | {action_message}\n"
    
    # 3. Use 'a' (append) mode to safely write the entry
    try:
        with open(HISTORY_FILE, 'a') as f:
            f.write(log_entry)
        print(f"Action recorded: {action_message}")
    except IOError as e:
        print(f"Error writing to history file: {e}")

# --- Demonstration ---

# Ensure the file is cleaned up before the first run for clear testing
if os.path.exists(HISTORY_FILE):
    os.remove(HISTORY_FILE)

print("--- Session 1: Initial Run ---")
record_action("Application started successfully.")
record_action("User loaded configuration profile 1.")

print("\n--- Session 2: Second Run (Appended Data) ---")
record_action("User initiated data backup.")
record_action("Application exited normally.")

# Verification (optional: read the file content to confirm appending)
print("\n--- Verifying File Content ---")
with open(HISTORY_FILE, 'r') as f:
    print(f.read().strip())

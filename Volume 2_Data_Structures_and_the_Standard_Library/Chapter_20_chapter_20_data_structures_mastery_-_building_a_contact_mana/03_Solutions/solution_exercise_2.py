
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

# Global list to store immutable log entries
event_log = []

def log_event(severity: str, component: str, message: str):
    """
    Formats logging details into a standardized tuple structure and appends it.
    Tuple structure: (timestamp, severity_level, component_name, message)
    """
    # Generate standardized timestamp string
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the immutable log entry tuple
    log_entry = (timestamp, severity.upper(), component, message)
    event_log.append(log_entry)
    print(f"Logged: {log_entry[1]} - {log_entry[2]}")


def search_by_severity(log_list: list[tuple], severity: str) -> list[tuple]:
    """
    Filters the log list and returns entries matching the specified severity.
    Uses list comprehension for efficiency.
    """
    target_severity = severity.upper()
    
    # Tuple Index 1 holds the severity level
    return [entry for entry in log_list if entry[1] == target_severity]


def count_component_errors(log_list: list[tuple], component: str) -> int:
    """
    Counts how many 'ERROR' level events have been recorded for a specific component.
    """
    count = 0
    # Index 1 is severity, Index 2 is component name
    for entry in log_list:
        if entry[1] == 'ERROR' and entry[2] == component:
            count += 1
            
    return count

# --- Testing 20.4.2 ---
print("\n--- Event Logging Test ---")
log_event("INFO", "API", "Service started successfully.")
log_event("WARNING", "DB", "High latency detected.")
log_event("ERROR", "API", "Authentication failed for user 101.")
log_event("ERROR", "DB", "Connection pool exhausted.")
log_event("INFO", "UI", "User logged in.")

errors = search_by_severity(event_log, "error")
print(f"\nFound {len(errors)} ERROR logs. Example: {errors[0]}")

api_errors = count_component_errors(event_log, "API")
db_errors = count_component_errors(event_log, "DB")

print(f"API Component Errors: {api_errors}")
print(f"DB Component Errors: {db_errors}")

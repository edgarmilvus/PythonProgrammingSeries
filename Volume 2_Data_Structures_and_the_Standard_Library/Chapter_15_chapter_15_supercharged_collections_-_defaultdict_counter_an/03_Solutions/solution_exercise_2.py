
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

from collections import Counter

# Simulated Input Log
log_events = [
    '200_OK', '404_NOT_FOUND', '200_OK', '500_SERVER_ERROR', '302_REDIRECT',
    '200_OK', '404_NOT_FOUND', '200_OK', '200_OK', '401_UNAUTHORIZED',
    '500_SERVER_ERROR', '200_OK', '200_OK', '404_NOT_FOUND', '401_UNAUTHORIZED',
    '999_CRITICAL_DB_FAIL', '200_OK', '200_OK', '404_NOT_FOUND', '200_OK'
]
known_critical_errors = ['500_SERVER_ERROR', '401_UNAUTHORIZED', '999_CRITICAL_DB_FAIL']
CRITICAL_THRESHOLD = 2

# 1. Frequency Tally
event_counts = Counter(log_events)

print("--- Exercise 2: Log File Anomaly Detection (Counter) ---")

# 2. Most Common
most_common = event_counts.most_common(3)
print("\nTop 3 Most Common Events:")
for event, count in most_common:
    print(f"  {event}: {count} times")

# 3. Anomaly Check (Events occurring only once)
# Filter the Counter items where the count equals 1
anomalies = [event for event, count in event_counts.items() if count == 1]
print("\nPotential Rare Anomalies (Count = 1):")
if anomalies:
    print(f"  {anomalies}")
else:
    print("  None found.")

# 4. Critical Threshold Alert
print(f"\nCritical Threshold Check (Threshold = {CRITICAL_THRESHOLD}):")
alerts_raised = False
for error in known_critical_errors:
    # Accessing event_counts[error] returns 0 if the error didn't occur, which is safe.
    count = event_counts[error]
    if count > CRITICAL_THRESHOLD:
        print(f"  ALERT: Critical Error '{error}' exceeded threshold! Count: {count}")
        alerts_raised = True

if not alerts_raised:
    print("  No critical errors exceeded the threshold.")

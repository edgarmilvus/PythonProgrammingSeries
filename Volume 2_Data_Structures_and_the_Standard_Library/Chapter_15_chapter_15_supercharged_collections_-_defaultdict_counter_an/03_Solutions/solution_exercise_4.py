
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

from collections import defaultdict, Counter, deque

# Simulated Event Stream (including filler events to test deque maxlen=10)
event_stream = [
    (1698800001, 'INFO', 'User login successful.'),
    (1698800005, 'WARNING', 'High latency detected.'),
    (1698800010, 'CRITICAL', 'Database connection lost (OLDEST).'), # Evicted later
    (1698800015, 'INFO', 'Routine backup started.'),
    (1698800020, 'CRITICAL', 'Filler 1: Memory leak detected.'),
    (1698800025, 'CRITICAL', 'Filler 2: File system read error.'),
    (1698800030, 'CRITICAL', 'Filler 3: High CPU usage spike.'),
    (1698800035, 'CRITICAL', 'Filler 4: Network saturation.'),
    (1698800040, 'CRITICAL', 'Filler 5: Authentication failure flood.'),
    (1698800045, 'CRITICAL', 'Filler 6: Service unavailable.'),
    (1698800050, 'CRITICAL', 'Filler 7: Disk full error.'),
    (1698800055, 'CRITICAL', 'Filler 8: Backup failed.'), # 9th critical event
    (1698800090, 'CRITICAL', 'Secondary server failure (10th).'), # Fills deque
    (1698800095, 'CRITICAL', 'Main server failure (11th - NEWEST).'), # Evicts the oldest (1698800010)
    (1698800100, 'WARNING', 'Disk space low.')
]

# 1. Initialize Collections
priority_groups = defaultdict(list)
alert_counts = Counter()
critical_alert_history = deque(maxlen=10)

# 2. Process the Event Stream
for timestamp, severity, message in event_stream:
    event_tuple = (timestamp, severity, message)

    # 4. Conditional Logic and Updates
    if severity == 'CRITICAL':
        # Track frequency
        alert_counts[severity] += 1
        # Add to fixed-size history (deque handles maxlen=10)
        critical_alert_history.append(event_tuple)

    elif severity == 'WARNING':
        # Track frequency
        alert_counts[severity] += 1

    # Group the message by severity (for all severities)
    priority_groups[severity].append(message)

# 5. Reporting
print("--- Exercise 4: Real-Time Prioritization and Alerting (Integration) ---")

print("\n--- 1. Event Frequency Report (Counter) ---")
print(f"Total CRITICAL Events: {alert_counts['CRITICAL']}")
print(f"Total WARNING Events: {alert_counts['WARNING']}")

print("\n--- 2. Critical Alert History (Deque maxlen=10) ---")
print(f"History Size: {len(critical_alert_history)}")
print("Note: The event starting at 1698800010 (OLDEST) should be evicted.")

for i, alert in enumerate(critical_alert_history):
    # Display index and the message
    print(f"  {i+1:02d}. Severity={alert[1]}, Message='{alert[2]}'")

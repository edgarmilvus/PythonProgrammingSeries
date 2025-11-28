
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

import json

# 1. Define the complex nested dictionary
sensor_log = {
    "device_id": "HVAC-001",
    "timestamp": 1678886400,
    "readings": [
        {"pressure": 101.3, "temperature": 22.5, "unit": "C"},
        {"temperature": 23.1, "pressure": 101.2, "unit": "C"}
    ],
    "location": "Server Room A"
}

print("\n--- Exercise 3 Solution ---")

# 2, 3, 4. Serialize with indent=2 AND sort_keys=True
# This forces the keys (device_id, location, readings, timestamp) to be alphabetized.
standardized_json = json.dumps(
    sensor_log,
    indent=2,
    sort_keys=True
)

# 5. Print the resulting standardized JSON string
print("Standardized JSON Output (Keys Sorted Alphabetically):")
print(standardized_json)

# Observation: The top-level keys are now in alphabetical order:
# "device_id", "location", "readings", "timestamp"
# And the nested keys are also sorted: "pressure", "temperature", "unit"

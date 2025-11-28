
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

sensor_readings = [
    "101.5", "105.2", "MAINTENANCE", "112.9", "145.0",
    "155.1", "130.0", "MAINTENANCE", "98.7"
]

CRITICAL_THRESHOLD = 150.0
shutdown_initiated = False

print("\n--- Exercise 3: Sensor Log Analysis with Flow Control ---")
print(f"Starting analysis. Critical threshold: {CRITICAL_THRESHOLD}")

for reading_str in sensor_readings:
    
    # 1. Use 'continue' to skip non-numeric maintenance records
    if reading_str == 'MAINTENANCE':
        print(f"-> [SKIP] Maintenance record encountered.")
        continue # Skip the rest of the loop body for this iteration
        
    # Convert string reading to float for numerical comparison
    try:
        reading = float(reading_str)
    except ValueError:
        # Should not happen with the provided data, but good practice
        print(f"-> [ERROR] Invalid reading format: {reading_str}")
        continue
    
    # 2. Use 'break' for emergency shutdown if threshold is breached
    if reading > CRITICAL_THRESHOLD:
        print(f"-> [CRITICAL] Reading {reading} exceeds {CRITICAL_THRESHOLD}.")
        shutdown_initiated = True
        break # Terminate the loop immediately
        
    # 3. Normal processing for valid readings
    print(f"-> [OK] Processed temperature: {reading}")

# Final Output based on loop termination reason
if shutdown_initiated:
    print("--- EMERGENCY SHUTDOWN INITIATED ---")
else:
    print("--- Analysis Completed Successfully ---")

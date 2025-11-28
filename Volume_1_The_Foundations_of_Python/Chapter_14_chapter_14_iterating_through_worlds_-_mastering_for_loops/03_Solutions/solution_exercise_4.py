
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

simulated_log = [
    88.5, 92.1, 96.0, 97.5, 98.1,  # Critical break occurs after 98.1
    90.0, 91.2, 99.0, 101.0
]

CRITICAL_THRESHOLD = 95.0
CONSECUTIVE_LIMIT = 3
consecutive_warnings = 0
system_failed = False

print("\n--- Exercise 4: Consecutive Failure Detection ---")
print(f"Threshold: {CRITICAL_THRESHOLD}. Consecutive limit: {CONSECUTIVE_LIMIT}")

for reading in simulated_log:
    print(f"Processing reading: {reading}")
    
    if reading > CRITICAL_THRESHOLD:
        # Reading is in Warning State: Increment counter
        consecutive_warnings += 1
        
        # Check if the failure limit has been reached
        if consecutive_warnings >= CONSECUTIVE_LIMIT:
            system_failed = True
            print(f"  !!! CRITICAL: {consecutive_warnings} consecutive warnings reached.")
            break # Terminate the loop immediately due to hard failure
            
    else:
        # Reading is safe: Reset the consecutive counter
        consecutive_warnings = 0
        
# Final Reporting
if system_failed:
    print("\n==============================================")
    print("CRITICAL FAILURE DETECTED: System Shut Down.")
    print("==============================================")
else:
    print("\nAnalysis Complete. No critical consecutive failures detected.")

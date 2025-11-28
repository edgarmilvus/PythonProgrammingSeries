
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

# 1. New parameter 'memory_usage' added to the function signature
def generate_report(device_name, temp_celsius, load_avg, memory_usage):
    # 2. Updated Docstring to include the new parameter
    """
    Generates a comprehensive formatted summary of device operational status.
    
    Parameters:
    device_name (str): The name of the server or device.
    temp_celsius (float): The current operating temperature in Celsius.
    load_avg (float): The system load average over the last minute.
    memory_usage (float): The current memory utilization as a decimal fraction (e.g., 0.75).
    """
    
    # Simple status logic
    status_msg = "HEALTHY" if temp_celsius < 60 else "WARNING"
    
    print("-" * 35)
    print("SYSTEM HEALTH REPORT")
    print("-" * 35)
    
    # Formatting structure: 20 chars for label (left-aligned), 15 chars for value (right-aligned)
    print(f"{'DEVICE NAME:':<20} {device_name:>15}")
    print(f"{'TEMPERATURE:':<20} {temp_celsius:>15.1f} C")
    print(f"{'LOAD AVERAGE:':<20} {load_avg:>15.2f}")
    
    # 3. Format the New Metric: Memory Usage
    # Right-aligned (>) 15 width, 1 decimal percentage (.1%)
    print(f"{'MEMORY USAGE:':<20} {memory_usage:>15.1%}")
    
    print(f"{'STATUS:':<20} {status_msg:>15}")
    print("-" * 35)

# 4. Testing the modified function
print("\n--- Test Run 1: Normal Operation ---")
generate_report("Web Proxy 03", 48.9, 0.78, 0.456)

print("\n--- Test Run 2: High Load/Memory Warning ---")
generate_report("Database Cluster", 62.1, 4.12, 0.91)

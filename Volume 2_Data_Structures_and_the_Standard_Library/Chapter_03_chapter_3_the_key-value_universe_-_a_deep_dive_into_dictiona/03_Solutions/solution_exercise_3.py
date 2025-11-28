
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

# --- Exercise 2 Solution ---

# Conversion formula: T_F = (T_C * 9/5) + 32

# 1. Dictionary Comprehension for Cleaning, Transformation, and Keying
normalized_data = {
    # Key: timestamp
    reading['timestamp']: {
        # Value: Transformed dictionary
        'temp_f': round((reading['temp_c'] * 9/5) + 32, 1),
        'humidity': reading['humidity']
    }
    # Iterate through the list of readings
    for reading in SENSOR_READINGS
    # Filter: Only include readings where temp_c is a numeric type (int or float)
    if isinstance(reading['temp_c'], (int, float))
}

# 2. View Analysis
print("\n--- Testing Exercise 2 ---")
print(f"Total number of normalized entries: {len(normalized_data)}")

print("\nFahrenheit Temperatures (using .values() view):")
# Iterate over the values view for efficiency
for data in normalized_data.values():
    print(f"Temperature: {data['temp_f']} F")

# Verification of the structure (should exclude the 'ERROR' reading)
# print(normalized_data)

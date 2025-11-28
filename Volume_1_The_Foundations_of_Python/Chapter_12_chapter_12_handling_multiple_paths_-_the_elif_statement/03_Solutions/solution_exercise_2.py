
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

def classify_temperature(temp):
    """
    Classifies a temperature (Celsius) into meteorological categories.

    Args:
        temp (float): The temperature in Celsius.
    """
    classification = ""

    # Start checking from the lowest temperature range
    if temp < -10:
        classification = "Extreme Cold"
    
    # If not Extreme Cold, check if it's -10 up to (but not including) 0
    elif temp < 0:
        classification = "Freezing"
        
    # If not Freezing, check if it's 0 up to (but not including) 15
    elif temp < 15:
        classification = "Cool"
        
    # If not Cool, check if it's 15 up to (but not including) 30
    elif temp < 30:
        classification = "Mild/Warm"
        
    # If none of the above, it must be 30 or above
    else:
        classification = "Hot"
        
    print(f"Temperature: {temp}°C -> Classification: {classification}")

# Example Usage:
print("\n--- Temperature Classification Examples ---")
classify_temperature(-15.5)  # Extreme Cold
classify_temperature(-5.0)   # Freezing
classify_temperature(0.0)    # Cool (0 is included in the < 15 range)
classify_temperature(14.9)   # Cool
classify_temperature(25.0)   # Mild/Warm
classify_temperature(30.0)   # Hot

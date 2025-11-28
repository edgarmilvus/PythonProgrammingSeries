
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

def celsius_to_fahrenheit(celsius_temp):
    """
    Converts a temperature value from Celsius to Fahrenheit.

    The conversion uses the standard formula: F = C * (9/5) + 32.

    Parameters:
        celsius_temp (float or int): The temperature value in degrees Celsius.
                                     This value can be positive, negative, or zero.

    Returns:
        float: The converted temperature value in degrees Fahrenheit.
    """
    # Ensure float division (9/5 = 1.8) for precision in the calculation.
    fahrenheit_temp = celsius_temp * (9 / 5) + 32
    return fahrenheit_temp

# --- Testing the Function and Docstring ---
print("\n--- Exercise 3: Celsius to Fahrenheit Converter ---")

# Test Case 1: Freezing point (0 C)
print(f"0°C is {celsius_to_fahrenheit(0)}°F")

# Test Case 2: Boiling point (100 C)
print(f"100°C is {celsius_to_fahrenheit(100)}°F")

# Test Case 3: Room temperature (25 C)
print(f"25°C is {celsius_to_fahrenheit(25)}°F")

# Optional: Demonstrate Docstring access
# print("\n--- Docstring Content ---")
# help(celsius_to_fahrenheit)


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

import math

def cartesian_to_polar(x: float, y: float) -> tuple[float, float]:
    """
    Converts Cartesian coordinates (x, y) to polar coordinates (distance, angle in degrees).
    
    Args:
        x: The x-coordinate (float).
        y: The y-coordinate (float).
        
    Returns:
        A tuple containing (distance, angle_in_degrees).
    """
    # 1. Calculate distance (hypotenuse) using math.hypot (numerically stable)
    distance = math.hypot(x, y)
    
    # 2. Calculate angle in radians using math.atan2 (handles all four quadrants)
    angle_radians = math.atan2(y, x)
    
    # 3. Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)
    
    return distance, angle_degrees

# Test case: x = -15.0, y = 8.0 (Second Quadrant)
x2, y2 = -15.0, 8.0
d2, theta2 = cartesian_to_polar(x2, y2)

print("\n--- Exercise 2: Polar Conversion ---")
print(f"Cartesian Input: ({x2}, {y2})")
print(f"Distance from Origin: {d2:.3f}")
print(f"Angle (Degrees):      {theta2:.2f}°")

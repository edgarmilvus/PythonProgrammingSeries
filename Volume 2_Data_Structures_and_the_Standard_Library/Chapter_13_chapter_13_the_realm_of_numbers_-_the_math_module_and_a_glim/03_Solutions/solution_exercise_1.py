
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

import math

def calculate_sphere_metrics(radius: float) -> tuple[float, float]:
    """
    Calculates the volume and surface area of a sphere using math.pi.
    
    Args:
        radius: The radius of the sphere (float).
        
    Returns:
        A tuple containing (volume, surface_area).
    """
    # Volume V = (4/3) * pi * r^3
    # Use 4.0 / 3.0 to ensure floating-point division
    volume = (4.0 / 3.0) * math.pi * (radius ** 3)
    
    # Surface Area A = 4 * pi * r^2
    surface_area = 4.0 * math.pi * (radius ** 2)
    
    return volume, surface_area

# Test case
r1 = 12.75
v1, a1 = calculate_sphere_metrics(r1)

print("--- Exercise 1: Sphere Metrics ---")
print(f"Radius: {r1}")
# Requirement: Volume displayed with exactly 6 decimal places
print(f"Volume:       {v1:.6f} cubic units")
# Requirement: Surface Area displayed with exactly 4 decimal places
print(f"Surface Area: {a1:.4f} square units")


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

import math

def simulate_trajectory_precise(V0: float, angle_deg: float, g: float = 9.81):
    """
    Simulates a projectile trajectory, using math.isclose() to detect landing precisely.
    
    Args:
        V0: Initial velocity (m/s).
        angle_deg: Launch angle in degrees.
        g: Acceleration due to gravity (m/s^2).
    """
    # Convert angle to radians
    angle_rad = math.radians(angle_deg)
    
    # Initial vertical velocity component (constant)
    Vy0 = V0 * math.sin(angle_rad)
    
    t = 0.0
    dt = 0.01  # Time step (0.01 seconds)
    
    print("\n--- Exercise 4: Trajectory Precision ---")
    print(f"Simulating trajectory (V0={V0}, Angle={angle_deg}°)...")
    
    # Loop until height is numerically close to zero
    while True:
        # Height formula H(t) = (V_y0 * t) - 0.5 * g * t^2
        height = (Vy0 * t) - (0.5 * g * (t ** 2))
        
        # CRITICAL: Use math.isclose() to check if height is numerically near 0.0
        # abs_tol=0.01 means we stop when height is within 0.01 meters of the ground.
        # The 't > 0.1' condition prevents immediate termination at the start (t=0).
        if math.isclose(height, 0.0, abs_tol=0.01) and t > 0.1:
            break
        
        # Safety break for cases where the simulation overshoots far below ground
        if height < -1.0:
            break

        t += dt
    
    print(f"Final Time (T): {t:.3f} seconds")
    print(f"Final Height (H): {height:.3f} meters")
    print("Termination condition used: math.isclose(H, 0.0, abs_tol=0.01)")

# Test case
simulate_trajectory_precise(V0=50.0, angle_deg=45.0)

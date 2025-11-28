
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

# Source File: solution_exercise_6.py
# Description: Solution for Exercise 6
# ==========================================

import math
import time
import random

# --- Exercise 1: Analyzing Spherical Geometry and Precision ---

def calculate_sphere_metrics(radius: float) -> tuple[float, float]:
    """
    Calculates the volume and surface area of a sphere using math.pi.
    """
    # Volume V = (4/3) * pi * r^3
    volume = (4.0 / 3.0) * math.pi * (radius ** 3)
    
    # Surface Area A = 4 * pi * r^2
    surface_area = 4.0 * math.pi * (radius ** 2)
    
    return volume, surface_area

# Test case 1
r1 = 12.75
v1, a1 = calculate_sphere_metrics(r1)

print("--- Exercise 1: Sphere Metrics ---")
print(f"Radius: {r1}")
# Volume formatted to 6 decimal places
print(f"Volume:       {v1:.6f} cubic units")
# Surface Area formatted to 4 decimal places
print(f"Surface Area: {a1:.4f} square units")
print("-" * 30)


# --- Exercise 2: Mapping Coordinates and Angles ---

def cartesian_to_polar(x: float, y: float) -> tuple[float, float]:
    """
    Converts Cartesian coordinates (x, y) to polar coordinates (distance, angle in degrees).
    """
    # 1. Calculate distance (D) using math.hypot (robust for large/small numbers)
    distance = math.hypot(x, y)
    
    # 2. Calculate angle (theta) in radians using math.atan2 (handles quadrants correctly)
    angle_radians = math.atan2(y, x)
    
    # 3. Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)
    
    return distance, angle_degrees

# Test case 2: Object in the second quadrant
x2, y2 = -15.0, 8.0
d2, theta2 = cartesian_to_polar(x2, y2)

print("--- Exercise 2: Polar Conversion ---")
print(f"Cartesian Input: ({x2}, {y2})")
print(f"Distance from Origin: {d2:.3f}")
print(f"Angle (Degrees):      {theta2:.2f}°")
print("-" * 30)


# --- Exercise 3: Factorial and Safe Storage Estimation ---

def calculate_storage_needs(N: int):
    """
    Calculates permutations and estimates storage needs using math.factorial, math.ceil, and math.floor.
    """
    # 1. Calculate total permutations P
    permutations = math.factorial(N)
    
    # Define storage capacity per unit (must be float for division)
    UNIT_CAPACITY = 1_000_000.0
    
    # 2. Calculate raw storage units needed
    raw_units = permutations / UNIT_CAPACITY
    
    # 3. Determine minimum safe integer units (must round UP)
    safe_units_ceil = math.ceil(raw_units)
    
    # 4. Determine maximum number of full units (must round DOWN)
    full_units_floor = math.floor(raw_units)
    
    print(f"Permutation Set Size (N): {N}")
    print(f"Total Permutations (P):   {permutations:,}")
    print(f"Raw Storage Units Needed: {raw_units:.4f}")
    print(f"Minimum Safe Units (ceil): {int(safe_units_ceil):,}")
    print(f"Maximum Full Units (floor): {int(full_units_floor):,}")

print("--- Exercise 3: Storage Estimation ---")
calculate_storage_needs(14)
print("-" * 30)


# --- Exercise 4: Interactive Challenge: Refining Trajectory Prediction Precision ---

def simulate_trajectory_precise(V0: float, angle_deg: float, g: float = 9.81):
    """
    Simulates a projectile trajectory, using math.isclose() to detect landing precisely.
    """
    # Convert angle to radians
    angle_rad = math.radians(angle_deg)
    
    # Initial vertical velocity component
    Vy0 = V0 * math.sin(angle_rad)
    
    t = 0.0
    dt = 0.01  # Time step
    
    print(f"Simulating trajectory (V0={V0}, Angle={angle_deg}°)...")
    
    # Loop until height is numerically close to zero
    while True:
        # Height formula H(t) = (Vy0 * t) - 0.5 * g * t^2
        height = (Vy0 * t) - (0.5 * g * (t ** 2))
        
        # CRITICAL: Check if height is close to zero (landing condition)
        # Using abs_tol=0.01 means we stop when height is within 1 cm of the ground.
        if math.isclose(height, 0.0, abs_tol=0.01) and t > 0.1:
            # The 't > 0.1' prevents immediate termination at t=0
            break
        
        # Safety break if we overshoot far below ground level
        if height < -1.0:
            break

        t += dt
    
    print(f"Final Time (T): {t:.3f} seconds")
    print(f"Final Height (H): {height:.3f} meters")
    print("Termination condition used: math.isclose(height, 0.0, abs_tol=0.01)")


print("--- Exercise 4: Trajectory Precision ---")
simulate_trajectory_precise(V0=50.0, angle_deg=45.0)
print("-" * 30)


# --- Exercise 5: Conceptualizing Numerical Efficiency (NumPy Prelude) ---

def measure_scalar_performance(N: int):
    """
    Measures the time taken to calculate the square root of N numbers using standard Python scalar operations.
    """
    print(f"Generating {N:,} random numbers...")
    # 1. Generate a large list of random floats
    data = [random.uniform(1.0, 1000.0) for _ in range(N)]
    results = []
    
    print("Starting scalar square root calculation...")
    
    # 2. Record start time
    start_time = time.time()
    
    # 3. Iterate and calculate square root using math.sqrt (scalar operation)
    for number in data:
        results.append(math.sqrt(number))
        
    # 4. Record end time
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    # 5. Print results
    print(f"Calculation finished. Processed {len(results):,} results.")
    print(f"Total elapsed time: {elapsed_time:.3f} seconds")
    
    # 6. Conclusion
    print("\n--- Efficiency Context ---")
    print("This demonstrates the inherent limitation of scalar operations for massive datasets.")
    print("Vectorized libraries (like NumPy) avoid the Python loop overhead entirely,")
    print("achieving orders of magnitude faster performance.")

print("--- Exercise 5: Efficiency Spotlight ---")
measure_scalar_performance(1_000_000)
print("-" * 30)

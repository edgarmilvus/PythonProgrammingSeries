
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

import sys
import time

# --- Exercise 1: The Sensor Data Translator ---

def get_sensor_reading():
    """Simulates returning sensor data as an immutable tuple: (timestamp_str, temp_celsius, humidity_percent)."""
    # Sample data: (Timestamp, Celsius, Humidity)
    return ("2023-10-27 14:30:00", 25.5, 62)

# 1. Call the function
sensor_data_tuple = get_sensor_reading()

# 2. Use direct tuple unpacking to assign values
time_str, celsius, humidity = sensor_data_tuple

# 3. Implement the conversion formula: F = (C * 9/5) + 32
fahrenheit = (celsius * 9/5) + 32

# 4. Print the results
print("--- Exercise 1: Sensor Data Translator ---")
print(f"Original Timestamp: {time_str}")
print(f"Original Temperature (C): {celsius}°C")
print(f"Humidity: {humidity}%")
print(f"Converted Temperature (F): {fahrenheit:.2f}°F")
print("-" * 40)


# --- Exercise 2: Generator Efficiency and Immutable State ---

# 1. Import sys (done above)
SEQUENCE_SIZE = 100000

print("\n--- Exercise 2: Generator Efficiency ---")

# 3. Create a generator expression for the tuple conversion
# Generator expressions use parentheses () and produce values on demand.
squared_gen_for_tuple = (i * i for i in range(SEQUENCE_SIZE))

# 4. Convert the generator output to a tuple and measure time
start_time_tuple = time.perf_counter()
squared_tuple = tuple(squared_gen_for_tuple)
end_time_tuple = time.perf_counter()

# 5. Crucially: Re-create the generator, as the previous one is now exhausted
squared_gen_for_list = (i * i for i in range(SEQUENCE_SIZE))

# Convert the generator output to a list and measure time
start_time_list = time.perf_counter()
squared_list = list(squared_gen_for_list)
end_time_list = time.perf_counter()

# 6. Measure and print memory sizes
tuple_size = sys.getsizeof(squared_tuple)
list_size = sys.getsizeof(squared_list)

print(f"Sequence Size: {SEQUENCE_SIZE:,} elements")
print(f"Tuple Size (bytes): {tuple_size:,}")
print(f"List Size (bytes): {list_size:,}")
print(f"Memory Difference (List overhead): {list_size - tuple_size:,} bytes")
print(f"Tuple Creation Time: {(end_time_tuple - start_time_tuple) * 1000:.4f} ms")
print(f"List Creation Time: {(end_time_list - start_time_list) * 1000:.4f} ms")

# 7. Comment on why tuple size is smaller
# The list requires extra overhead for storing pointers and managing allocation 
# space to support dynamic resizing and modification (mutability), which 
# a tuple (fixed size, immutable) does not need, resulting in lower memory usage.
print("-" * 40)


# --- Exercise 3: Immutable Configuration Management with Nested Tuples ---

print("\n--- Exercise 3: Immutable Configuration Management ---")

# 1. Define server configuration tuples (Name, IP, Port)
SERVER_A = ("Web_Prod", "192.168.1.10", 80)
SERVER_B = ("DB_Staging", "10.0.0.5", 5432)
SERVER_C = ("API_Test", "172.16.0.20", 443)

# 2. Create a master configuration tuple (tuple of tuples)
APPLICATION_CONFIGS = (SERVER_A, SERVER_B, SERVER_C)

# 3. Define the function to retrieve details
def get_config_detail(config_tuple, server_index, detail_index):
    """Retrieves a specific detail from the nested configuration tuple."""
    try:
        # Accesses the inner tuple first, then the element within it
        return config_tuple[server_index][detail_index]
    except IndexError:
        return "Error: Invalid index provided."

# 4. Retrieve and print the IP address of the second server (index 1)
# IP address is the second element (index 1) of the inner tuple
server_name = get_config_detail(APPLICATION_CONFIGS, 1, 0)
server_ip = get_config_detail(APPLICATION_CONFIGS, 1, 1)

print(f"Configuration loaded successfully (immutable state).")
print(f"Server Name: {server_name}")
print(f"Retrieved IP Address for {server_name}: {server_ip}")

# 5. Attempt modification to demonstrate immutability
print("\nAttempting to change the port of SERVER_A (index [0][2]):")
try:
    # This line attempts to assign a new value to an element within an inner tuple
    APPLICATION_CONFIGS[0][2] = 8080
except TypeError as e:
    print(f"Successfully blocked modification: {e}")
    print("The configuration remains fixed due to tuple immutability.")
print("-" * 40)


# --- Exercise 4: Interactive Challenge - Refactoring the Asset Tracker (Tuple Immutability) ---

print("\n--- Exercise 4: Interactive Challenge (Immutable Path) ---")

# 1. Define function to create a waypoint tuple
def create_waypoint(id, lat, lon, timestamp):
    """Returns a new immutable waypoint tuple: (ID, Lat, Lon, Timestamp)."""
    return (id, lat, lon, timestamp)

# 2. Initialize the asset path as an empty tuple
asset_path = ()

# 3. Define function to record a waypoint (returns a new tuple)
def record_waypoint(current_path, new_waypoint):
    """Records a waypoint by concatenating the current path with the new waypoint.
    Returns a new tuple (simulation of appending)."""
    
    # Use tuple concatenation (+). The new_waypoint must be wrapped in a tuple 
    # using the trailing comma syntax: (new_waypoint,).
    return current_path + (new_waypoint,)

# 4. Use record_waypoint three times to build the path
wp1 = create_waypoint(1, 34.0522, -118.2437, "2023-11-01T10:00:00Z")
asset_path = record_waypoint(asset_path, wp1)

wp2 = create_waypoint(2, 34.0525, -118.2440, "2023-11-01T10:05:00Z")
asset_path = record_waypoint(asset_path, wp2)

wp3 = create_waypoint(3, 34.0530, -118.2445, "2023-11-01T10:10:00Z")
asset_path = record_waypoint(asset_path, wp3)

# 5. Print the final asset_path
print(f"Path recorded (Total waypoints: {len(asset_path)})")
print("First Waypoint:", asset_path[0])
print("Final Waypoint:", asset_path[-1])
print(f"Path is a {type(asset_path)} of {type(asset_path[0])}s.")

# 6. Demonstrate immutability attempt
print("\nAttempting to change the Latitude (index 1) of Waypoint 1:")
try:
    # Attempt to change the element at index 1 of the inner tuple at index 0
    asset_path[0][1] = 40.7 
except TypeError as e:
    print(f"Modification attempt failed: {e}")
    print("The historical waypoint data is protected by tuple immutability.")
print("-" * 40)

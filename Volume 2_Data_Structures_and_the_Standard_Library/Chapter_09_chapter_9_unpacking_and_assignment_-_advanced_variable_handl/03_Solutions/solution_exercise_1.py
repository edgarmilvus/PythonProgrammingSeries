
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

# --- Exercise 9.4.1 Solution: Data Swapping and Configuration Reversal ---

# 1. Initialize variables
temp_a = 10
temp_b = 20
print("--- Exercise 9.4.1 ---")
print(f"Start: temp_a={temp_a}, temp_b={temp_b}")

# Pythonic simultaneous swap using a single assignment line
# The right side (temp_b, temp_a) is evaluated first, creating a tuple (20, 10),
# which is then unpacked onto the left side.
temp_a, temp_b = temp_b, temp_a
print(f"Swap Result: temp_a={temp_a}, temp_b={temp_b}")

# 2. Sequence Reversal and Selective Unpacking
config = ['TCP', 8080, 'Listening']

# Input structure: [Protocol, Port, Status]
# We want to assign Protocol to p_name (position 0) and Port to p_num (position 1).
# We use _ to ignore the status (position 2).
p_name, p_num, _ = config

print(f"\nConfiguration Unpacking:")
print(f"Protocol Name (p_name): {p_name}")
print(f"Port Number (p_num): {p_num}")


# --- Exercise 9.4.2 Solution: Server Log Truncation and Selective Extraction ---

log_entry = ('2023-10-27T14:30:00', '192.168.1.10', '10.0.0.5', 'jdoe', 'LOGIN_ATTEMPT', 200)

# Log structure: (T, IP1, IP2, User, Action, Result)
# We only need User (index 3) and Result (index 5).
# Use the underscore (_) as a placeholder for all discarded fields.
_, _, _, user, _, status_code = log_entry

print("\n--- Exercise 9.4.2 ---")
print(f"Extracted User ID: {user}")
print(f"Extracted Status Code: {status_code}")


# --- Exercise 9.4.3 Solution: Header, Footer, and Variable Payload Segmentation ---

# Packet structure: [Header ID, Version, *Payload, Checksum]
data_packet = [101, 1.2, 'A', 'B', 'C', 'D', 'E', 9876]

# Use extended unpacking to capture the fixed start (2 elements), 
# the variable middle (*payload), and the fixed end (1 element).
header_id, header_version, *payload, checksum = data_packet

print("\n--- Exercise 9.4.3 ---")
print(f"Header ID: {header_id}, Version: {header_version}")
print(f"Checksum: {checksum}")
print(f"Payload Type: {type(payload)}")
print(f"Payload Contents: {payload}")


# --- Exercise 9.4.4 Solution: Interactive Challenge (Refactoring) ---

def process_user_record_unpacked(record):
    """
    Processes a variable-length user record using advanced unpacking.
    Structure: (User ID, Name, *Roles, Status)
    Ignores the Name field and collects all roles into a list.
    """
    
    # 1. user_id takes the first element (ID)
    # 2. _ takes the second element (Name) - ignored
    # 3. *assigned_roles collects all elements up to the last one (Roles list)
    # 4. status takes the last element (Account Status)
    user_id, _, *assigned_roles, status = record
    
    return {
        'user_id': user_id,
        'assigned_roles': assigned_roles,
        'status': status
    }

# Test Cases
user_1 = (5001, "Dr. Smith", "Lead_Researcher", "Project_Manager", "Active") # Two roles
user_2 = (5002, "J. Doe", "Intern", "Inactive") # One role
user_3 = (5003, "C. Jones", "Inactive") # Edge case: Zero roles (ID, Name, Status)

result_1 = process_user_record_unpacked(user_1)
result_2 = process_user_record_unpacked(user_2)
result_3 = process_user_record_unpacked(user_3)

print("\n--- Exercise 9.4.4 ---")
print(f"User 5001 (Multiple Roles): {result_1}")
print(f"User 5002 (Single Role): {result_2}")
print(f"User 5003 (Zero Roles): {result_3}")
# Note: *assigned_roles correctly results in an empty list [] when no elements remain.

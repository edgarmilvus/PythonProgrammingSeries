
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# Exercise 5 Solution
print("--- Exercise 5: Configuration Data Type Enforcement ---")

def enforce_types(config_dict):
    """
    Takes a dictionary of string configuration settings and enforces specific 
    data types using explicit conversion functions, handling errors gracefully.
    """
    enforced_config = {}

    # 1. Standard Integer Conversions (Assuming these are generally safe)
    try:
        enforced_config['port'] = int(config_dict['port'])
        enforced_config['buffer_size'] = int(config_dict['buffer_size'])
    except ValueError as e:
        print(f"CRITICAL ERROR: Failed to convert a mandatory integer setting. Error: {e}")

    # 2. Float Conversion
    try:
        enforced_config['retry_delay'] = float(config_dict['retry_delay'])
    except ValueError:
        print("Warning: Retry delay conversion failed. Defaulting to 1.0.")
        enforced_config['retry_delay'] = 1.0

    # 3. String (No conversion needed)
    enforced_config['database_name'] = config_dict['database_name']

    # 4. Boolean Conversion (Must handle string 'False' explicitly)
    # The built-in bool() is misleading for config files (bool("False") is True)
    logging_str = config_dict['logging_enabled'].lower()
    if logging_str == "true":
        enforced_config['logging_enabled'] = True
    elif logging_str == "false":
        enforced_config['logging_enabled'] = False
    else:
        enforced_config['logging_enabled'] = False
        print("Warning: Invalid boolean value for logging_enabled. Set to False.")

    # 5. Error-Prone Integer Conversion (Robust try/except block)
    key = 'max_connections'
    try:
        # Attempt conversion
        enforced_config[key] = int(config_dict[key])
        print(f"Successfully converted '{key}' to integer.")
    except ValueError:
        default_value = 5
        # If conversion fails due to "invalid_number", set the default
        print(f"Conversion failed for '{key}' ('{config_dict[key]}'). Using default value: {default_value}")
        enforced_config[key] = default_value
        
    return enforced_config

# Initial Configuration (All Strings)
config_data = {
    "port": "8080",
    "buffer_size": "4096",
    "retry_delay": "1.5",
    "logging_enabled": "True",
    "database_name": "prod_db",
    "max_connections": "invalid_number" 
}

print("\n--- Starting Type Enforcement Process ---")
processed_config = enforce_types(config_data)

print("\n--- Final Processed Configuration ---")
import pprint
pprint.pprint(processed_config)

print("\n--- Verification of Types ---")
print(f"Port Type: {type(processed_config['port'])}")
print(f"Retry Delay Type: {type(processed_config['retry_delay'])}")
print(f"Logging Enabled Type: {type(processed_config['logging_enabled'])}")
print(f"Max Connections Type (Set by default): {type(processed_config['max_connections'])}")

print("-" * 50)

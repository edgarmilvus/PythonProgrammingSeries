
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

# --- Exercise 3 Solution ---

def deep_merge_config(default, override):
    """
    Recursively merges two dictionaries. 
    Values from 'override' take precedence. If both values are dictionaries, 
    the function recurses.
    """
    # Start with a copy of the default dictionary to work on
    result = default.copy()

    # Iterate through all key-value pairs in the override dictionary
    for key, value in override.items():
        # Check if the key exists in the result (default config)
        if key in result:
            # Check if both the default value and the override value are dictionaries
            if isinstance(result[key], dict) and isinstance(value, dict):
                # Recursive Case: Deep merge the nested dictionaries
                result[key] = deep_merge_config(result[key], value)
            else:
                # Base Case 1: Override the default value with the new value
                result[key] = value
        else:
            # Base Case 2: Key exists only in override, add it to the result
            result[key] = value

    return result

# --- Testing Exercise 3 ---
print("\n--- Testing Exercise 3 ---")
merged_config = deep_merge_config(DEFAULT_CONFIG, USER_CONFIG)

# Expected outcomes:
# 1. logging.level should be 'DEBUG' (overwritten)
# 2. logging.format should still exist (merged)
# 3. network.retries should be 5 (overwritten)
# 4. network.protocol should be 'HTTPS' (added)
# 5. database section should exist (new key added)

print("Merged Configuration:")
import json
# Using json.dumps for pretty printing the nested structure
print(json.dumps(merged_config, indent=4))

# Check specific merged values
print(f"\nLogging Level: {merged_config['logging']['level']}")
print(f"Network Retries: {merged_config['network']['retries']}")
print(f"Database Host: {merged_config.get('database', {}).get('host')}")

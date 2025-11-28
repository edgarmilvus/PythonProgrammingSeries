
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

import json

# 1. Define the Python dictionary (contains a list and a boolean)
app_config = {
    "version": 2.1,
    "debug_mode": True,
    "features": ["logging", "caching"],
    "max_retries": 5
}

print("--- Exercise 1 Solution ---")
print(f"Original object type: {type(app_config)}")

# 2. Serialize the dictionary into a JSON formatted string
# Using indent=2 for human readability in the print output
json_string = json.dumps(app_config, indent=2)

# 3. Print types to confirm serialization
print(f"Serialized string type: {type(json_string)}")
print("\nSerialized JSON Output:")
print(json_string)

# 4. Deserialize the JSON string back into a Python dictionary
loaded_config = json.loads(json_string)

# 5. Verify the loaded object type and content
print(f"\nLoaded object type: {type(loaded_config)}")
# Note how JSON 'true' is mapped back to Python True
print(f"Verified version number: {loaded_config['version']}")
print(f"Is debug mode enabled? {loaded_config['debug_mode']}")

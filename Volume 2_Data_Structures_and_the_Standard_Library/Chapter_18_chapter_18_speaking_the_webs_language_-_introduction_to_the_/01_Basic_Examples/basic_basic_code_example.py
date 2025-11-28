
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

import json

# 1. Define a Python dictionary (the source data)
# This dictionary maps Python data types to common data types.
python_data = {
    "user_id": 1001,
    "username": "Phoenix_Rising",
    "is_premium": True,
    "last_login": None,  # Python's None maps directly to JSON's null
    "stats": [
        {"hp": 150, "mana": 75},
        {"level": 50, "xp": 12500}
    ]
}

print("--- 1. Original Python Object (Dictionary) ---")
print(f"Type: {type(python_data)}")
print(python_data)
print("-" * 50)

# 2. Convert Python data to a JSON string (Serialization/Encoding)
# The 'dumps' (dump string) function performs the conversion.
# We use 'indent=4' to make the resulting JSON string human-readable.
json_string = json.dumps(python_data, indent=4)

print("--- 2. Serialized JSON String (Text Format) ---")
print(f"Type: {type(json_string)}")
# Note how the output now uses double quotes for keys/strings, and 'null' for None.
print(json_string)
print("-" * 50)

# 3. Convert the JSON string back to a Python object (Deserialization/Decoding)
# The 'loads' (load string) function performs the reverse conversion.
# This simulates receiving data back from a server.
python_reloaded = json.loads(json_string)

print("--- 3. Deserialized Python Object (Usable Data) ---")
print(f"Type: {type(python_reloaded)}")
print(python_reloaded)

# 4. Verification Check
print("\nVerification: Is the original object identical to the reloaded object?")
# We compare the two dictionaries directly.
print(python_data == python_reloaded)

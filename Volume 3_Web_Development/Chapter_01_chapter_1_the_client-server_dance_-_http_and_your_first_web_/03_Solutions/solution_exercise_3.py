
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

def parse_headers(raw_headers_string):
    """
    Converts raw header string (lines separated by \r\n) into a dictionary.
    Header keys are normalized to lowercase.

    Args:
        raw_headers_string (str): Multi-line string containing headers.

    Returns:
        dict: Dictionary of parsed headers.
    """
    headers = {}
    lines = raw_headers_string.split('\r\n')
    
    for line in lines:
        if not line:
            continue
        try:
            # Split only on the first occurrence of ': '
            key, value = line.split(': ', 1)
            # Normalize key to lowercase and strip whitespace from value
            headers[key.lower()] = value.strip()
        except ValueError:
            # Skip malformed lines that don't contain a key: value structure
            continue
    return headers

def identify_client(headers_dict):
    """
    Inspects the 'user-agent' header to classify the client type.

    Args:
        headers_dict (dict): Lowercase dictionary of HTTP headers.

    Returns:
        str: Client classification ("Browser", "Command-Line Tool", or "Unknown").
    """
    user_agent = headers_dict.get('user-agent', '').lower()

    if "mozilla" in user_agent or "safari" in user_agent:
        return "Browser"
    elif "curl" in user_agent or "wget" in user_agent:
        return "Command-Line Tool"
    else:
        return "Unknown"

# --- Testing Examples ---
# raw_test_headers = (
#     "Host: localhost:8080\r\n"
#     "User-Agent: Mozilla/5.0 (Windows NT 10.0)\r\n"
#     "Content-Length: 100\r\n"
#     "Accept: */*"
# )
# parsed = parse_headers(raw_test_headers)
# print(parsed)
# print(f"Client Type 1: {identify_client(parsed)}") # Browser
# print(f"Client Type 2: {identify_client({'user-agent': 'curl/7.64.1'})}") # Command-Line Tool
# print(f"Client Type 3: {identify_client({'custom-header': 'value'})}") # Unknown


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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# Internal Routing Table Definition
ROUTER = {
    '/': {'GET': 200},
    '/api/users': {'GET': 200, 'POST': 201},
    '/admin': {'POST': 200}
}

def determine_response(method, path):
    """
    Simulates server routing logic and returns the appropriate HTTP status code.

    Args:
        method (str): HTTP method (e.g., 'GET', 'POST').
        path (str): Request target path (e.g., '/api/users').

    Returns:
        int: The corresponding HTTP status code.
    """
    # 1. Check if the path exists (404 Not Found)
    if path not in ROUTER:
        return 404

    # Get the allowed methods for this path
    allowed_methods = ROUTER[path]

    # 2. Check if the method is allowed for this path (405 Method Not Allowed)
    if method in allowed_methods:
        # 3. Success case (200 or 201)
        return allowed_methods[method]
    else:
        return 405

# --- Testing Examples ---
# print(f"/ (GET): {determine_response('GET', '/')}")          # Expected: 200
# print(f"/api/users (POST): {determine_response('POST', '/api/users')}") # Expected: 201
# print(f"/admin (GET): {determine_response('GET', '/admin')}")          # Expected: 405
# print(f"/unknown (GET): {determine_response('GET', '/unknown')}")      # Expected: 404

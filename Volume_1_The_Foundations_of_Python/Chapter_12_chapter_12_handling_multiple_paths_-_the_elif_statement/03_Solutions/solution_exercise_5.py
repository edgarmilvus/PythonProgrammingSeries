
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

def check_update_status(status_code):
    """
    Maps an integer status code to a human-readable software update explanation.
    """
    explanation = ""
    
    # Ensure input is treated as an integer
    try:
        status_code = int(status_code)
    except ValueError:
        print(f"Error: Input '{status_code}' is not a valid integer code.")
        return

    # 1. Check specific success/warning codes first
    if status_code == 0:
        explanation = "Success (Update applied successfully.)"
    
    elif status_code == 1:
        explanation = "Warning (Update applied, but minor configuration issues detected.)"
        
    # 2. Check informational ranges (100-199)
    elif status_code >= 100 and status_code <= 199:
        explanation = "Informational (Process is running or pending.)"
        
    # 3. Check client error ranges (200-299)
    elif status_code >= 200 and status_code <= 299:
        explanation = "Client Error (Issue caused by user input or permissions.)"
        
    # 4. Check server error ranges (400-499)
    elif status_code >= 400 and status_code <= 499:
        explanation = "Server Error (Issue caused by server or infrastructure failure.)"
        
    # 5. Catch-all for any other code
    else:
        explanation = "Unknown Status (Contact support.)"
        
    print(f"Status Code {status_code}: {explanation}")

# Example Usage:
print("\n--- Software Update Status Examples ---")
check_update_status(0)    # Success
check_update_status(1)    # Warning
check_update_status(150)  # Informational
check_update_status(203)  # Client Error
check_update_status(404)  # Server Error
check_update_status(999)  # Unknown Status

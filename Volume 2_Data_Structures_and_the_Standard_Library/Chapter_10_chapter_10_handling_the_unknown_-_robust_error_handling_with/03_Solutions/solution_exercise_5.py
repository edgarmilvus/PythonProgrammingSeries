
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

class DatabaseConnectionError(Exception):
    """Custom exception for high-level database connection failures."""
    pass

def attempt_network_connection(timeout_occurred=False):
    """
    Simulates a low-level networking attempt that might time out.
    If timeout_occurred is True, raises a built-in TimeoutError.
    """
    if timeout_occurred:
        # Simulate a built-in error from a standard library module
        raise TimeoutError("Network request timed out after 5 seconds.")

    print("Low-level connection successful.")
    return True

def connect_to_db(should_fail=True):
    """
    High-level function that wraps the network attempt and handles errors,
    using exception chaining to preserve context.
    """
    print("Attempting to connect to database...")
    try:
        # Call the low-level function
        attempt_network_connection(should_fail)
    except TimeoutError as e:
        # Catch the low-level error (e) and raise a high-level, domain-specific error.
        # 'from e' links the new exception to the original cause.
        raise DatabaseConnectionError("Failed to establish database connection due to network issues.") from e

    print("Database connection successfully established.")


# Demonstration Block (Required for testing the exception chain)
def run_connection_test():
    try:
        # Setting should_fail=True triggers the TimeoutError, which then triggers the chain.
        connect_to_db(should_fail=True)
    except DatabaseConnectionError as db_error:
        print("\n--- APPLICATION ERROR CAUGHT ---")
        print(f"Caught high-level error: {db_error}")
        print("\n--- DEBUGGING TRACEBACK (Observe the 'During handling of the above exception' text) ---")
        # Re-raising the exception here forces Python to print the full traceback
        # demonstrating the explicit exception chain.
        raise

# run_connection_test()


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

def process_config(filename, file_exists=True):
    """
    Simulates configuration file processing, demonstrating try/except/else/finally flow.
    """
    print(f"Attempting to process '{filename}'...")
    data = None

    try:
        if not file_exists:
            # Simulate a failure condition
            raise FileNotFoundError(f"Configuration file '{filename}' not found.")

        # Simulate successful reading
        data = {"setting_a": 10, "setting_b": "value"}
        print("SUCCESS: File read successfully.")

    except FileNotFoundError as e:
        # Handles the specific expected failure
        print(f"FAILURE: Cannot load configuration. {e}")

    except Exception as e:
        # Handles unexpected errors during the try block
        print(f"FAILURE: An unexpected error occurred during reading: {e}")

    else:
        # This block runs ONLY if the 'try' block completed without raising an exception.
        print("ELSE BLOCK: Starting data validation and processing.")
        # Perform simulated validation
        if data and isinstance(data.get("setting_a"), int):
            print("ELSE BLOCK: Configuration data is valid.")
        else:
            print("ELSE BLOCK: Configuration data failed secondary validation.")

    finally:
        # This block ALWAYS runs, regardless of success or failure (cleanup/logging).
        print("--- Resource cleanup and logging complete. ---")

# Test cases
# print("\n--- Test Case 1: Success ---")
# process_config("app_settings.json", file_exists=True)
# print("\n--- Test Case 2: Failure ---")
# process_config("app_settings.json", file_exists=False)

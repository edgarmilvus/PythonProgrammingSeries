
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

user_records = [
    ["Alice", 95],
    ["Bob", 88],
    ["Charlie"],  # IndexError: Missing score
    ["David", 72],
    ["Eve", "N/A"],  # ValueError: Non-numeric score
    ["Frank", 65],
]

def process_data_resiliently(records):
    """
    Processes a list of records, skipping and logging errors without crashing.
    """
    total_score = 0
    successful_records = 0
    failed_records = 0

    print("--- Starting Resilient Data Processing ---")

    for i, record in enumerate(records):
        print(f"Processing Record {i+1}: {record}")

        try:
            # 1. Accessing index 1 can raise IndexError
            username = record[0]
            score_raw = record[1]

            # 2. Converting to int can raise ValueError
            score = int(score_raw)

        except IndexError as e:
            # Handle structural error (missing expected elements)
            failed_records += 1
            print(f"  [ERROR] Record {i+1} failed (IndexError): Structure malformed (expected at least 2 elements). Details: {e}")
            continue # Skip to the next record

        except ValueError as e:
            # Handle data type error (non-numeric score)
            failed_records += 1
            print(f"  [ERROR] Record {i+1} failed (ValueError): Score '{score_raw}' is not a valid integer. Details: {e}")
            continue # Skip to the next record

        except Exception as e:
            # Catch any other unforeseen error
            failed_records += 1
            print(f"  [CRITICAL ERROR] Record {i+1} failed due to unexpected issue: {type(e).__name__}: {e}")
            continue

        else:
            # Success path (runs only if try block completes without exception)
            total_score += score
            successful_records += 1
            print(f"  [SUCCESS] {username} processed with score {score}.")

    # Final Summary Report
    print("\n--- Processing Summary ---")
    print(f"Total Records Attempted: {len(records)}")
    print(f"Successful Records: {successful_records}")
    print(f"Failed Records: {failed_records}")

    if successful_records > 0:
        average_score = total_score / successful_records
        print(f"Total Score: {total_score}")
        print(f"Average Score (of successful records): {average_score:.2f}")

# process_data_resiliently(user_records)

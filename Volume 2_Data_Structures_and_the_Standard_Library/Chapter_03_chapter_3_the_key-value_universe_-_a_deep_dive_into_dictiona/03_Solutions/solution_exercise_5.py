
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

# --- Exercise 4 Solution ---

# 1. Define the key mapping dictionary
KEY_MAPPING = {
    "user_id": "id",
    "name_first": "firstName",
    "name_last": "lastName"
}

def transform_user_data(data_list):
    """
    Transforms and filters user data using combined list and dictionary structures.
    Filters for active users ('A'), renames keys, and translates status to boolean.
    """
    
    # Outer List Comprehension: Filters and iterates over the source list
    transformed_data = [
        {
            # Inner Dictionary: Explicitly defines the required output structure
            # and applies the transformation logic in a single step.
            "id": user_dict["user_id"],
            "firstName": user_dict["name_first"],
            "lastName": user_dict["name_last"],
            # Status Interpretation: 'A' -> True, anything else -> False
            "is_active": user_dict["status_code"] == 'A'
        }
        for user_dict in data_list
        # Filtering Condition: Only include users where status_code is 'A'
        if user_dict["status_code"] == 'A'
    ]
    
    return transformed_data

# --- Testing Exercise 4 ---
print("\n--- Testing Exercise 4 ---")
final_pipeline_data = transform_user_data(API_USERS_DATA)

print(f"Total users processed (should be 2): {len(final_pipeline_data)}")
print("Transformed and Filtered Data:")
import pprint
pprint.pprint(final_pipeline_data)

# Verification check: The output should only contain Alice and Charlie, with camelCase keys and is_active=True.

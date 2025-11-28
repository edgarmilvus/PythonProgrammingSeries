
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

# Exercise 4: Interactive Challenge Implementation

def process_configuration(job_name, run_date, max_retries=3, email_on_failure=False):
    """
    Configures a batch processing job, utilizing default values for optional settings.

    Args:
        job_name (str): The unique name of the job (required).
        run_date (str): The date the job is scheduled to run (required).
        max_retries (int, optional): Maximum number of times to attempt the job. Defaults to 3.
        email_on_failure (bool, optional): Whether to send an email if the job fails. Defaults to False.
    """
    
    # Indentation is critical here to define the function block.
    print("-" * 30)
    print(f"Job Configuration for: {job_name}")
    print(f"Scheduled Date: {run_date}")
    print(f"Max Retries Allowed: {max_retries}")
    print(f"Email Notification: {email_on_failure}")
    print("-" * 30)


# 3. Standard Execution (Using all defaults)
print("--- 3. Standard Execution (Positional only) ---")
# Only job_name and run_date are provided positionally.
process_configuration("Data_Cleanup_A", "2024-06-15")

# 4. Override Retries (Positional required, Keyword optional)
print("\n--- 4. Override Retries (Mixing Positional and Keyword) ---")
# The first two are positional, the third is a keyword override.
process_configuration("Archive_Backup_B", "2024-06-16", max_retries=5)

# 5. Full Customization (Demonstrating keyword order flexibility)
print("\n--- 5. Full Customization (Mixed Keyword Order) ---")
# Positional arguments come first, followed by keywords in any order.
process_configuration(
    "Critical_Update_C", 
    "2024-06-17", 
    email_on_failure=True, 
    max_retries=1
)

# Example of a common error (If uncommented, this would throw a SyntaxError)
# print("\n--- ERROR EXAMPLE: Positional after Keyword ---")
# process_configuration(job_name="Invalid_Call", "2024-06-18", max_retries=3) 
# The error occurs because "2024-06-18" is a positional argument following the keyword argument job_name.

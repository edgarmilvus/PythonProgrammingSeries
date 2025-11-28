
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

# =================================================================
# 1. GLOBAL SCOPE DEFINITION
# These variables are defined at the module level and are accessible
# anywhere in this file, including inside functions.
# =================================================================
company_name = "TechCorp Solutions"
version_number = 1.0
request_counter = 0 # A simple global counter

def process_data_request(request_id):
    # =============================================================
    # 2. LOCAL SCOPE DEFINITION
    # This variable is created when the function is called and
    # destroyed when the function finishes execution.
    # =============================================================
    department_name = "Data Analytics"
    
    # 3. Reading Global Variables (Allowed by Default)
    # Python searches outward: Local -> Enclosing -> Global -> Built-in
    print(f"--- Processing Request {request_id} ---")
    print(f"Company: {company_name}")
    print(f"System Version: {version_number}")
    
    # 4. Accessing Local Variable
    print(f"Handled by Department: {department_name}")
    
    # We can also modify a global variable, but ONLY if we
    # explicitly declare it using the 'global' keyword (covered later).
    # If we tried to modify request_counter here without 'global',
    # Python would create a *new* local variable named request_counter.
    
    return f"Request {request_id} completed successfully."

# 5. Execution in the Global Scope
print(f"Initial global counter state: {request_counter}")
result_1 = process_data_request(4001)
print(f"\nFunction Result: {result_1}")

# 6. Global Scope Verification
print("\n--- Global Scope Verification ---")
print(f"The Global Company Name is still: {company_name}")

# 7. Attempting to access the Local variable from the Global Scope
# This attempt will fail, but we skip the actual error to allow the
# program to finish demonstrating the concept.
print("Attempting to read local variable 'department_name' from global scope...")
try:
    # If this line was uncommented, a NameError would occur:
    # print(department_name)
    print("... Access denied (variable does not exist here).")
except NameError as e:
    print(f"Error encountered: {e}")

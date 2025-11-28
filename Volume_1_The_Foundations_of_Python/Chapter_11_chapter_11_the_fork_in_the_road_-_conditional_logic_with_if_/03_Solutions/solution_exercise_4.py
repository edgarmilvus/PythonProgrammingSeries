
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

# Start your solution here
SYSTEM_MODE = "MAINTENANCE" # Test value 1: MAINTENANCE
# SYSTEM_MODE = "UNKNOWN_MODE" # Test value 2: UNKNOWN_MODE

def run_production():
    print("--- MODE: PRODUCTION ---")
    print("Initializing secure database connection and logging.")

def run_testing():
    print("--- MODE: TESTING ---")
    print("Loading mock data and skipping external API calls.")

def run_development():
    print("--- MODE: DEVELOPMENT ---")
    print("Enabling hot reloading and verbose debugging logs.")

# Requirement 1: New function definition
def enter_maintenance():
    print("--- MODE: MAINTENANCE ---")
    print("CRITICAL WARNING: System is currently down for scheduled maintenance.")
    print("All operational processes are halted.")

# Dispatcher Logic (Requirement 3 & 4 modifications)
if SYSTEM_MODE == "PRODUCTION":
    run_production()
elif SYSTEM_MODE == "TESTING":
    run_testing()
elif SYSTEM_MODE == "DEVELOPMENT":
    run_development()
# Requirement 3: Handle the new maintenance mode
elif SYSTEM_MODE == "MAINTENANCE":
    enter_maintenance()
# Requirement 4: Refined error handling for unknown modes (Halt execution)
else:
    print("-" * 40)
    print(f"CRITICAL SYSTEM FAILURE: Invalid configuration mode detected: '{SYSTEM_MODE}'.")
    # The key change: We do NOT call run_development() here.
    print("System execution halted to prevent data corruption.")
    print("-" * 40)

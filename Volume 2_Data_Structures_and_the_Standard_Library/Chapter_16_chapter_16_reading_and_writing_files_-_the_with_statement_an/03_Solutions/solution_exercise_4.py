
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

import sys
import os 
from datetime import datetime # Used for simulating user input timestamp

CONFIG_FILE = ".processor_config"

def save_config(file_path):
    """Saves the last successfully used file path."""
    print(f"[CONFIG] Saving '{file_path}' to {CONFIG_FILE}...")
    try:
        # Use 'w' mode to overwrite the previous setting
        with open(CONFIG_FILE, 'w') as f:
            # Ensure a newline is written for clean reading later
            f.write(file_path + '\n')
    except IOError:
        print("[ERROR] Could not write configuration file.")

def load_config():
    """Loads the last used file path from the configuration file."""
    try:
        # Use 'r' mode to safely read the configuration
        with open(CONFIG_FILE, 'r') as f:
            # Read the path and strip any surrounding whitespace/newlines
            path = f.read().strip()
            if path:
                print(f"[CONFIG] Loaded path: {path}")
                return path
            return None
    except FileNotFoundError:
        # Handle the case where the config file doesn't exist yet
        print(f"[CONFIG] Configuration file ({CONFIG_FILE}) not found. Starting fresh.")
        return None
    except IOError:
        print("[ERROR] Could not read configuration file due to I/O error.")
        return None

def run_data_processor(input_path):
    """Simulates the main data processing logic."""
    if input_path:
        print(f"\n[PROCESSOR] Successfully initializing analysis using file: {input_path}")
        
        # After successful processing, save the path for next time (Priority 1 & 3)
        save_config(input_path)
    else:
        print("\n[PROCESSOR] No input path provided. Exiting.")


# --- Main Execution Simulation ---

# Initialize the path variable
input_file_path = None

# A. Check Priority 1: Command-line arguments (sys.argv)
if len(sys.argv) > 1:
    # Use the path provided as the first argument (sys.argv[1])
    input_file_path = sys.argv[1]
    print(f"Source: Command Line Argument ('{input_file_path}')")

# B. Check Priority 2: Configuration file (if no command-line argument was given)
elif not input_file_path:
    print("Source: Checking Configuration File...")
    input_file_path = load_config()
    
    # C. Check Priority 3: Manual user input (if config load failed)
    if not input_file_path:
        print("Source: Configuration not found or empty.")
        
        # Simulating user input for the exercise
        # Note: In a real script, this would block execution until input is received.
        print("--- Manual Input Required ---")
        manual_input = input(f"Please enter the path manually (e.g., 'data_{datetime.now().strftime('%H%M%S')}.csv'): ")
        
        if manual_input:
            input_file_path = manual_input.strip()
            
# 2. Run the main application logic
run_data_processor(input_file_path)

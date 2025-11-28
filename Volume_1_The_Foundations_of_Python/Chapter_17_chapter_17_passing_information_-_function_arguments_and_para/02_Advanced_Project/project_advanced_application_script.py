
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import os
import datetime

# --- Helper Functions ---

def get_timestamp():
    """
    Retrieves a formatted timestamp for logging purposes.
    Returns: A string representing the current date and time.
    """
    # Using datetime.now() to ensure the log entry is timely
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def log_activity(message, level="INFO"):
    """
    Logs an activity message to the console.
    This function demonstrates a simple, reusable logging wrapper.
    """
    # Positional arguments (message) define the core content.
    # Keyword argument with default (level) allows customization.
    timestamp = get_timestamp()
    print(f"{timestamp} [{level.upper()}]: {message}")


# --- Core Application Logic ---

def process_file_operation(source_file_name, target_directory, prefix="ARCHIVED_", log_action=True, dry_run=False):
    """
    Simulates renaming and archiving a file based on provided parameters.

    Parameters:
    source_file_name (str): The name of the file to be processed (Positional, Required).
    target_directory (str): The destination path for the archived file (Positional, Required).
    prefix (str): The prefix to prepend to the new file name (Keyword, Defaulted).
    log_action (bool): Whether to record the operation in the log (Keyword, Defaulted=True).
    dry_run (bool): If True, only reports the action without executing it (Keyword, Defaulted=False).
    """

    # 1. Input Validation and Path Construction
    if not source_file_name or not target_directory:
        if log_action:
            log_activity("Error: Source file or target directory cannot be empty.", level="ERROR")
        return False

    # Standardize the file name using the provided prefix
    new_file_name = f"{prefix}{source_file_name}"

    # Use os.path.join for robust, OS-independent path construction (RAG concept)
    full_target_path = os.path.join(target_directory, new_file_name)

    # 2. Status Reporting based on 'dry_run' argument
    if dry_run:
        status_message = f"DRY RUN: Would move '{source_file_name}' to '{full_target_path}'."
        if log_action:
            log_activity(status_message, level="PREVIEW")
        return True

    # 3. Execution Phase (Simulated)
    try:
        # Simulate the actual file operation (e.g., os.rename or shutil.move)
        # In a real application, we would check if target_directory exists first.
        
        # Simulate successful operation
        if log_action:
            log_activity(f"Processing '{source_file_name}'. Target: {full_target_path}")

        # Placeholder for actual file system modification
        # print(f"Executing move: '{source_file_name}' -> '{full_target_path}'")
        
        if log_action:
            log_activity(f"Success: File archived as '{new_file_name}'.")
        return True

    except Exception as e:
        # Simulate handling a file system error
        if log_action:
            log_activity(f"Operation failed for '{source_file_name}'. Error: {e}", level="CRITICAL")
        return False


# --- Demonstration of Argument Flexibility ---

if __name__ == "__main__":
    
    # Define constants for clarity
    SOURCE_FILE_1 = "report_Q3_2024.pdf"
    SOURCE_FILE_2 = "temp_data_export.csv"
    ARCHIVE_PATH_A = "/data/archives/reports"
    ARCHIVE_PATH_B = "/data/archives/temp"

    print("--- Scenario 1: Minimal Positional Call (Using all Defaults) ---")
    # Only positional arguments are provided. prefix="ARCHIVED_", log_action=True, dry_run=False are used.
    process_file_operation(SOURCE_FILE_1, ARCHIVE_PATH_A)

    print("\n--- Scenario 2: Positional and Selective Keyword Call (Custom Prefix) ---")
    # Positional arguments define location. Keyword argument overrides the default prefix.
    process_file_operation(SOURCE_FILE_2, ARCHIVE_PATH_B, prefix="TEMP_CLEANED_")

    print("\n--- Scenario 3: Full Keyword Call (Order Independent, Disabling Logging) ---")
    # All arguments specified using keywords. Order doesn't matter (PEP 8 encourages this for clarity).
    # Note: log_action is explicitly set to False.
    process_file_operation(
        target_directory=ARCHIVE_PATH_A,
        source_file_name=SOURCE_FILE_2,
        log_action=False,
        prefix="SILENT_ARCHIVE_"
    )
    # Since log_action=False, only the print statements inside __main__ will appear.

    print("\n--- Scenario 4: Dry Run Mode (Checking the action without execution) ---")
    # Using a mix of positional arguments and the 'dry_run' flag via keyword.
    process_file_operation(SOURCE_FILE_1, ARCHIVE_PATH_B, dry_run=True, prefix="PREVIEW_")

    print("\n--- Scenario 5: Overriding Logging in Dry Run ---")
    # Dry run activated, but logging suppressed.
    process_file_operation(SOURCE_FILE_2, ARCHIVE_PATH_A, dry_run=True, log_action=False)
    print("Action attempted silently (log_action=False).")

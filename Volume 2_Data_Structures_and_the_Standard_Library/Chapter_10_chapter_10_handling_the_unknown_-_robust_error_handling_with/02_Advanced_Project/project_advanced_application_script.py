
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
from typing import Dict, Any

# --- 1. Custom Exception Definition ---
class ConfigurationError(Exception):
    """Custom exception raised for issues specific to configuration validation 
    or critical file access failures."""
    pass

# --- 2. Configuration Processing Function ---
def load_and_validate_config(filepath: str) -> Dict[str, Any]:
    """
    Reads, parses, and validates application configuration settings from a file.
    Uses nested try/except blocks to differentiate between I/O errors and data errors.
    """
    config_data = {}
    file_handle = None # Initialize handle for safe access in 'finally' block

    # Outer TRY block: Handles file opening and reading (I/O errors)
    try:
        print(f"--- Attempting to read configuration from: {filepath} ---")
        # Attempt to open the file (Potential FileNotFoundError)
        file_handle = open(filepath, 'r')
        
        for line_number, line in enumerate(file_handle, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Inner TRY block: Handles parsing of individual lines
            try:
                # Expecting format: key=value
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                config_data[key] = value

            except ValueError:
                # Specific handling for lines that don't contain exactly one '='
                print(f"[Warning] Skipping malformed line {line_number}: '{line}'")
                continue
        
    except FileNotFoundError:
        # Catch critical I/O error
        print(f"\n[CRITICAL ERROR] Configuration file not found at '{filepath}'.")
        # Raise our custom, specific exception for the main program to catch
        raise ConfigurationError(f"Required configuration file missing: {filepath}")

    except Exception as e:
        # Catch any other unexpected I/O or system errors (PermissionError, etc.)
        print(f"\n[UNEXPECTED I/O ERROR] An unknown error occurred during read: {e}")
        raise ConfigurationError(f"I/O failure during read operation: {type(e).__name__}")
        
    # ELSE block: Executes ONLY if the outer TRY block completes without exception
    else:
        print("\n[SUCCESS] File read completed successfully. Starting validation...")
        
        # TRY block 3: Handles data type conversion and logic validation
        try:
            # 1. Check for mandatory keys
            if 'buffer_size' not in config_data or 'max_file_mb' not in config_data:
                 raise ConfigurationError("Missing mandatory keys: buffer_size or max_file_mb.")

            # 2. Convert string values to Integer (Potential ValueError)
            buffer_size = int(config_data['buffer_size'])
            max_file_mb = int(config_data['max_file_mb'])
            
            # 3. Logic validation (e.g., preventing division by zero or negative values)
            if buffer_size <= 0:
                # Custom validation failure using 'raise'
                raise ConfigurationError("Buffer size must be a positive integer (> 0).")

            # Example calculation: Determine max log entries based on file size and buffer size
            # 1 MB = 1048576 Bytes
            max_entries = (max_file_mb * 1048576) // buffer_size 
            
            # Update config_data with validated and calculated values
            config_data['buffer_size'] = buffer_size
            config_data['max_file_mb'] = max_file_mb
            config_data['max_entries'] = max_entries
            
            print(f"[VALIDATION OK] Calculated max entries: {max_entries:,}")
            return config_data

        except ValueError as ve:
            # Handle cases where int() conversion failed (e.g., 'buffer_size=ten')
            raise ConfigurationError(f"Data type error in config: Numeric value required. Details: {ve}")
        
        except ConfigurationError as ce:
            # Re-raise the custom error defined internally (e.g., missing keys or logic failure)
            raise ce

    # FINALLY block: Executes regardless of whether an exception occurred or not
    finally:
        if file_handle:
            file_handle.close()
            print(f"[CLEANUP] Closed file handle for {filepath}.")

# --- 3. Main Execution Block ---

CONFIG_FILE = "app_settings.cfg"

# Setup test file with a mix of good and bad data
try:
    with open(CONFIG_FILE, 'w') as f:
        f.write("# Application Configuration Settings\n")
        f.write("log_level=INFO\n")
        f.write("buffer_size=512\n")
        f.write("malformed_line_test\n") # This line will trigger an inner ValueError
        f.write("max_file_mb=10\n")
        f.write("timeout=30\n")
    
    # Attempt to load the configuration
    final_config = load_and_validate_config(CONFIG_FILE)
    
    print("\n--- APPLICATION START SUCCESS ---")
    print("Configuration Summary:")
    for k, v in final_config.items():
        print(f"  {k}: {v} ({type(v).__name__})")

except ConfigurationError as e:
    # Top-level catch for all expected configuration failures
    print("\n--- PROCESS FAILED ---")
    print(f"The application could not start due to configuration issues.")
    print(f"Reason: {e}")

except Exception as e:
    # Last resort catch for truly unexpected Python runtime errors
    print(f"\n[FATAL SYSTEM FAILURE] An unexpected error stopped execution: {type(e).__name__}: {e}")

finally:
    # Clean up the test file created earlier
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(f"\n[SYSTEM CLEANUP] Removed temporary file: {CONFIG_FILE}")


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

import os
import sys

# --- 1. Define fallbacks and constants ---
# This is an insecure default key, used only if the environment variable is missing.
# We use a long string to simulate a real key, though it should never be hardcoded.
DEFAULT_SECRET = "insecure_dev_fallback_key_1234567890_do_not_use_in_prod"

def load_config():
    """
    Loads configuration settings into a dictionary, prioritizing environment variables
    set by the Operating System.
    """
    config = {}

    # 2a. Determine the Environment Type
    # os.environ.get() safely retrieves the value or uses the default ('development').
    env_type = os.environ.get('ENVIRONMENT', 'development').lower()
    config['ENVIRONMENT'] = env_type

    # 2b. Set Debug Status based on Environment
    # We explicitly force DEBUG=False in production for security reasons.
    if env_type == 'production':
        config['DEBUG'] = False
    else:
        # In development, we check if the user explicitly set DEBUG.
        # Environment variables are always strings, so we check for 'true' or '1'.
        debug_setting = os.environ.get('DEBUG', 'True').lower()
        config['DEBUG'] = (debug_setting == 'true' or debug_setting == '1')

    # 2c. Load Sensitive Data (The Secret Key)
    # This must always come from the environment if possible.
    secret_key = os.environ.get('SECRET_KEY')

    if secret_key:
        config['SECRET_KEY'] = secret_key
        # In a real app, we would log this, but here we print confirmation.
        print(f"[INFO] Configuration: SECRET_KEY loaded securely from OS environment.")
    else:
        # Warning: Using a hardcoded default is a major security flaw in production.
        config['SECRET_KEY'] = DEFAULT_SECRET
        print(f"[WARNING] Configuration: Using default SECRET_KEY. This is INSECURE.")

    return config

# --- 3. Simulation of application startup ---
print("--- Application Startup Sequence ---")
app_config = load_config()

# --- 4. Reporting the results ---
print("\n--- Current Configuration Settings ---")
print(f"Environment Type: {app_config['ENVIRONMENT'].upper()}")
print(f"Debug Mode Status: {app_config['DEBUG']}")
print(f"Secret Key Security Check: Key length is {len(app_config['SECRET_KEY'])} characters.")

# --- 5. Conditional Logic Demonstration ---
if app_config['DEBUG']:
    print("\n[BEHAVIOR] Detailed error tracebacks are ACTIVE.")
else:
    print("\n[BEHAVIOR] Detailed error tracebacks are INACTIVE. User sees generic error page.")

# --- 6. Instructions for Testing ---
print("\n--- Testing Instructions ---")
print("To test the production environment, run this script after setting environment variables:")
print("Example (Linux/macOS):")
print("$ export ENVIRONMENT=production")
print("$ python config_loader.py")
print("Example (Windows CMD):")
print("$ set ENVIRONMENT=production")
print("$ python config_loader.py")

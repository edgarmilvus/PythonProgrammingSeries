
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

import os
from dotenv import load_dotenv
import re
from typing import Dict, Type

# --- Exercise 1: The Config Gateway – Environment Variable Fallbacks ---

def load_server_settings():
    """
    Loads server settings with type conversion and fallbacks.
    Prioritizes environment variables over documented defaults.
    """
    
    # 1. Retrieve and convert SERVER_PORT (Default: 5000)
    # Fallback to '5000' string, then attempt conversion to int
    port_str = os.environ.get('SERVER_PORT', '5000')
    try:
        port = int(port_str)
    except ValueError:
        # Safety fallback if the environment variable is set but invalid
        print(f"Warning: SERVER_PORT '{port_str}' is not a valid integer. Using default 5000.")
        port = 5000
        
    # 2. Retrieve and convert DEBUG_MODE (Default: False)
    # Fallback to 'False' string. Must explicitly check the string value.
    debug_str = os.environ.get('DEBUG_MODE', 'False').lower()
    # If the string is 'true' or '1', it is True; otherwise, it is False.
    debug_mode = (debug_str == 'true' or debug_str == '1')
    
    print("\n--- Exercise 1 Results (Environment Fallbacks) ---")
    print(f"Port: {port} (Type: {type(port).__name__})")
    print(f"Debug Mode: {debug_mode} (Type: {type(debug_mode).__name__})")


# --- Exercise 2: Implementing the Configuration Matrix ---

class Config:
    """Base configuration class holding common settings."""
    SECRET_KEY = "super-secret-default"
    TESTING = False
    DEBUG = False # Default safe setting

class DevelopmentConfig(Config):
    """Configuration specific for local development."""
    DEBUG = True
    DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(Config):
    """Configuration specific for secure, production deployment."""
    DEBUG = False
    # Secure, external connection string (simulated)
    DATABASE_URI = "postgresql://user:pass_prod_123@db.example.com/prod_db"
    
# Map environment names to configuration classes
CONFIG_MAP: Dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': Config,
    'default': DevelopmentConfig # Safe fallback for unknown environments
}

def load_config(env_name: str = None) -> Config:
    """Loads the appropriate configuration class based on environment name."""
    # Read APP_ENV from os.environ, defaulting to 'development' if not provided
    env = (env_name or os.environ.get('APP_ENV', 'development')).lower()
    
    # Retrieve the configuration class, falling back to 'default' if the name is unknown
    config_class = CONFIG_MAP.get(env, CONFIG_MAP['default'])
    return config_class()

def run_exercise_2():
    print("\n--- Exercise 2 Results (Config Matrix) ---")
    
    # Scenario 1: Development
    dev_config = load_config('development')
    print(f"DEV Config: DEBUG={dev_config.DEBUG}, DB={dev_config.DATABASE_URI}")
    
    # Scenario 2: Production
    prod_config = load_config('production')
    print(f"PROD Config: DEBUG={prod_config.DEBUG}, DB={prod_config.DATABASE_URI}")


# --- Exercise 3: Interactive Challenge – Secure Dotenv Integration ---

# Re-defining simplified classes for E3 context
class ConfigE3:
    TEST_VAR = "DefaultValue"
    
class DevelopmentConfigE3(ConfigE3):
    pass

def create_app(config_name='development'):
    """Application Factory function with conditional dotenv loading."""
    
    # 1. Determine environment and conditionally load .env
    env = config_name.lower()
    
    if env == 'development':
        # Only load .env file if running in development mode
        success = load_dotenv()
        if success:
            print("INFO: Successfully loaded .env file for development environment.")
        else:
            print("WARNING: Running in development mode but .env file not found.")
    else:
        # In production/staging, secrets must come from the host environment
        print(f"INFO: Running in {env} mode. Skipping .env file loading for security.")
    
    # 2. Map config_name to the appropriate class (Simplified)
    if env == 'development':
        app_config = DevelopmentConfigE3()
    else:
        app_config = ConfigE3() # Fallback for production/other
        
    # 3. Apply configuration (Simulated)
    # os.environ.get() retrieves the value loaded by dotenv, or the OS environment value
    test_var_value = os.environ.get('TEST_VAR', app_config.TEST_VAR)
    
    print(f"--- Application Configuration Loaded ---")
    print(f"Environment: {env}")
    print(f"TEST_VAR: {test_var_value}")
    print("----------------------------------------")
    
    return app_config


# --- Exercise 4: Security Focus – Masking Sensitive Credentials ---

def mask_secret(uri: str) -> str:
    """
    Masks the password portion of a database URI (scheme://user:password@host/db).
    Returns the original URI if no password/host format is detected.
    """
    
    # Check if the URI contains credentials (indicated by both ':' and '@')
    if '@' not in uri or ':' not in uri.split('//')[-1]:
        return uri # Return unchanged if it doesn't look like a cred-containing URI
    
    try:
        # 1. Split into the credential part and the host/db part
        scheme_user_pass, rest = uri.split('@', 1)
        
        # 2. Extract the user:pass part (removing the scheme:// prefix)
        user_pass_part = scheme_user_pass.split('//', 1)[-1]
        
        # 3. Use rsplit to separate the username part from the password part by the last colon
        # Example: "admin:my_secret_password_123" -> ("admin", "my_secret_password_123")
        user_part, _ = user_pass_part.rsplit(':', 1)
        
        # 4. Reconstruct the URI with the masked password
        masked_password = '***'
        
        # Get the scheme part (e.g., 'mysql:')
        scheme_part = uri.split('//', 1)[0]
        
        # Rebuild: scheme://user:***@rest
        masked_uri = scheme_part + '//' + user_part + ':' + masked_password + '@' + rest
        
        return masked_uri
        
    except ValueError:
        # Catch unexpected formats during splitting
        return uri

def run_exercise_4():
    print("\n--- Exercise 4 Results (Credential Masking) ---")
    
    DB_URI_SECURE = "mysql://admin:my_secret_password_123@db.example.com:3306/app_db"
    DB_URI_INSECURE = "sqlite:///local.db"
    
    masked_secure = mask_secret(DB_URI_SECURE)
    masked_insecure = mask_secret(DB_URI_INSECURE)
    
    print(f"Original Secure URI:   {DB_URI_SECURE}")
    print(f"Masked Secure URI:     {masked_secure}")
    print("-" * 20)
    print(f"Original Insecure URI: {DB_URI_INSECURE}")
    print(f"Masked Insecure URI:   {masked_insecure}")


# --- Execution Block ---

if __name__ == '__main__':
    
    # --- Setup for Exercise 1 ---
    # Ensure variables are clear for initial test (using defaults)
    if 'SERVER_PORT' in os.environ: del os.environ['SERVER_PORT']
    if 'DEBUG_MODE' in os.environ: del os.environ['DEBUG_MODE']
    
    # Scenario 1.1: Using defaults
    load_server_settings() 
    
    # Scenario 1.2: Using environment overrides
    os.environ['SERVER_PORT'] = '8080'
    os.environ['DEBUG_MODE'] = 'True'
    load_server_settings()
    
    # --- Run Exercise 2 ---
    run_exercise_2()
    
    # --- Run Exercise 4 ---
    run_exercise_4()
    
    # --- Run Exercise 3 (Interactive Challenge) ---
    # NOTE: This requires a local file named .env containing TEST_VAR=LoadedFromDotEnv
    
    # Scenario A: Development (Should load .env)
    # Ensure APP_ENV is set for the factory
    os.environ['APP_ENV'] = 'development'
    print("\n--- Exercise 3: Running in Development Mode (Expect DotEnv Load) ---")
    create_app(os.environ['APP_ENV'])
    
    # Scenario B: Production (Should NOT load .env, should use default)
    os.environ['APP_ENV'] = 'production'
    # Crucially, clear the variable loaded by dotenv in the previous step
    if 'TEST_VAR' in os.environ:
        del os.environ['TEST_VAR']
        
    print("\n--- Exercise 3: Running in Production Mode (Expect Default Value) ---")
    create_app(os.environ['APP_ENV'])

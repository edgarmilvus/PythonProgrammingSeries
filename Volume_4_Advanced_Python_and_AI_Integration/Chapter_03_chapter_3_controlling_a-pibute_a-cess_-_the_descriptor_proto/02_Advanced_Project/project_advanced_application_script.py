
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

import time
from typing import Any, Type

# --- 1. Base Descriptor Class for Shared Logic ---

class ConfigDescriptor:
    """
    Base class providing __set_name__ implementation for storing the attribute
    name and handling the internal storage key.
    """
    def __init__(self, default: Any = None):
        # The attribute name on the instance's __dict__ where the value is stored.
        self.storage_name = None
        self.default = default

    def __set_name__(self, owner: Type, name: str):
        """Called by the owner class when the descriptor is defined."""
        # Use a mangled name to prevent accidental attribute collision
        self.storage_name = f'_{name}'

# --- 2. Data Descriptor: Strict Type Enforcement ---

class TypedAttribute(ConfigDescriptor):
    """Data descriptor enforcing a specific data type upon assignment."""
    def __init__(self, expected_type: Type, **kwargs):
        super().__init__(**kwargs)
        self.expected_type = expected_type

    def __get__(self, instance: Any, owner: Type):
        """Retrieves the value from the instance's dictionary."""
        if instance is None:
            return self # Access via class returns the descriptor itself
        
        # Use dict.get() for safe retrieval, falling back to the default if provided
        return instance.__dict__.get(self.storage_name, self.default)

    def __set__(self, instance: Any, value: Any):
        """Validates the type and stores the value."""
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Attribute must be of type {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        instance.__dict__[self.storage_name] = value

# --- 3. Data Descriptor: Range Validation (Inherits Type Enforcement) ---

class PositiveInt(TypedAttribute):
    """Data descriptor enforcing integer type and a positive range."""
    def __init__(self, min_val: int = 1, max_val: int = None):
        super().__init__(int)
        self.min_val = min_val
        self.max_val = max_val

    def __set__(self, instance: Any, value: int):
        # Step 1: Execute parent's type validation (__set__ from TypedAttribute)
        super().__set__(instance, value) 
        
        # Step 2: Perform range validation
        if value < self.min_val:
            raise ValueError(f"Value must be at least {self.min_val}.")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"Value cannot exceed {self.max_val}.")
            
# --- 4. Hybrid Descriptor: Lazy Default Initialization ---

class LazyDefaultString(ConfigDescriptor):
    """
    Provides a default value only upon first access if the attribute is unset.
    Simulates a time-consuming initialization (e.g., fetching a token).
    """
    def __init__(self, default_prefix: str):
        super().__init__()
        self.default_prefix = default_prefix

    def __get__(self, instance: Any, owner: Type):
        if instance is None:
            return self
        
        # Check if the value is already stored in the instance dictionary
        if self.storage_name not in instance.__dict__:
            print(f"--- [LAZY LOAD]: Initializing default for {self.storage_name} ---")
            # Simulate a slow lookup/calculation
            time.sleep(0.5) 
            
            # Construct the default value dynamically
            default_value = f"{self.default_prefix}{instance.__class__.__name__.lower()}-{time.time()}"
            
            # Store the calculated value in the instance dictionary for future access
            instance.__dict__[self.storage_name] = default_value
            
        return instance.__dict__[self.storage_name]

    # Note: We include __set__ to make this a Data Descriptor, allowing user override
    def __set__(self, instance: Any, value: str):
        if not isinstance(value, str):
             raise TypeError("Lazy default attribute must be a string if explicitly set.")
        instance.__dict__[self.storage_name] = value

# --- 5. Owner Class: The API Configuration ---

class APIServiceConfig:
    """Configuration holder using descriptors for controlled attribute access."""
    
    # Descriptor Definitions (Class Attributes)
    api_key = TypedAttribute(str, default="DEFAULT_API_KEY_001")
    timeout_seconds = PositiveInt(min_val=5, max_val=30)
    max_retries = PositiveInt(min_val=1, max_val=5)
    
    # Lazy initialization for a dynamic resource URL
    resource_url = LazyDefaultString(default_prefix="https://api.v2/resources/") 

    def __init__(self, key: str, timeout: int = 10, retries: int = 3):
        # Assignment triggers the __set__ method of the respective descriptor
        self.api_key = key
        self.timeout_seconds = timeout
        self.max_retries = retries

# --- 6. Demonstration and Testing ---

print("--- 1. Configuration Setup (Successful Assignments) ---")
try:
    config = APIServiceConfig(key="VALID_KEY_XYZ", timeout=15)
    print(f"Config API Key: {config.api_key}")
    print(f"Config Timeout: {config.timeout_seconds} seconds")
    print(f"Config Retries: {config.max_retries}")
except Exception as e:
    print(f"Setup Error: {e}")

print("\n--- 2. Validation Failure Tests (Assignment Blocked by __set__) ---")
try:
    config.timeout_seconds = 60  # Exceeds max_val=30
except ValueError as e:
    print(f"Caught Expected Error (Range): {e}")

try:
    config.api_key = 12345  # Wrong type (int instead of str)
except TypeError as e:
    print(f"Caught Expected Error (Type): {e}")

print("\n--- 3. Lazy Loading Demonstration (First Access Only) ---")
# First access triggers the slow calculation inside LazyDefaultString.__get__
print(f"Resource URL (Initial access): {config.resource_url}") 
# Second access uses the stored value, skipping the calculation
print(f"Resource URL (Second access): {config.resource_url}")

# Verify that the internal storage name is used
print(f"\nInternal storage check: {'_resource_url' in config.__dict__}")


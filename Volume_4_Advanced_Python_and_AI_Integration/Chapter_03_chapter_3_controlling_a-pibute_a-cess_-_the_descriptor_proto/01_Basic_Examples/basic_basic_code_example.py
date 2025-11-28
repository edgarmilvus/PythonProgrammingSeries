
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

import sys

class PositiveInteger:
    """
    A Data Descriptor designed to enforce that the attribute it manages 
    is always a non-negative integer.
    """
    
    def __init__(self, name=None):
        # 1. Store the public name of the attribute for clearer error messages.
        self.name = name
        
        # 2. Crucial: Initialize a dictionary to store the actual attribute values.
        # Descriptors are class attributes, but they must store instance-specific data.
        # We use a dictionary where the key is the ID of the owner instance (id(instance)).
        self._data = {} 

    # --- Attribute Retrieval (Reading: instance.attribute) ---
    def __get__(self, instance, owner):
        """Called when the attribute is accessed."""
        
        # If the attribute is accessed via the Class (e.g., InventoryProduct.stock_level)
        if instance is None:
            # Return the descriptor instance itself, allowing introspection.
            return self
        
        # Retrieve the value specific to this instance.
        # If the value hasn't been set, return 0 as a safe default for stock.
        # We use id(instance) to uniquely identify the owner object.
        return self._data.get(id(instance), 0) 

    # --- Attribute Assignment (Writing: instance.attribute = value) ---
    def __set__(self, instance, value):
        """Called when the attribute is assigned a new value."""
        
        # 1. Type Validation: Ensure the input is an integer.
        if not isinstance(value, int):
            # Raise a detailed error using the stored attribute name.
            raise TypeError(f"'{self.name}' must be an integer, not {type(value).__name__}")
        
        # 2. Value Validation: Ensure the input is positive or zero.
        if value < 0:
            raise ValueError(f"'{self.name}' must be a positive number (>= 0). Received: {value}")
        
        # 3. Storage: If validation passes, store the value.
        # The key is the unique ID of the specific InventoryProduct instance.
        self._data[id(instance)] = value

    # --- Attribute Deletion (Deleting: del instance.attribute) ---
    def __delete__(self, instance):
        """Called when the attribute is deleted."""
        
        # Check if the instance has a stored value to delete.
        instance_key = id(instance)
        if instance_key in self._data:
            # Remove the specific instance's data from the storage dictionary.
            del self._data[instance_key]
            # Print confirmation for demonstration purposes
            print(f"[{self.name}] Data for instance {instance_key} successfully deleted.")
        else:
            # If the attribute wasn't set or already deleted, raise an error.
            raise AttributeError(f"Cannot delete attribute '{self.name}': No value stored.")


# --- The Owner Class ---
class InventoryProduct:
    """Class that uses the descriptor to manage its stock level."""
    
    # CRITICAL STEP: Assign the descriptor instance to the class attribute.
    # This makes 'stock_level' a managed attribute.
    stock_level = PositiveInteger(name='stock_level') 
    
    def __init__(self, name, initial_stock):
        self.name = name
        # Setting this attribute triggers PositiveInteger.__set__
        self.stock_level = initial_stock 

# --- Demonstration and Flow Execution ---

# 1. Initialization (Triggers __set__)
product_a = InventoryProduct("CPU Cooler X", 50)
product_b = InventoryProduct("Thermal Paste Z", 120)

print("--- Initial State ---")
print(f"{product_a.name} stock: {product_a.stock_level}") # Triggers __get__
print(f"{product_b.name} stock: {product_b.stock_level}") # Triggers __get__

# 2. Valid Assignment (Triggers __set__)
product_a.stock_level = 48
print(f"\n--- After Valid Update ---")
print(f"{product_a.name} stock updated to: {product_a.stock_level}")

# 3. Invalid Assignment: Negative Value (Triggers __set__ validation failure)
print(f"\n--- Testing Validation (Value Error) ---")
try:
    product_a.stock_level = -10
except ValueError as e:
    print(f"Validation Blocked (Value Error): {e}")

# 4. Invalid Assignment: Wrong Type (Triggers __set__ validation failure)
print(f"\n--- Testing Validation (Type Error) ---")
try:
    product_b.stock_level = "Out of Stock"
except TypeError as e:
    print(f"Validation Blocked (Type Error): {e}")
    
# 5. Deletion (Triggers __delete__)
print(f"\n--- Testing Deletion ---")
del product_a.stock_level

# 6. Access After Deletion (Triggers __get__)
# Since __delete__ removed the key, __get__ will return the default (0).
print(f"{product_a.name} stock after deletion: {product_a.stock_level}") 

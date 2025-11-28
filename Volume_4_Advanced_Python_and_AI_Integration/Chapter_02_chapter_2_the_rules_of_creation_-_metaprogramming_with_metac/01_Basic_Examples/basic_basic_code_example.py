
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

# custom_metaclass_example.py

# Step 1: Define the Metaclass, inheriting from the base class factory 'type'
class AttributeEnforcer(type):
    """
    A custom metaclass responsible for enforcing specific naming conventions
    and adding mandatory attributes to any class that uses it.
    """

    # Step 2: Override the __new__ method
    # This method is called *before* the class object itself is created.
    # mcs: Metaclass class (AttributeEnforcer)
    # name: Name of the class being created (e.g., 'AIConfig')
    # bases: Tuple of base classes (e.g., (object,))
    # attrs: Dictionary of attributes defined in the class body
    def __new__(mcs, name, bases, attrs):
        print(f"\n[Metaclass Hook] Processing class definition: {name}")

        # 3a. Initialize a new dictionary to store the modified attributes
        modified_attrs = {}

        # 3b. Iterate over the original attributes defined by the developer
        for key, value in attrs.items():
            # Skip Python internal attributes (dunder methods like __init__, __doc__)
            if not key.startswith('__'):
                # Enforce the required uppercase naming convention
                new_key = key.upper()
                modified_attrs[new_key] = value
                print(f"  -> Renamed attribute '{key}' to '{new_key}'")
            else:
                # Preserve internal attributes unchanged
                modified_attrs[key] = value

        # 4. Inject a mandatory framework attribute
        MANDATORY_VERSION_KEY = "_FRAMEWORK_VERSION_"
        if MANDATORY_VERSION_KEY not in modified_attrs:
            modified_attrs[MANDATORY_VERSION_KEY] = 4.1  # Current Book/Framework Version
            print(f"  -> Injected mandatory attribute: {MANDATORY_VERSION_KEY}")

        # 5. Call the standard type creation mechanism (the parent 'type' class)
        # This final call creates the actual class object based on our modified blueprint.
        new_class = super().__new__(mcs, name, bases, modified_attrs)

        print(f"[Metaclass Hook] Class {name} creation complete.")
        return new_class

# Step 6: Define a class that explicitly uses the custom metaclass
# The 'metaclass=...' keyword directs Python to use AttributeEnforcer instead of 'type'.
class AIConfig(metaclass=AttributeEnforcer):
    """
    A configuration class whose definition is intercepted and modified
    by the AttributeEnforcer metaclass.
    """
    # User-defined attributes (note the mixed case)
    model_name = "GPT-4o"
    temperature = 0.7
    max_tokens = 2048

    def __init__(self, description):
        # Instance initialization code
        self.description = description

    def show_config(self):
        # Accessing the attributes using their enforced uppercase names
        print(f"\n--- {self.description} Configuration ---")
        # We must use the uppercase names, as the lowercase names no longer exist
        print(f"Model: {self.MODEL_NAME}")
        print(f"Version: {self._FRAMEWORK_VERSION_}")
        print(f"Temp: {self.TEMPERATURE}")

# Step 7: Demonstrate usage and verification
print("\n--- Runtime Execution ---")
config_instance = AIConfig("Production LLM Settings")
config_instance.show_config()

# Verification check: attempting to access the original attribute name fails
try:
    print(f"\nAttempting to access original name 'model_name': {AIConfig.model_name}")
except AttributeError as e:
    print(f"Access failed (expected): {e}")

# Verification check: accessing the metaclass-modified attribute name succeeds
print(f"Accessing enforced name 'MODEL_NAME': {AIConfig.MODEL_NAME}")


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

# 1. Define the Class Object (SystemComponent)
# The class itself is an instance of the built-in 'type' metaclass.
class SystemComponent:
    """
    A base class demonstrating attribute storage and lookup mechanics.
    """
    
    # 2. Class Attributes: Stored in SystemComponent.__dict__
    NAMESPACE = "CORE"
    VERSION = 1.0
    
    def __init__(self, name: str):
        # 3. Instance Attributes: Stored in the instance's __dict__
        self.name = name
        self.status = "Initialized"

    def get_info(self):
        """
        Method demonstrating attribute lookup chain:
        1. Check instance attributes (self.name)
        2. Check class attributes (self.VERSION)
        """
        return f"[{self.NAMESPACE}] {self.name} (v{self.VERSION}) Status: {self.status}"

# 4. Instance Creation
comp1 = SystemComponent("Database_Connector")
comp2 = SystemComponent("API_Handler")

print("--- INITIAL STATE ---")
print(f"Comp1: {comp1.get_info()}")
print(f"Comp2: {comp2.get_info()}")

# 5. Attribute Modification and Shadowing Demonstration

# 5a. Modify Instance Attribute (Unique to comp1)
comp1.status = "Active"

# 5b. Modify Class Attribute (Affects all future lookups unless shadowed)
SystemComponent.VERSION = 1.1 

# 5c. Shadowing: Creating an instance attribute that masks the class attribute
# Python creates 'VERSION' only in comp2's internal dictionary.
comp2.VERSION = 99.0 

print("\n--- STATE AFTER MODIFICATION ---")
print(f"Comp1 (Class attribute updated, status unique): {comp1.get_info()}")
print(f"Comp2 (Class attribute shadowed, uses 99.0): {comp2.get_info()}")

# 6. Deep Inspection using __dict__

print("\n--- OBJECT MODEL INSPECTION ---")

# 6a. Class Inspection
print(f"\nType of SystemComponent: {type(SystemComponent)}")
print(f"Class Attributes (SystemComponent.__dict__ keys): {SystemComponent.__dict__.keys()}")
print(f"Class VERSION value: {SystemComponent.VERSION}")

# 6b. Instance 1 Inspection (Shows instance-specific attributes)
print(f"\nType of comp1: {type(comp1)}")
print(f"Comp1 Instance Attributes (comp1.__dict__): {comp1.__dict__}")
# Note: VERSION is not in comp1.__dict__, it is accessed via the class.

# 6c. Instance 2 Inspection (Shows the shadowed attribute)
print(f"Comp2 Instance Attributes (comp2.__dict__): {comp2.__dict__}")
# Note: VERSION is now explicitly in comp2.__dict__, masking the class VERSION (1.1).

# 7. Proving the Class Attribute is still 1.1
print(f"Direct Class Access (SystemComponent.VERSION): {SystemComponent.VERSION}")

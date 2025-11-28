
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
from typing import List, Callable, Any

# --- Exercise 1: Configuration Contract Enforcer ---

class ConfigurationContractMeta(type):
    """
    Metaclass that enforces the presence of required configuration attributes 
    (MODEL_NAME, MAX_TOKENS, DEFAULT_TEMPERATURE) during class creation.
    """
    def __new__(mcs, name: str, bases: tuple, clsdict: dict):
        required_attrs = ['MODEL_NAME', 'MAX_TOKENS', 'DEFAULT_TEMPERATURE']
        
        # Only apply enforcement to concrete subclasses, not the base class itself
        # We assume the base class is named BaseConfiguredComponent for clarity
        if name != 'BaseConfiguredComponent':
            for attr in required_attrs:
                if attr not in clsdict:
                    raise TypeError(
                        f"Configuration contract violation in class '{name}': "
                        f"Required attribute '{attr}' is missing."
                    )
        
        return super().__new__(mcs, name, bases, clsdict)

# Base class using the metaclass
class BaseConfiguredComponent(metaclass=ConfigurationContractMeta):
    pass

# Demonstration of success
class ValidLLMConfig(BaseConfiguredComponent):
    MODEL_NAME = "gpt-4o"
    MAX_TOKENS = 4096
    DEFAULT_TEMPERATURE = 0.7

print(f"[Ex 1] ValidLLMConfig successfully defined.")

# Demonstration of failure (will raise TypeError upon definition)
try:
    class InvalidLLMConfig(BaseConfiguredComponent):
        MODEL_NAME = "claude-3"
        # MAX_TOKENS is missing
        DEFAULT_TEMPERATURE = 0.9
except TypeError as e:
    print(f"\n[Ex 1] Successfully caught expected error for InvalidLLMConfig: {e}")

# --- Exercise 2: The Path-Resolving Component Injector ---

class PathResolverMeta(type):
    """
    Metaclass that automatically resolves and injects a FULL_PATH attribute 
    based on the RESOURCE_NAME attribute, using os.path.join().
    """
    BASE_DIR = "/opt/data/resources"

    def __new__(mcs, name: str, bases: tuple, clsdict: dict):
        # 1. Check for required attribute
        if 'RESOURCE_NAME' not in clsdict:
            # Skip enforcement on the base class
            if name != 'ResourceComponent':
                 raise TypeError(
                    f"Path contract violation in class '{name}': "
                    f"Required attribute 'RESOURCE_NAME' is missing."
                )
        else:
            resource_name = clsdict['RESOURCE_NAME']
            
            # 2. Construct the platform-independent full path
            full_path = os.path.join(mcs.BASE_DIR, resource_name)
            
            # 3. Inject the FULL_PATH into the class dictionary
            clsdict['FULL_PATH'] = full_path
        
        return super().__new__(mcs, name, bases, clsdict)

class ResourceComponent(metaclass=PathResolverMeta):
    pass

class ModelWeightLoader(ResourceComponent):
    RESOURCE_NAME = 'bert_weights.bin'

print(f"\n[Ex 2] ModelWeightLoader Path: {ModelWeightLoader.FULL_PATH}")
expected_path = os.path.join("/opt/data/resources", "bert_weights.bin")
assert ModelWeightLoader.FULL_PATH == expected_path
print(f"[Ex 2] Path resolution successful and platform-independent.")


# --- Exercise 3: Dynamic Class Method Injection for Context Management ---

def _injected_context_getter(cls: Any) -> dict:
    """The function that will be injected as a class method."""
    print(f"[{cls.__name__}] Accessing simulated request context...")
    return { 'user_id': 42, 'request_id': 'xyz', 'source': cls.__name__ }

class ContextInjectorMeta(type):
    """
    Metaclass that injects a standardized 'get_current_context' class method.
    """
    def __new__(mcs, name: str, bases: tuple, clsdict: dict):
        # 1. Wrap the function using classmethod() to ensure it binds correctly
        context_method = classmethod(_injected_context_getter)
        
        # 2. Inject the wrapped method into the class dictionary
        clsdict['get_current_context'] = context_method
        
        # 3. Finalize class creation
        return super().__new__(mcs, name, bases, clsdict)

class APILogger(metaclass=ContextInjectorMeta):
    def log_request(self):
        context = self.get_current_context()
        print(f"Logging request ID: {context['request_id']}")

print("\n[Ex 3] Testing dynamic class method injection:")
# Call the injected method directly on the class
context_data = APILogger.get_current_context()
print(f"[Ex 3] Retrieved context data: {context_data}")

# Verify it works via an instance as well
logger = APILogger()
logger.log_request()


# --- Exercise 4: Interactive Challenge - Enforcing Dependency Contracts ---

# Global registry simulation
COMPONENT_REGISTRY = {}

class ComponentRegistryMeta(type):
    """
    Modified metaclass to enforce dependency contract (must have a callable 
    get_dependencies method) and register the component.
    """
    def __new__(mcs, name: str, bases: tuple, clsdict: dict):
        
        # Define the required method name
        DEP_METHOD_NAME = 'get_dependencies'
        
        # Skip base classes (assuming they end with 'Base' or similar marker)
        if not name.endswith('ComponentBase'):

            # --- Dependency Contract Enforcement ---
            
            # 1. Check for presence
            if DEP_METHOD_NAME not in clsdict:
                raise TypeError(
                    f"Dependency Contract Violation in '{name}': "
                    f"Must define the class method '{DEP_METHOD_NAME}()'."
                )
            
            dep_attr = clsdict[DEP_METHOD_NAME]
            
            # 2. Check for callability
            if not callable(dep_attr):
                 raise TypeError(
                    f"Dependency Contract Violation in '{name}': "
                    f"'{DEP_METHOD_NAME}' must be a callable method, not a {type(dep_attr).__name__}."
                )
        
        # Create the class object
        cls = super().__new__(mcs, name, bases, clsdict)
        
        # --- Registration Logic ---
        if not name.endswith('ComponentBase'):
            COMPONENT_REGISTRY[name] = cls
            print(f"-> Registered component: {name}")
        
        return cls

# Base class for demonstration
class AIComponentBase(metaclass=ComponentRegistryMeta):
    pass

# Successful component definition
class ValidatorComponent(AIComponentBase):
    
    @classmethod
    def get_dependencies(cls) -> List[str]:
        return ["DataPreprocessor", "ModelLoader"]

# Failed component definition (raises TypeError)
try:
    class BrokenComponent(AIComponentBase):
        # This is a string, which is not callable
        get_dependencies = "I am not a function" 
        
except TypeError as e:
    print(f"\n[Ex 4] Successfully caught expected error for BrokenComponent: {e}")

# Verification of successful registration
print(f"[Ex 4] Registry Contents: {list(COMPONENT_REGISTRY.keys())}")
if 'ValidatorComponent' in COMPONENT_REGISTRY:
    print(f"[Ex 4] ValidatorComponent Dependencies: {ValidatorComponent.get_dependencies()}")

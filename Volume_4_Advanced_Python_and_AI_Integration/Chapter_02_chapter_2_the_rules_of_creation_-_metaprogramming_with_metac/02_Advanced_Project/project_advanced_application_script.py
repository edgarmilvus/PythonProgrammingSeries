
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

import typing

# I. Global Registry and Metaclass Definition
COMPONENT_REGISTRY: typing.Dict[str, typing.Type['PipelineComponent']] = {}

class ComponentRegistryMeta(type):
    """
    Metaclass responsible for enforcing component structure, injecting utility methods, 
    and performing automatic registration into the global registry.
    """
    def __new__(mcs, name, bases, attrs):
        # 1. Skip processing for the abstract base class itself ('PipelineComponent')
        # This prevents the metaclass logic from running on the definition of the base class.
        if name == 'PipelineComponent':
            return super().__new__(mcs, name, bases, attrs)

        # 2. Enforce API Contract
        required_attrs = ['COMPONENT_ID']
        required_methods = ['process']

        # Check for required class attributes (e.g., the unique ID)
        for attr in required_attrs:
            if attr not in attrs:
                raise TypeError(f"Component {name} must define the class attribute '{attr}'.")

        # Check for required instance methods (the core functionality)
        for method in required_methods:
            if method not in attrs or not callable(attrs[method]):
                raise TypeError(f"Component {name} must implement the method '{method}' as a callable.")

        # 3. Dynamic Attribute Injection: Inject a standardized configuration accessor
        def get_config(cls):
            """Dynamically added class method for standardized config retrieval."""
            # Accesses attributes defined on the class object
            return {
                "id": cls.COMPONENT_ID, 
                "name": cls.__name__, 
                "type": "Processing_Unit",
                "registered_by": "Metaclass"
            }
        
        # Inject the method into the class attributes dictionary (attrs) 
        # Note: We must wrap it in classmethod() before it is finalized.
        attrs['get_config'] = classmethod(get_config)

        # 4. Create the final class object using the standard type.__new__
        new_class = super().__new__(mcs, name, bases, attrs)

        # 5. Automatic Registration (Post-creation, using the finalized class object)
        component_id = new_class.COMPONENT_ID
        if component_id in COMPONENT_REGISTRY:
            raise ValueError(f"Component ID '{component_id}' already registered by another class.")
        
        COMPONENT_REGISTRY[component_id] = new_class
        print(f"-> Registered Component: {name} ({component_id})")

        return new_class

# II. Base Class Definition
class PipelineComponent(metaclass=ComponentRegistryMeta):
    """
    The abstract base component that leverages the metaclass for validation 
    and automatic framework integration.
    """
    pass 

# III. Concrete Component Implementations (These trigger the metaclass __new__ upon definition)
class InputValidator(PipelineComponent):
    """Component to sanitize and validate user input."""
    COMPONENT_ID = "input_validator_v1"
    
    def process(self, data: str) -> str:
        # Simple sanitization logic
        print(f"[Validator] Cleaning input data: stripping whitespace and lowercasing.")
        return data.strip().lower()

class LLMQueryExecutor(PipelineComponent):
    """Component responsible for interacting with the external LLM API."""
    COMPONENT_ID = "llm_executor_v2"
    
    def process(self, data: str) -> str:
        # Placeholder for an actual API call
        print(f"[Executor] Submitting query: '{data[:25]}...'")
        return f"LLM_RESPONSE: The result for '{data}' is generated."

class ResultFormatter(PipelineComponent):
    """Component to structure the final output."""
    COMPONENT_ID = "output_formatter_v1"
    
    def process(self, data: str) -> str:
        # Logic to structure the final output
        print(f"[Formatter] Wrapping final result in JSON structure.")
        return f'{{"status": "success", "result": "{data}"}}'

# IV. Usage and Demonstration
def run_orchestrator(steps: list[str], initial_data: str):
    """
    Assembles and runs the pipeline dynamically by retrieving registered classes.
    """
    print("\n--- Pipeline Orchestrator Start ---")
    current_data = initial_data
    
    for step_id in steps:
        if step_id not in COMPONENT_REGISTRY:
            raise KeyError(f"Component ID '{step_id}' not found in registry. Check framework registration.")
        
        # Retrieve the Component Class object (not an instance) from the metaclass-managed registry
        ComponentClass = COMPONENT_REGISTRY[step_id]
        
        # Instantiate the component and process the data
        instance = ComponentClass()
        current_data = instance.process(current_data)
        
    print("--- Pipeline Orchestrator Complete ---")
    return current_data

# Demonstration
print("\n--- Framework Inspection ---")

# 1. Inspecting the registry and using the dynamically injected method
for comp_id, comp_cls in COMPONENT_REGISTRY.items():
    # We call get_config() directly on the class object, which was injected by the metaclass
    config = comp_cls.get_config() 
    print(f"| Config for {comp_id}: {config['name']} (Type: {config['type']})")

# 2. Running the pipeline
pipeline_sequence = ["input_validator_v1", "llm_executor_v2", "output_formatter_v1"]
input_text = "   What is the purpose of metaprogramming?   "

final_output = run_orchestrator(pipeline_sequence, input_text)

print(f"\nFinal Output:\n{final_output}")

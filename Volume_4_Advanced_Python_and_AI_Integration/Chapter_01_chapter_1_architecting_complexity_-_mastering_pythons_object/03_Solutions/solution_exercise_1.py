
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

import sys
from typing import Any

# --- Exercise 1: Dissecting the C3 Algorithm – The Multi-Layered Configuration Puzzle ---

print("--- Exercise 1: Dissecting the C3 Algorithm ---")

class BaseConfig:
    def initialize(self):
        print("1. BaseConfig initialized.")

class SecurityMixin:
    def initialize(self):
        print("2. SecurityMixin applied.")
        super().initialize()

class LoggingMixin:
    def initialize(self):
        print("3. LoggingMixin activated.")
        super().initialize()

class WebProtocol(BaseConfig):
    def initialize(self):
        print("4. WebProtocol setup.")
        super().initialize()

class ServiceEndpoint(LoggingMixin, SecurityMixin, WebProtocol):
    def initialize(self):
        print("5. ServiceEndpoint started.")
        super().initialize()

# 5. Verification: Print the MRO
print("\nMRO of ServiceEndpoint (C3 Linearization):")
# MRO: [ServiceEndpoint, LoggingMixin, SecurityMixin, WebProtocol, BaseConfig, object]
print(ServiceEndpoint.mro())

# 4. Prediction Challenge & 3. Execution
print("\nExecution Trace (Predicted and Actual Output):")
endpoint = ServiceEndpoint()
endpoint.initialize()

# Prediction Challenge Answer:
# The MRO dictates the flow of cooperative inheritance via super().initialize():
# 1. ServiceEndpoint (starts the chain)
# 2. LoggingMixin (calls super() -> SecurityMixin)
# 3. SecurityMixin (calls super() -> WebProtocol)
# 4. WebProtocol (calls super() -> BaseConfig)
# 5. BaseConfig (stops the chain)
# Output Sequence: 5, 3, 2, 4, 1.


# --- Exercise 2: Mastering Data Descriptors – The Type-Checked Configuration Validator ---

print("\n--- Exercise 2: Mastering Data Descriptors ---")

class StrictInt:
    """A data descriptor for strict integer validation within a defined range."""
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
        self.name = None # Placeholder for the attribute name

    def __set_name__(self, owner: type, name: str):
        """Called at class creation time to set the internal storage key."""
        # Use a mangled name to store the value on the instance
        self.name = f'_{name}'

    def __get__(self, instance: Any, owner: type) -> int:
        if instance is None:
            # Accessing from the class (returns the descriptor itself)
            return self
        
        # Retrieve value from the instance's dictionary
        if self.name not in instance.__dict__:
            raise AttributeError(f"Attribute '{self.name[1:]}' has not been set.")
        
        return instance.__dict__[self.name]

    def __set__(self, instance: Any, value: int):
        # 3. Check 1: Type validation
        if not isinstance(value, int):
            raise TypeError(f"Attribute must be an integer, got {type(value).__name__}.")
        
        # 3. Check 2: Range validation
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Value {value} is outside the allowed range "
                f"[{self.min_value}, {self.max_value}]."
            )
        
        # 3. Check 3: Store the validated value
        instance.__dict__[self.name] = value

class ServerConfig:
    # 4. Use descriptor instances
    port = StrictInt(min_value=1024, max_value=65535)
    threads = StrictInt(min_value=1, max_value=32)

config = ServerConfig()

# Demonstrate successful assignment and retrieval
config.port = 8080
config.threads = 16
print(f"Success: Server Port: {config.port}, Threads: {config.threads}")

# Demonstrate Failure Mode 1: Type Error
try:
    config.port = "invalid"
except TypeError as e:
    print(f"Failure (Type Error): {e}")

# Demonstrate Failure Mode 2: Value Error
try:
    config.threads = 50
except ValueError as e:
    print(f"Failure (Value Error): {e}")


# --- Exercise 3: Optimizing Memory Footprint with __slots__ and Controlled Mutability ---

print("\n--- Exercise 3: Optimizing Memory Footprint with __slots__ ---")

class TelemetryPoint:
    """Memory optimized class enforcing immutability after initialization."""
    # 1. Use __slots__ and include a flag for tracking initialization state
    __slots__ = ('timestamp', 'value', 'source_id', '_initialized')

    # 2. Initialization
    def __init__(self, timestamp, value, source_id):
        # Use object.__setattr__ to bypass the custom __setattr__ logic
        object.__setattr__(self, 'timestamp', timestamp)
        object.__setattr__(self, 'value', value)
        object.__setattr__(self, 'source_id', source_id)
        
        # Mark initialization as complete
        object.__setattr__(self, '_initialized', True)
        
    # 3. Enforce Immutability
    def __setattr__(self, name, value):
        # Check if initialization is complete and if the attribute is one of the slotted ones
        if getattr(self, '_initialized', False) and name in self.__slots__:
            raise AttributeError(f"Cannot modify attribute '{name}' after initialization.")
        
        # For initialization or setting non-slotted attributes (which will fail 
        # because __dict__ is missing, fulfilling requirement 5 implicitly for non-slotted fields)
        object.__setattr__(self, name, value)

class StandardPoint:
    """Standard class for comparison."""
    def __init__(self, timestamp, value, source_id):
        self.timestamp = timestamp
        self.value = value
        self.source_id = source_id

# 4. Demonstrate memory saving
tp = TelemetryPoint(1678886400, 42.5, "sensor_A")
sp = StandardPoint(1678886400, 42.5, "sensor_A")

print(f"Memory Check: Slotted TelemetryPoint size: {sys.getsizeof(tp)} bytes")
print(f"Memory Check: StandardPoint size: {sys.getsizeof(sp)} bytes")

# Test immutability enforcement
print(f"Initial value: {tp.value}")
try:
    tp.value = 99.9  # Attempt modification
except AttributeError as e:
    print(f"Test Immutability: Caught expected error: {e}")

# 5. Test non-slotted attribute assignment (should fail due to absence of __dict__)
try:
    tp.new_field = "test"
except AttributeError as e:
    print(f"Test No __dict__: Caught expected error: {e}")


# --- Exercise 4: Interactive Challenge – Controlling Class Lifecycle via __init_subclass__ ---

print("\n--- Exercise 4: Controlling Class Lifecycle via __init_subclass__ ---")

class EngineBase:
    registry = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # 1. Enforce Configuration Check
        mandatory_keys = getattr(cls, 'MANDATORY_CONFIG_KEYS', None)
        
        if not mandatory_keys or not isinstance(mandatory_keys, (list, tuple)) or not mandatory_keys:
            # Allow the base class itself to be defined
            if cls.__name__ != 'EngineBase':
                raise TypeError(
                    f"Subclass {cls.__name__} must define a non-empty "
                    f"'MANDATORY_CONFIG_KEYS' class attribute."
                )

        if cls.__name__ != 'EngineBase':
            EngineBase.registry[cls.__name__] = cls
            print(f"[{cls.__name__}] Registered successfully.")
            
    def __init__(self):
        # Base init must be called for cooperative inheritance
        super().__init__()
        # Note: EngineBase does not print anything here, allowing the chain to terminate cleanly.

class DiagnosticMixin:
    # 2. Diagnostic Mixin
    def __init__(self):
        print("--- Diagnostic check completed first. ---")
        # NOTE: We do NOT call super() here. The concrete class will manage the chain flow.

class FeatureMixin:
    # 3. Feature Mixin
    def __init__(self):
        print("--- Feature setup completed. ---")
        super().__init__() # Cooperates with the MRO chain

# 4. Test Case: OptimizedEngine
class OptimizedEngine(EngineBase, FeatureMixin, DiagnosticMixin):
    MANDATORY_CONFIG_KEYS = ('host', 'port')

    def __init__(self):
        # 5. Validation: Force DiagnosticMixin to run first, regardless of MRO position.
        # We explicitly call the DiagnosticMixin's __init__ method directly.
        DiagnosticMixin.__init__(self) 
        
        # Then, we call super(), which starts the cooperative chain from the next class 
        # in the MRO (FeatureMixin, then EngineBase, then object).
        super().__init__() 
        
        print(f"[{self.__class__.__name__}] Initialization complete.")

print("\nOptimizedEngine MRO (Note the position of DiagnosticMixin):")
print(OptimizedEngine.mro())

print("\nInstantiating OptimizedEngine (Watch the forced execution order):")
engine = OptimizedEngine()

# Test case for enforcement failure
try:
    class MissingConfigEngine(EngineBase):
        pass # Fails because MANDATORY_CONFIG_KEYS is missing
except TypeError as e:
    print(f"\nTest Enforcement Failure: Caught expected error: {e}")


# --- Exercise 5: Advanced Class Construction – Controlling Subclassing with __slots__ Enforcement ---

print("\n--- Exercise 5: Advanced Class Construction – __slots__ Enforcement ---")

class SlottedBase:
    """Base class enforcing __slots__ definition in all subclasses."""
    # 1. Base class uses slots itself
    __slots__ = () 

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # 2. Get __slots__ safely
        slots = getattr(cls, '__slots__', None)
        
        # 3. Validation Logic
        if cls.__name__ == 'SlottedBase':
            return # Skip validation for the base class itself

        if slots is None or not isinstance(slots, (list, tuple)) or not slots:
            # Check for missing or empty slots
            raise TypeError(
                f"Subclass {cls.__name__} must define a non-empty "
                f"__slots__ attribute for memory optimization."
            )
        
        # Check if __dict__ was explicitly added, which defeats the purpose
        if '__dict__' in slots:
             raise TypeError(
                f"Subclass {cls.__name__} violates SlottedBase constraint: "
                f"__dict__ must not be included in __slots__."
            )

class ValidDataModel(SlottedBase):
    """4. Correctly defines __slots__."""
    __slots__ = ('key', 'value', 'count')
    
    def __init__(self, k, v, c):
        self.key = k
        self.value = v
        self.count = c

print("\nValidDataModel created successfully.")
valid_instance = ValidDataModel(1, 2, 3)

# 5. Demonstrate missing __dict__
if not hasattr(valid_instance, '__dict__'):
    print("Test __dict__ Absence: ValidDataModel instance successfully lacks a __dict__.")
else:
    print("Error: ValidDataModel instance still has a __dict__.")

# 4. Test InvalidDataModel (should fail during class definition)
try:
    class InvalidDataModel(SlottedBase):
        pass # Missing __slots__
except TypeError as e:
    print(f"\nTest Enforcement Failure: Caught expected error: {e}")


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

import time
import threading
from typing import Callable, Any, List, Optional

# --- Exercise 1: The Robust Integer Validator and Range Enforcer (Data Descriptor) ---

class RangedInt:
    """
    Data descriptor enforcing type (int) and range constraints.
    Uses __set_name__ for robust private storage key management.
    """
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
        self.public_name = None
        self.private_name = None

    def __set_name__(self, owner, name):
        # Capture the name used in the owner class and define a private storage key
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Retrieve value from the instance's private storage
        if self.private_name not in instance.__dict__:
            # This case should ideally not happen if __init__ sets the value
            raise AttributeError(f"'{self.public_name}' has not been set.")
            
        return instance.__dict__[self.private_name]

    def __set__(self, instance, value):
        # 1. Type Validation
        if not isinstance(value, int):
            raise TypeError(
                f"Attribute '{self.public_name}' must be an integer, not {type(value).__name__}"
            )

        # 2. Range Validation
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Attribute '{self.public_name}' must be between {self.min_value} and {self.max_value}. Got {value}."
            )

        # 3. Storage: Store in the instance's dictionary using the private key
        instance.__dict__[self.private_name] = value

class Product:
    # Applying the descriptor
    quantity = RangedInt(min_value=1, max_value=100)
    
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity # This triggers RangedInt.__set__

# --- Exercise 2: The Lazy Property Cache (Non-Data Descriptor) ---

# Mock expensive function
def simulate_data_fetch(instance):
    """Simulates a time-consuming calculation based on the owner instance."""
    time.sleep(1) # Simulate delay
    return f"Data fetched for {instance.report_id} at {time.time()}"

class LazyCalculator:
    """
    Non-data descriptor that performs an expensive calculation only on first access
    and caches the result directly on the instance, shadowing itself for subsequent calls.
    """
    def __init__(self, calculation: Callable):
        self.calculation = calculation
        self.public_name = None
    
    def __set_name__(self, owner, name):
        self.public_name = name

    def __get__(self, instance, owner):
        if instance is None:
            # Access via class (ReportGenerator.complex_data)
            return self
        
        # This is the first access. Run calculation.
        print(f"[{self.public_name}] Calculating expensive data...")
        result = self.calculation(instance)
        
        # Cache the result directly on the instance's __dict__
        # This creates a standard instance attribute that shadows the descriptor 
        # (since this is a non-data descriptor).
        setattr(instance, self.public_name, result)
        
        print(f"[{self.public_name}] Calculation complete and cached.")
        return result

class ReportGenerator:
    def __init__(self, report_id):
        self.report_id = report_id
    
    # Apply the non-data descriptor
    complex_data = LazyCalculator(simulate_data_fetch)

# --- Exercise 3: Contextual Flasher Descriptor (Advanced State Management) ---

# Simple simulation of a Request Context
class RequestContext:
    def __init__(self, request_id: int):
        self.request_id = request_id
        self.messages: List[str] = []

# Simulation of a stack manager 
class ContextStack:
    # Using a simple list for simulation; in a real app, this would be thread-local
    _stack: List[RequestContext] = [] 
    
    @staticmethod
    def push(context: RequestContext):
        ContextStack._stack.append(context)
        print(f"--- Context {context.request_id} Pushed ---")

    @staticmethod
    def pop() -> Optional[RequestContext]:
        if ContextStack._stack:
            context = ContextStack._stack.pop()
            print(f"--- Context {context.request_id} Popped ---")
            return context
        return None

    @staticmethod
    def get_current() -> RequestContext:
        if not ContextStack._stack:
            raise RuntimeError("Cannot access context: No active request context found.")
        return ContextStack._stack[-1]

class Flasher:
    """
    Data descriptor that interacts with the global ContextStack 
    to manage request-specific flash messages.
    """
    # Flasher is a data descriptor because it implements both __get__ and __set__

    def __get__(self, instance, owner) -> List[str]:
        if instance is None:
            return self
            
        context = ContextStack.get_current()
        
        # Retrieve and clear (Flashing mechanism)
        messages = list(context.messages)
        context.messages.clear()
        
        return messages

    def __set__(self, instance, message: str):
        context = ContextStack.get_current()
        
        # Append message to the current context
        context.messages.append(message)
        print(f"[Flash Set] Message added: '{message[:20]}...' to Context {context.request_id}")

class WebController:
    # The descriptor manages the attribute access, but storage is external (in ContextStack)
    flash_messages = Flasher()

# --- Exercise 4: Interactive Challenge - Enforcing Immutability in Configuration Models ---

class ImmutableAttribute:
    """
    Data descriptor that allows assignment only once, enforcing immutability thereafter.
    """
    def __init__(self):
        self.public_name = None
        self.private_name = None

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Retrieve value from private storage
        if self.private_name not in instance.__dict__:
            # Allows access to the attribute only if it has been set
            raise AttributeError(f"'{self.public_name}' has not been initialized.")
            
        return instance.__dict__[self.private_name]

    def __set__(self, instance, value):
        # Check if the attribute has already been set 
        if self.private_name in instance.__dict__:
            raise AttributeError(
                f"Configuration Error: '{self.public_name}' is an immutable attribute and cannot be changed after initialization."
            )
        
        # Initial setting is allowed
        instance.__dict__[self.private_name] = value
        print(f"[Immutable Set] '{self.public_name}' initialized to '{value}'")

# Modified ConfigurationModel using the ImmutableAttribute descriptor
class ConfigurationModel:
    """
    Configuration model where database_url and environment are immutable.
    """
    # Apply the Immutable Descriptor
    database_url = ImmutableAttribute()
    environment = ImmutableAttribute()
    
    # Standard mutable attribute (will be stored directly in instance.__dict__)
    port = 8080 

    def __init__(self, db_url, port, env):
        # Initial setting triggers ImmutableAttribute.__set__
        self.database_url = db_url 
        self.port = port # Standard assignment (bypasses descriptors if none exist for 'port')
        self.environment = env # Triggers ImmutableAttribute.__set__


# --- Demonstration Section ---

print("="*50)
print("DEMONSTRATION 1: RangedInt Validation")
print("="*50)
try:
    p1 = Product("Widget", 50)
    print(f"Product quantity set correctly: {p1.quantity}")
    
    p1.quantity = 99
    print(f"Product quantity changed to: {p1.quantity}")

    # Attempt 1: Out of range (101 > 100)
    print("\nAttempting p1.quantity = 101...")
    p1.quantity = 101
except (TypeError, ValueError) as e:
    print(f"Validation Error Caught (Expected): {e}")

try:
    # Attempt 2: Wrong type
    print("\nAttempting p1.quantity = 'ten'...")
    p1.quantity = "ten"
except (TypeError, ValueError) as e:
    print(f"Validation Error Caught (Expected): {e}")


print("\n"+"="*50)
print("DEMONSTRATION 2: LazyCalculator Memoization")
print("="*50)
report = ReportGenerator(report_id="Q3_2024")

# 1. First Access (Triggers calculation and caching)
start_time = time.time()
data1 = report.complex_data 
time1 = time.time() - start_time
print(f"First access time (includes 1s delay): {time1:.3f}s")

# 2. Second Access (Retrieves cached value instantly)
start_time = time.time()
data2 = report.complex_data 
time2 = time.time() - start_time
print(f"Second access time (cached): {time2:.3f}s")

print(f"\nData consistency check: {data1 == data2}")
# Check if descriptor is shadowed (should be True)
print(f"Is 'complex_data' now in instance __dict__? {'complex_data' in report.__dict__}")


print("\n"+"="*50)
print("DEMONSTRATION 3: Contextual Flasher")
print("="*50)

controller = WebController()
req1 = RequestContext(request_id=101)

# 1. Push Context
ContextStack.push(req1)

# 2. Flash messages via descriptor (__set__)
controller.flash_messages = "User logged in successfully."
controller.flash_messages = "Profile updated."
controller.flash_messages = "A critical warning occurred."

# Check context state before retrieval
print(f"\nContext 101 messages BEFORE retrieval: {req1.messages}")

# 3. Retrieve messages (triggers __get__, clears context list)
flashed = controller.flash_messages
print(f"\nRetrieved flashed messages: {flashed}")

# 4. Verify context is cleared
print(f"Context 101 messages AFTER retrieval: {req1.messages}")

# 5. Pop context
ContextStack.pop()


print("\n"+"="*50)
print("DEMONSTRATION 4: ImmutableAttribute Challenge")
print("="*50)

# 1. Initialization (Allowed)
conf = ConfigurationModel(
    db_url="postgresql://prod_db", 
    port=5432, 
    env="production"
)

print(f"\nInitial DB URL: {conf.database_url}")
print(f"Initial Port (Mutable): {conf.port}")

# 2. Attempt to change Immutable Attribute (database_url)
try:
    print("\nAttempting to change database_url...")
    conf.database_url = "mysql://new_db"
except AttributeError as e:
    print(f"Immutability Enforced (Expected): {e}")

# 3. Attempt to change Mutable Attribute (port)
try:
    print("\nAttempting to change port...")
    conf.port = 8081 # This is a standard instance attribute assignment
    print(f"New Port: {conf.port}")
except Exception as e:
    print(f"Unexpected Error: {e}")

# 4. Attempt to change another Immutable Attribute (environment)
try:
    print("\nAttempting to change environment...")
    conf.environment = "staging"
except AttributeError as e:
    print(f"Immutability Enforced (Expected): {e}")

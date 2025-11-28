
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
import functools
from typing import Callable, Any, Dict, Tuple

# --- Exercise 3 Setup ---
class PermissionDeniedError(Exception):
    """Custom exception for access control failures."""
    pass

# Simulate the current user's session data
CURRENT_USER = {'username': 'Alice', 'role': 'editor'}
# CURRENT_USER = {'username': 'Bob', 'role': 'admin'} # Uncomment to test success

# --- Exercise 1: The Stateful Counter ---

def id_generator_factory(prefix: str) -> Callable[[], str]:
    """
    Factory function that creates a unique ID generator using a closure.
    The inner function maintains an independent counter state.
    """
    counter = 0

    def generate_id():
        # Use nonlocal to modify the 'counter' variable in the factory's scope
        nonlocal counter
        counter += 1
        return f"{prefix}{counter:04d}"

    return generate_id

# Demonstration of Exercise 1
user_id_gen = id_generator_factory("USER-")
session_id_gen = id_generator_factory("SESSION-")

print("--- Exercise 1 Output ---")
print(f"User ID 1: {user_id_gen()}")
print(f"Session ID 1: {session_id_gen()}")
print(f"User ID 2: {user_id_gen()}")
print(f"Session ID 2: {session_id_gen()}")
print("-" * 20)


# --- Exercise 2: Robust Execution Profiler ---

def profile_execution(func: Callable) -> Callable:
    """
    Decorator that measures and logs the execution time of a function,
    handling arbitrary arguments.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        
        # Prepare arguments for clear logging
        arg_list = [repr(a) for a in args]
        kwarg_list = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        full_args = ", ".join(arg_list + kwarg_list)

        print(f"[PROFILE] Function '{func.__name__}({full_args})' executed in {elapsed:.4f} seconds.")
        
        return result
    return wrapper

@profile_execution
def complex_calculation(n: int, multiplier: float = 1.0) -> int:
    """Performs a time-consuming calculation."""
    time.sleep(0.05) # Simulate work
    total = sum(i * multiplier for i in range(n))
    return int(total)

print("--- Exercise 2 Output ---")
result_a = complex_calculation(100000, multiplier=2.5)
result_b = complex_calculation(10000)
print(f"Result A: {result_a}")
print("-" * 20)


# --- Exercise 3: Role-Based Access Control (RBAC) ---

def requires_role(required_role: str) -> Callable[[Callable], Callable]:
    """
    Decorator factory for role-based access control.
    Requires an outer function to accept the configuration argument (required_role).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_role = CURRENT_USER.get('role')
            
            if user_role == required_role:
                print(f"[RBAC] Access granted for {CURRENT_USER['username']} (Role: {user_role}).")
                return func(*args, **kwargs)
            else:
                msg = (f"User {CURRENT_USER['username']} (Role: {user_role}) "
                       f"denied access. Required role: {required_role}")
                print(f"[RBAC ERROR] {msg}")
                raise PermissionDeniedError(msg)
        return wrapper
    return decorator

@requires_role('admin')
def delete_critical_data(item_id: int):
    """Deletes critical data from the system."""
    return f"Successfully deleted item {item_id}."

print("--- Exercise 3 Output ---")
try:
    # This call will fail because CURRENT_USER is 'editor', not 'admin'
    delete_critical_data(42)
except PermissionDeniedError as e:
    print(f"Caught expected error: {e}")

# Verify metadata preservation (thanks to functools.wraps)
print("\n--- Metadata Check ---")
print(f"Decorated function name: {delete_critical_data.__name__}")
print(f"Decorated function docstring: {delete_critical_data.__doc__}")
print("-" * 20)


# --- Exercise 4: Interactive Challenge - Smart Cache Expiration ---

# Cache structure: {key: (result, timestamp)}
# Key is immutable (args tuple, sorted kwargs tuple)
CACHE_STORE: Dict[Tuple, Tuple[Any, float]] = {}

def ttl_cache(seconds: int) -> Callable[[Callable], Callable]:
    """
    A configurable caching decorator with a Time-To-Live (TTL).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a consistent, immutable key
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()

            if key in CACHE_STORE:
                result, timestamp = CACHE_STORE[key]
                
                # Check for expiration
                if current_time - timestamp < seconds:
                    print(f"[TTL CACHE] HIT: Serving cached result for {func.__name__} (Freshness: {current_time - timestamp:.2f}s)")
                    return result
                else:
                    print(f"[TTL CACHE] MISS/EXPIRED: Cache for {func.__name__} expired.")
            
            # Cache Miss or Expiration: Execute the function
            print(f"[TTL CACHE] Computing new result for {func.__name__}...")
            result = func(*args, **kwargs)
            
            # Store the new result with current timestamp
            CACHE_STORE[key] = (result, current_time)
            return result
        return wrapper
    return decorator

@ttl_cache(seconds=3) # Cache for 3 seconds
def fetch_external_data(endpoint: str, user_id: int) -> str:
    """Simulates fetching data from an external API."""
    time.sleep(0.1)
    return f"Data for {endpoint}:{user_id} @ {time.strftime('%H:%M:%S')}"

print("--- Exercise 4 Output ---")
print("Call 1:", fetch_external_data("/users", 101))
print("Call 2 (Immediate HIT):", fetch_external_data("/users", 101))
time.sleep(3.5) # Wait for cache to expire
print("Call 3 (After Expiration):", fetch_external_data("/users", 101))
print("-" * 20)


# --- Exercise 5: Stacking Decorators for Resilience ---

def log_activity(func: Callable) -> Callable:
    """Decorator to log function entry and exit."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[ACTIVITY LOG] Entering function: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            print(f"[ACTIVITY LOG] Exiting function: {func.__name__}")
    return wrapper

def retry_on_failure(max_attempts: int, delay: float = 0.5) -> Callable[[Callable], Callable]:
    """Decorator factory to retry function execution on ValueError."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts_left = max_attempts
            
            while attempts_left > 0:
                try:
                    print(f"[RETRY] Attempting execution (Attempt {max_attempts - attempts_left + 1} of {max_attempts})...")
                    return func(*args, **kwargs)
                except ValueError as e:
                    attempts_left -= 1
                    if attempts_left == 0:
                        print(f"[RETRY FAILED] All {max_attempts} attempts failed.")
                        raise # Re-raise the final exception
                    
                    print(f"[RETRY] Attempt failed ({e}). Retrying in {delay}s...")
                    time.sleep(delay)
            
        return wrapper
    return decorator

# Global counter to control when the simulated API succeeds
FAILURE_COUNT = 0
SUCCESS_THRESHOLD = 3 

# Order of execution: log_activity (outer wrapper) wraps retry_on_failure (inner wrapper)
@log_activity
@retry_on_failure(max_attempts=4)
def simulate_api_call(data: str):
    """Simulates a flaky API call that fails a few times before succeeding."""
    global FAILURE_COUNT
    
    if FAILURE_COUNT < SUCCESS_THRESHOLD:
        FAILURE_COUNT += 1
        print(f"    [API] Failure on call {FAILURE_COUNT}.")
        # The retry decorator catches this
        raise ValueError("Network connection unstable.")
    
    print("    [API] Success!")
    return f"Processed data: {data}"

print("--- Exercise 5 Output (Stacking Decorators) ---")
try:
    final_result = simulate_api_call("critical_payload")
    print(f"Final Result: {final_result}")
except Exception as e:
    print(f"Execution failed completely: {e}")
print("-" * 20)

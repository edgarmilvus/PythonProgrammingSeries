
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
import random
import asyncio
from functools import wraps

# --- Exercise 5.4.1: The Persistent Call Tracker ---

def create_call_tracker():
    """
    Factory function that generates a decorator capable of tracking 
    call statistics using closures for state management.
    """
    
    # The decorator function returned by the factory
    def tracker_decorator(func):
        # State variables closed over by the 'wrapper' and 'get_stats'
        call_count = 0
        last_arguments = ((), {})
        history = [] # Stores return values of last 3 calls

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_count, last_arguments, history
            
            # Increment call count immediately as this tracks attempts
            call_count += 1
            
            try:
                result = func(*args, **kwargs)
                
                # Update state only upon successful execution
                last_arguments = (args, kwargs)
                history.append(result)
                
                # Maintain history size (last 3 calls)
                if len(history) > 3:
                    history.pop(0) 
                    
                return result
            except Exception as e:
                # If the function fails, we still tracked the attempt (call_count)
                raise e

        def get_stats():
            """Returns the current state of the tracked function."""
            return {
                "call_count": call_count,
                "last_arguments": last_arguments,
                "history": history
            }
        
        # Attach the inspection method to the wrapped function
        wrapper.get_stats = get_stats
        
        return wrapper

    return tracker_decorator

# Example Usage for E5.4.1 (Verification)
# tracker = create_call_tracker()
# 
# @tracker
# def calculate_sum(a, b):
#     return a + b
# 
# calculate_sum(10, 5) # call 1
# calculate_sum(20, 3) # call 2
# calculate_sum(1, 1)  # call 3
# calculate_sum(5, 5)  # call 4 (pushes out call 1 result)
# # print(calculate_sum.get_stats()) 
# # Expected history: [23, 2, 10]

# --- Exercise 5.4.2: Dynamic Data Validator Factory ---

def make_validator_factory(rule_type, threshold):
    """
    Creates a specialized validation function based on the provided rule type 
    and threshold, encapsulating these parameters via closure.
    """

    def validator(data):
        """The actual validation function returned by the factory."""
        
        is_valid = False
        error_message = ""

        if rule_type == 'min_length':
            if not isinstance(data, (str, list, tuple)):
                raise TypeError("Min length validation requires iterable data.")
            if len(data) >= threshold:
                is_valid = True
            else:
                error_message = f"Data length ({len(data)}) is less than minimum required length of {threshold}."
        
        elif rule_type == 'max_value':
            if not isinstance(data, (int, float)):
                 raise TypeError("Max value validation requires numerical data.")
            if data <= threshold:
                is_valid = True
            else:
                error_message = f"Value {data} exceeds maximum allowed value of {threshold}."
        
        elif rule_type == 'is_positive':
            # Note: threshold is ignored here, demonstrating configurable behavior
            if not isinstance(data, (int, float)):
                 raise TypeError("Positive check requires numerical data.")
            if data > 0:
                is_valid = True
            else:
                error_message = f"Value {data} must be positive."
        
        else:
            raise NotImplementedError(f"Rule type '{rule_type}' is not supported.")

        if not is_valid:
            raise ValueError(error_message)
        
        return True

    return validator

# Example Usage for E5.4.2 (Verification)
# check_username_length = make_validator_factory('min_length', 8)
# check_age_limit = make_validator_factory('max_value', 100)
# check_positive = make_validator_factory('is_positive', 0) 
# 
# try:
#     check_username_length("long_user") # Succeeds
#     check_username_length("short") # Fails
# except ValueError as e:
#     # print(f"Validation failed: {e}")
#     pass


# --- Exercise 5.4.3: Implementing a Configurable Exponential Backoff Retry Decorator ---

def retry(max_attempts, initial_delay=1.0):
    """
    Outermost closure for configuration: max_attempts, initial_delay.
    """
    def decorator(func):
        """
        Middle closure: accepts the function to be decorated.
        """
        # Note: current_attempt must be defined here to be closed over
        # and persist across the wrapper's internal retry loops.
        # However, since the wrapper is called once per decorated function call, 
        # the state must be initialized *inside* the wrapper for each new call.
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            # State variable initialized for *each* execution of the decorated function
            current_attempt = 0 
            
            # Use a loop to handle the retries
            while current_attempt < max_attempts:
                # We do not need `nonlocal` here because `current_attempt` is defined
                # in the immediate scope of the wrapper and is being locally modified.
                # If we had defined it in the 'decorator' scope, we would need `nonlocal`.
                current_attempt += 1
                
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    if current_attempt >= max_attempts:
                        print(f"Attempt {current_attempt}/{max_attempts}: Failed permanently.")
                        raise e
                    
                    # Calculate exponential backoff delay: D = initial_delay * 2^(attempt - 1)
                    delay = initial_delay * (2 ** (current_attempt - 1))
                    
                    print(f"Attempt {current_attempt}/{max_attempts}: Failed with {type(e).__name__}. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
            
        return wrapper
    return decorator

# Example Usage for E5.4.3 (Verification)
# # To test the closure's state management, we must ensure the decorated function
# # can access or manipulate its own state, which is tricky here. 
# # Instead, we rely on the closure to manage the retry loop state (current_attempt).
# 
# call_counter = 0
# @retry(max_attempts=4, initial_delay=0.1)
# def unstable_api_call(data):
#     global call_counter
#     call_counter += 1
#     if call_counter < 3:
#         raise ConnectionError(f"Transient failure {call_counter}.")
#     return f"Success on attempt {call_counter}"
# 
# # try:
# #     result = unstable_api_call("test_request")
# #     print(f"Result: {result}")
# # except Exception as e:
# #     print(f"Final failure: {e}")


# --- Interactive Challenge 5.4.4: Enhancing the Asynchronous Task Manager with Rate Limiting ---

def rate_limiter(limit: int, window: int):
    """
    Asynchronous decorator factory for rate limiting.
    State is managed using a mutable list closed over by the wrapper.
    """
    
    # State: [current_calls, last_reset_time]
    # This state is closed over by the async_wrapper
    state = [0, time.time()] 

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            
            # Use a loop to handle the waiting and re-checking logic
            while True:
                current_time = time.time()
                current_calls, last_reset_time = state
                
                # 1. Check for Window Expiration
                if current_time >= last_reset_time + window:
                    print(f"[{func.__name__}] Window expired. Resetting counter.")
                    state[0] = 0 # Reset calls
                    state[1] = current_time # Reset time
                    current_calls = 0 # Update local variable for immediate check
                
                # 2. Check Limit
                if current_calls < limit:
                    state[0] += 1 # Increment call count
                    print(f"[{func.__name__} Call {state[0]}/{limit}] Executing...")
                    return await func(*args, **kwargs)
                
                # 3. Limit Hit: Calculate sleep duration
                else:
                    sleep_duration = (last_reset_time + window) - current_time
                    if sleep_duration > 0:
                        print(f"[{func.__name__} LIMIT HIT] Max calls ({limit}) reached. Waiting {sleep_duration:.2f}s for window reset.")
                        await asyncio.sleep(sleep_duration)
                        # Loop continues, re-checking the window status immediately after sleep
                    else:
                        # If sleep_duration is zero or negative, the window should have reset,
                        # so we continue the loop to re-evaluate the window expiration check.
                        continue 
        
        return async_wrapper
    return decorator

# Example Usage for E5.4.4 (Verification)

@rate_limiter(limit=3, window=5) # 3 calls every 5 seconds
async def fetch_data(task_id):
    """Simulates an external API call."""
    # print(f"Processing Task {task_id}")
    await asyncio.sleep(0.1) # Simulate network latency
    return f"Data for Task {task_id} retrieved."

async def run_tasks():
    # Schedule 10 tasks concurrently to force the rate limit to be hit quickly
    tasks = [fetch_data(i) for i in range(1, 11)]
    results = await asyncio.gather(*tasks)
    print("\n--- All Tasks Completed ---")

# if __name__ == '__main__':
#     # To run the async example:
#     # print("Starting concurrent tasks...")
#     # asyncio.run(run_tasks())
#     pass


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
import functools
from typing import Callable, Any, Dict, List

# --- 1. Simulated Data and Environment Setup ---

# Simulated user database for authorization checks
USER_DATABASE = {
    "alice": {"role": "admin", "department": "R&D"},
    "bob": {"role": "analyst", "department": "Finance"},
    "charlie": {"role": "guest", "department": "Marketing"}
}

# Global log store for persistent audit trails
AUDIT_LOG: List[Dict[str, Any]] = []

# --- 2. Decorator Factory: Role-Based Access Control (Decorator with Arguments) ---

def role_required(required_role: str) -> Callable:
    """
    A decorator factory that checks if the user calling the function 
    has the specified required_role before execution.
    
    This is the outermost layer, responsible for configuring the requirement.
    """
    print(f"[Factory Setup] Configuring role restriction: {required_role}")

    # The actual decorator function (takes the function to be wrapped)
    def decorator(func: Callable) -> Callable:
        
        # Crucial step: Preserve the original function's metadata and signature
        @functools.wraps(func)
        def wrapper(username: str, *args, **kwargs) -> Any:
            
            # Retrieve user data based on the mandatory 'username' argument
            user_data = USER_DATABASE.get(username)
            
            # Authorization Check Logic
            if not user_data:
                raise PermissionError(f"User '{username}' not found in database.")
            
            user_role = user_data.get("role")
            
            # Core security check
            if user_role != required_role:
                log_entry = {
                    "timestamp": time.time(),
                    "function": func.__name__,
                    "status": "DENIED",
                    "user": username,
                    "reason": f"Required role '{required_role}', but user has '{user_role}'"
                }
                AUDIT_LOG.append(log_entry)
                raise PermissionError(
                    f"Access denied for {username}. Role must be '{required_role}'."
                )

            # If authorized, execute the original function (or the next wrapped function)
            print(f"[Auth] Access granted for {username} ({user_role}). Executing {func.__name__}...")
            # Pass all arguments, including the username, through to the core function
            return func(username, *args, **kwargs)

        return wrapper
    return decorator

# --- 3. Standard Decorator: Performance and Input/Output Logging ---

def performance_logger(func: Callable) -> Callable:
    """
    Logs the execution time, arguments, and return value of the decorated function.
    This decorator must handle arbitrary arguments (*args, **kwargs).
    """
    @functools.wraps(func)
    def wrapper(username: str, *args, **kwargs) -> Any:
        start_time = time.perf_counter()
        
        # Capture input parameters for the audit trail
        input_log = {
            "positional_args": args,
            "keyword_args": kwargs
        }
        
        try:
            # Execute the function, correctly passing all arguments received by the wrapper
            result = func(username, *args, **kwargs)
            
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000 # Convert to milliseconds

            # Log success details
            log_entry = {
                "timestamp": time.time(),
                "function": func.__name__,
                "status": "SUCCESS",
                "user": username,
                "duration_ms": f"{duration:.2f}",
                "input": input_log,
                # Summarize output to prevent excessive log size
                "output_summary": str(result)[:50] + ("..." if len(str(result)) > 50 else "")
            }
            AUDIT_LOG.append(log_entry)
            
            return result
        
        except Exception as e:
            # Log failure details (e.g., if the core function raises a ValueError)
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000
            
            log_entry = {
                "timestamp": time.time(),
                "function": func.__name__,
                "status": "FAILURE",
                "user": username,
                "duration_ms": f"{duration:.2f}",
                "error": str(e)
            }
            AUDIT_LOG.append(log_entry)
            # Re-raise the exception so the calling code knows the operation failed
            raise 

    return wrapper

# --- 4. Application Functions (Applying Multiple Decorators) ---

# Decorator stacking order: performance_logger wraps the result of role_required("admin")
@performance_logger
@role_required("admin")
def process_critical_data(username: str, dataset_id: int, config: Dict[str, Any]) -> str:
    """Simulates a secure, time-intensive administrative task."""
    time.sleep(0.05) # Simulate processing time
    if dataset_id % 2 != 0:
        # Application logic failure
        raise ValueError("Critical data processing requires an even dataset ID.")
    
    output = f"Dataset {dataset_id} processed successfully by {username}. Config mode: {config.get('mode')}"
    return output

@performance_logger
@role_required("analyst")
def generate_report(username: str, start_date: str, end_date: str) -> List[str]:
    """Simulates a standard analytical task."""
    time.sleep(0.01)
    report_data = [
        f"Report generated by {username}: Q4 Financial Data (100 records)",
        f"Dates covered: {start_date} to {end_date}"
    ]
    return report_data

# --- 5. Execution and Demonstration ---

def run_demonstration():
    print("--- 1. Analyst attempting report generation (SUCCESS expected) ---")
    try:
        report = generate_report("bob", "2023-10-01", "2023-12-31")
        print(f"Result Summary: {report[0]}\n")
    except Exception as e:
        print(f"Execution Error: {e}\n")

    print("--- 2. Admin attempting critical data processing (SUCCESS, then APPLICATION FAILURE) ---")
    try:
        # Success case (even ID)
        admin_output = process_critical_data("alice", 42, {"mode": "secure_write"})
        print(f"Result Summary: {admin_output}\n")
        
        # Failure case (odd ID, triggers ValueError inside the core function)
        process_critical_data("alice", 43, {"mode": "secure_write"})
        
    except Exception as e:
        # This catches the ValueError raised by the core function, which was logged by the decorator
        print(f"Execution Error Caught: {e}\n")

    print("--- 3. Guest attempting admin task (PERMISSION DENIED expected) ---")
    try:
        process_critical_data("charlie", 10, {"mode": "test"})
    except Exception as e:
        # This catches the PermissionError raised by the role_required decorator
        print(f"Execution Error Caught: {e}\n")

    print("\n--- 4. Final Audit Log Summary ---")
    # Display the collected logs
    for i, log in enumerate(AUDIT_LOG):
        status = log['status']
        func = log['function']
        user = log.get('user', 'N/A')
        
        detail = ""
        if status == "SUCCESS":
            detail = f"Duration: {log['duration_ms']}ms | Output: {log['output_summary']}"
        elif status == "FAILURE":
            detail = f"Error: {log['error']}"
        elif status == "DENIED":
            detail = f"Reason: {log['reason']}"
            
        print(f"[{i+1}] Status: {status:<7} | Func: {func:<25} | User: {user:<8} | {detail}")

if __name__ == "__main__":
    run_demonstration()

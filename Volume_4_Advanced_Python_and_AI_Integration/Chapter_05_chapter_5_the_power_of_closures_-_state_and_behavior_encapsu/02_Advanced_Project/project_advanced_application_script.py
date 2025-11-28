
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

import datetime
import time
from typing import Callable, Tuple, Dict, Any

# Define severity levels for clear configuration
SEVERITY_LEVELS = {
    "DEBUG": 1,
    "INFO": 2,
    "WARNING": 3,
    "ERROR": 4,
    "CRITICAL": 5
}

# Define the type hint for the returned tuple for clarity
AuditorTuple = Tuple[Callable[[str, str], str], Callable[[], Dict[str, Any]]]

def create_module_auditor(module_name: str, min_severity_level: int) -> AuditorTuple:
    """
    Function factory that creates a stateful auditor closure pair.
    
    The enclosing scope holds the state (message_count, last_log_timestamp)
    which is unique to the specific module auditor instance created.
    """
    # 1. Enclosing scope variables (the state retained by the closures)
    message_count = 0
    last_log_timestamp = None
    
    print(f"[Auditor Factory] Initializing auditor for '{module_name}'. Min Level: {min_severity_level}")

    def log_message(severity: str, message: str) -> str:
        """
        The primary closure function. It accesses and modifies the state 
        variables from the enclosing scope using 'nonlocal'.
        """
        nonlocal message_count, last_log_timestamp 
        
        current_time = datetime.datetime.now()
        severity_value = SEVERITY_LEVELS.get(severity.upper(), 0)

        # 2. Check configuration (min_severity_level is retained from factory arguments)
        if severity_value < min_severity_level:
            return f"[{module_name}] Filtered: {severity} message below threshold ({min_severity_level})."

        # 3. Update state variables using nonlocal binding
        message_count += 1
        
        # Calculate time difference since last log
        time_diff = None
        if last_log_timestamp:
            time_diff = current_time - last_log_timestamp
        
        last_log_timestamp = current_time
        
        # Format the log output
        log_entry = (
            f"[{module_name}][{severity.upper()}] "
            f"Msg #{message_count}: {message}"
        )
        
        if time_diff:
            log_entry += f" (Delta: {time_diff.total_seconds():.3f}s)"
        
        return log_entry

    def get_audit_summary() -> Dict[str, Any]:
        """
        A secondary closure function returned by the factory to expose the 
        internal state without allowing modification via this getter.
        """
        # This function also accesses the same retained state variables
        return {
            "module": module_name,
            "total_messages_logged": message_count,
            "last_logged_time": last_log_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f") if last_log_timestamp else "N/A",
            "min_level_config": min_severity_level
        }

    # Return the two closures
    return log_message, get_audit_summary

# --- Application Simulation ---

# 4. Create specialized auditors using the factory
# DB Auditor: Only logs WARNINGs and above (Level 3)
db_logger, db_summary = create_module_auditor("Database_ORM", SEVERITY_LEVELS["WARNING"])

# Network Auditor: Logs everything (Level 1)
net_logger, net_summary = create_module_auditor("Network_API", SEVERITY_LEVELS["DEBUG"])

print("\n--- Running Database Audit Simulation ---")
# This INFO message is filtered by the DB auditor's configured threshold (Level 3)
print(db_logger("INFO", "Attempting connection pool initialization.")) 
time.sleep(0.15)
# This WARNING message is logged (Msg #1)
print(db_logger("WARNING", "Slow query detected on user table.")) 
time.sleep(0.45)
# This CRITICAL message is logged (Msg #2)
print(db_logger("CRITICAL", "Transaction commit failed due to lock timeout.")) 

print("\n--- Running Network Audit Simulation ---")
# All messages are logged for the Network auditor (Level 1 threshold)
print(net_logger("DEBUG", "Pinging external service endpoint.")) # Logged (Msg #1)
time.sleep(0.1)
print(net_logger("INFO", "Successful handshake established.")) # Logged (Msg #2)
print(net_logger("INFO", "Sending 500 records payload.")) # Logged (Msg #3)
time.sleep(0.05)
print(net_logger("DEBUG", "Closing socket connection.")) # Logged (Msg #4)

print("\n--- Final State Summaries (Inspecting Retained State) ---")
# 5. Accessing the encapsulated state via the summary closure
print("DB State:", db_summary())
print("NET State:", net_summary())

print("\nVerification Check:")
# The DB auditor still filters low-severity messages, retaining its configuration
print(db_logger("DEBUG", "This should never appear."))
# The NET auditor continues its count
print(net_logger("ERROR", "External service returned 500."))

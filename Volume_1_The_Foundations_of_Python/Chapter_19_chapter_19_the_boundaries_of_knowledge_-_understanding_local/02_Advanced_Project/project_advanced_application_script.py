
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

# ----------------------------------------------------------------------
# RAG System Performance Tracker: Demonstrating Global State Management
# ----------------------------------------------------------------------

# Global Scope Variables: These define the initial, authoritative state 
# of the system (Adhering to the DRY Principle for configuration).
RAG_SYSTEM_NAME = "Knowledge_Augmentor_V2"
TOTAL_QUERIES_PROCESSED = 0
SUCCESSFUL_QUERIES = 0
GLOBAL_LATENCY_SUM = 0.0

# Configuration settings (intended to be read-only globally)
DEFAULT_TEMPERATURE = 0.75
MAX_TOKENS = 256

# --- Helper Function (Purely Local) ---

def _simulate_processing_time(query_length):
    """Calculates simulated latency based on query complexity."""
    # All variables defined here (base_time, complexity_factor, simulated_latency) 
    # are strictly local to this function and vanish upon return.
    base_time = 0.15
    complexity_factor = query_length / 50.0
    simulated_latency = base_time + complexity_factor
    return simulated_latency

# --- Core Logic Function 1: Configuration Loading (Demonstrates Shadowing) ---

def load_configuration():
    """Reads global config and demonstrates variable shadowing."""
    
    print(f"\n[1] Initializing System: {RAG_SYSTEM_NAME} (Global Read)")
    print("-" * 40)
    
    # Python reads RAG_SYSTEM_NAME and MAX_TOKENS from the global scope 
    # because they are not defined locally.
    print(f"  > Max Tokens Allowed: {MAX_TOKENS} (Global Read)")
    
    # Variable shadowing: We define a local variable named DEFAULT_TEMPERATURE.
    # This creates a NEW variable in the local scope, hiding the global one 
    # for the duration of this function's execution.
    DEFAULT_TEMPERATURE = 0.85 # This is a local variable assignment.
    
    print(f"  > Loaded Config Temp: {DEFAULT_TEMPERATURE} (Local Shadow Value)")
    
    # The global DEFAULT_TEMPERATURE (0.75) remains unchanged outside this function.
    return DEFAULT_TEMPERATURE # Return the local shadowed value for context

# --- Core Logic Function 2: Query Processing (CRITICAL: Demonstrates 'global' keyword) ---

def process_query(query, expected_success=True):
    """Processes a query and explicitly updates global performance metrics."""
    
    # CRITICAL: These declarations tell Python NOT to create new local variables 
    # but to link these names directly to the existing global variables defined 
    # outside the function. This allows for mutation of the global state.
    global TOTAL_QUERIES_PROCESSED
    global SUCCESSFUL_QUERIES
    global GLOBAL_LATENCY_SUM
    
    # Local scope variables for calculation
    query_length = len(query)
    latency = _simulate_processing_time(query_length)
    
    # 1. Update total count (Global modification)
    TOTAL_QUERIES_PROCESSED += 1
    
    # 2. Update latency sum (Global modification)
    GLOBAL_LATENCY_SUM += latency
    
    # 3. Conditional success update (Global modification)
    if expected_success and latency < 1.0:
        SUCCESSFUL_QUERIES += 1
        status = "Success" # Local variable
    else:
        status = "Failure (High Latency/Error)" # Local variable
        
    print(f"  > Query '{query[:15]}...' | Length: {query_length} | Latency: {latency:.3f}s | Status: {status}")
    
# --- Core Logic Function 3: Reporting (Demonstrates Reading Final Global State) ---

def display_report():
    """Calculates and prints the final performance report based on modified global state."""
    print("\n[3] Final Performance Report")
    print("-" * 40)
    
    # Accessing the globally modified variables
    total = TOTAL_QUERIES_PROCESSED
    success = SUCCESSFUL_QUERIES
    
    # Local calculation: derived metric
    avg_latency = GLOBAL_LATENCY_SUM / total if total > 0 else 0.0
    success_rate = (success / total) * 100 if total > 0 else 0.0
    
    # Local variable definition: standard check
    DRY_PRINCIPLE_CHECK = "Passed"
    
    print(f"  System: {RAG_SYSTEM_NAME}")
    print(f"  Total Queries Processed: {total}")
    print(f"  Successful Queries: {success}")
    print(f"  Success Rate: {success_rate:.2f}%")
    print(f"  Average Latency: {avg_latency:.3f} seconds")
    print(f"  Design Principle Check: {DRY_PRINCIPLE_CHECK}") # Local variable
    
    # Final Sanity Check: Prove the global DEFAULT_TEMPERATURE was never changed 
    # by the shadowing in load_configuration().
    print(f"\n  [Scope Check] Original Global Temperature: {DEFAULT_TEMPERATURE}")


# ----------------------------------------------------------------------
# Main Execution Flow
# ----------------------------------------------------------------------

if __name__ == "__main__":
    
    # Phase 1: Configuration Loading (Demonstrates Shadowing)
    local_temp = load_configuration()
    
    # Proof of concept: Comparing the global variable to the value returned 
    # from the function's local scope.
    print(f"  [Scope Check] Global Temperature (after load_config): {DEFAULT_TEMPERATURE}")
    print(f"  [Scope Check] Local Temperature returned from function: {local_temp}")
    
    # Phase 2: Processing Queries (Demonstrates 'global' keyword modification)
    print("\n[2] Processing Live Queries")
    print("-" * 40)
    
    # Simulate various queries, triggering global state updates
    process_query("What is Retrieval Augmented Generation?", expected_success=True)
    process_query("Explain the Principle of DRY in Python software engineering.", expected_success=True)
    process_query("Write a 500-word essay on the history of LLMs and their integration into modern cloud infrastructure.", expected_success=False) # Long query, simulated failure
    process_query("How does the global keyword affect variable scope?", expected_success=True)
    process_query("Define Context Processor in web frameworks.", expected_success=True)
    
    # Phase 3: Reporting (Demonstrates reading modified global state)
    display_report()

# ----------------------------------------------------------------------
# End of Script
# ----------------------------------------------------------------------

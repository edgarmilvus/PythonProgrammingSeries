
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

import asyncio
import time
import random
import uuid
from contextvars import ContextVar
from typing import List, Union, Any

# --- Exercise 8.4.2 Custom Exception ---
class ProcessingError(Exception):
    """Custom exception for failed record processing."""
    pass

# --- Exercise 8.4.3 Context Variable Definition ---
# Define the Context Variable for request tracking
REQUEST_ID = ContextVar('request_id', default='N/A')

# ==============================================================================
# Exercise 8.4.1: High-Throughput API Gateway Simulation
# ==============================================================================

async def fetch_service_data(service_id: int, latency: float) -> str:
    """Simulates fetching data from a microservice."""
    start_time = time.perf_counter()
    await asyncio.sleep(latency)
    elapsed = time.perf_counter() - start_time
    # Note: elapsed will be close to latency, but slightly higher due to overhead
    return f"Service {service_id} fetched in {elapsed:.4f}s (Target: {latency:.4f}s)"

async def main_concurrent(tasks_data: List[tuple]) -> None:
    print("\n--- Running 8.4.1 Concurrent (asyncio.gather) ---")
    start_time = time.perf_counter()
    
    tasks = []
    for service_id, latency in tasks_data:
        tasks.append(fetch_service_data(service_id, latency))
        
    # Execute all tasks simultaneously
    results = await asyncio.gather(*tasks)
    
    end_time = time.perf_counter()
    total_time = end_time - start_time
    
    print(f"Concurrent Execution Time: {total_time:.4f} seconds")
    # Uncomment below to see individual results:
    # for result in results:
    #     print(f"  [C] {result}")

async def main_sequential(tasks_data: List[tuple]) -> None:
    print("\n--- Running 8.4.1 Sequential ---")
    start_time = time.perf_counter()
    
    # Execute tasks one after the other
    for service_id, latency in tasks_data:
        # Await is called inside the loop, forcing sequential execution
        await fetch_service_data(service_id, latency)
        
    end_time = time.perf_counter()
    total_time = end_time - start_time
    
    print(f"Sequential Execution Time: {total_time:.4f} seconds")

async def run_841():
    # 10 tasks with random latencies
    tasks_data = [
        (i + 1, random.uniform(0.1, 1.5)) for i in range(10)
    ]
    
    await main_concurrent(tasks_data)
    await main_sequential(tasks_data)
    print("\nComparison: Concurrent time should be close to the maximum single task latency.")


# ==============================================================================
# Exercise 8.4.2: Resilient Batch Processing
# ==============================================================================

async def process_record(record_id: int, should_fail: bool) -> str:
    """Processes a record, raising an exception if configured."""
    if should_fail:
        print(f"  [FAIL] Record {record_id} intentionally failing...")
        await asyncio.sleep(0.1) # Simulate a small delay before failure
        raise ProcessingError(f"Record {record_id} is corrupted or invalid.")
    
    # Simulate successful processing
    await asyncio.sleep(0.5)
    return f"Record {record_id} successfully processed."

async def run_842():
    print("\n--- Running 8.4.2 Resilient Batch Processing ---")
    
    # Create 15 tasks, ensuring 5 fail (records 3, 6, 9, 12, 15)
    tasks_config = []
    for i in range(1, 16):
        is_fail = (i % 3 == 0)
        tasks_config.append(process_record(i, is_fail))
        
    # Execute using gather with return_exceptions=True
    # The result list will contain either strings (success) or Exception objects (failure)
    results: List[Union[str, ProcessingError]] = await asyncio.gather(
        *tasks_config,
        return_exceptions=True
    )
    
    successful_count = 0
    failed_count = 0
    
    print("\n--- Batch Processing Summary ---")
    print(f"Total tasks attempted: {len(results)}")
    
    for result in results:
        if isinstance(result, Exception):
            failed_count += 1
            print(f"  [FAILURE] Task Failed (Type: {type(result).__name__}): {result}")
        elif isinstance(result, str):
            successful_count += 1
            print(f"  [SUCCESS] {result}")

    print(f"\nReport: {successful_count} successful, {failed_count} failed.")


# ==============================================================================
# Exercise 8.4.3: Interactive Challenge - Parallel State Management
# ==============================================================================

async def analyze_document(doc_name: str, delay: float) -> str:
    """Analyzes a document, retrieving the REQUEST_ID from contextvars."""
    
    # Retrieve the state bound to the current task's context
    try:
        current_request_id = REQUEST_ID.get()
    except LookupError:
        current_request_id = "CONTEXT NOT FOUND"
    
    print(f"  [Task {doc_name}] Starting analysis. Request ID: {current_request_id[:8]}...")
    await asyncio.sleep(delay)
    
    return f"Document '{doc_name}' analysis complete. Used Request ID: {current_request_id}"

async def run_843():
    print("\n--- Running 8.4.3 Parallel State Management (contextvars) ---")
    
    # 1. Generate a unique ID for this entire parallel operation
    session_uuid = str(uuid.uuid4())
    print(f"Generated Global Session ID: {session_uuid}")

    # 2. Bind the ID to the current execution context. This token is used for cleanup.
    token = REQUEST_ID.set(session_uuid)

    try:
        # 3. Create parallel tasks (these tasks inherit the current context)
        tasks = [
            analyze_document("Document A (1.2s)", 1.2),
            analyze_document("Document B (0.5s)", 0.5),
            analyze_document("Document C (1.8s)", 1.8),
        ]

        # 4. Execute using asyncio.gather
        results = await asyncio.gather(*tasks)

        # 5. Verify results
        print("\n--- Verification ---")
        for result in results:
            print(f"  {result}")
            # Check if the retrieved ID matches the global session ID
            if session_uuid not in result:
                raise RuntimeError("Context variable leakage or failure detected!")
        
        print("\nVerification successful: All parallel tasks inherited the correct Request ID via contextvars.")

    finally:
        # 6. Crucial cleanup: reset the context variable to its previous value (or default)
        REQUEST_ID.reset(token)
        print("Context variable reset.")


# ==============================================================================
# Exercise 8.4.4: Enforcing Structured Concurrency with Timeout
# ==============================================================================

async def fetch_data_source(source_name: str, required_time: float) -> str:
    """Fetches data, handling cancellation gracefully."""
    print(f"  [Source {source_name}] Starting fetch (expecting {required_time}s)...")
    try:
        # This sleep is the point where cancellation will occur if timeout hits
        await asyncio.sleep(required_time)
        return f"Source {source_name} data fetched successfully."
    except asyncio.CancelledError:
        # Structured cleanup required upon cancellation
        print(f"  [Source {source_name}] Timeout detected. Initiating cleanup and resource release.")
        # Simulate cleanup work
        await asyncio.sleep(0.1) 
        print(f"  [Source {source_name}] Cleanup complete.")
        # Re-raise the cancellation error to propagate the structured shutdown
        raise

async def run_844():
    print("\n--- Running 8.4.4 Structured Concurrency with Timeout ---")
    
    # Tasks setup (C is too long for the 3.0s timeout)
    tasks = [
        fetch_data_source("A", 1.0),
        fetch_data_source("B", 2.0),
        fetch_data_source("C", 5.0),
    ]
    
    try:
        print("Attempting to gather tasks with a 3.0 second timeout...")
        # Wrap gather in wait_for. wait_for handles the cancellation of the underlying tasks.
        results = await asyncio.wait_for(
            asyncio.gather(*tasks),
            timeout=3.0
        )
        print("\nGather completed successfully.")
        for result in results:
            print(f"  [Result] {result}")

    except asyncio.TimeoutError:
        print("\n!!! TIMEOUT DETECTED !!!")
        print("The overall operation exceeded 3.0 seconds.")
        print("Tasks A and B should have finished. Task C was cancelled mid-sleep.")
        print("Verify console output for 'Cleanup complete' messages from cancelled tasks.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# ==============================================================================
# Main Execution Block
# ==============================================================================

async def main():
    await run_841()
    await run_842()
    await run_843()
    await run_844()

if __name__ == "__main__":
    # Note: Running all exercises sequentially in the main loop for clarity
    asyncio.run(main())


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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

import asyncio
import time
from typing import List, Awaitable

# --- 1. The Core Asynchronous Worker ---

async def simulate_fetch(item_name: str, delay_seconds: float) -> str:
    """
    Simulates an I/O bound task (like an API call or database query).
    The function pauses execution for the specified duration using await asyncio.sleep.
    """
    # Record the start time for visualization
    start_time = time.monotonic() 
    
    print(f"[{time.strftime('%H:%M:%S', time.localtime())}] Task '{item_name}': Starting fetch (Delay: {delay_seconds:.1f}s)...")
    
    # Crucial: Yield control back to the event loop
    await asyncio.sleep(delay_seconds)
    
    end_time = time.monotonic()
    duration = end_time - start_time
    
    print(f"[{time.strftime('%H:%M:%S', time.localtime())}] Task '{item_name}': Finished. Duration: {duration:.2f}s.")
    
    return f"Result for {item_name} (Slept for {delay_seconds:.1f}s)"

# --- 2. Sequential Execution (The Inefficient Baseline) ---

async def sequential_execution():
    """
    Runs three tasks one after the other. The total time is additive.
    """
    print("\n" + "="*50)
    print("--- Starting Sequential Execution ---")
    print("="*50)
    start_time = time.monotonic()

    # Task 1 must complete before Task 2 starts
    result_a = await simulate_fetch("User Profile", 2.0)
    
    # Task 2 must complete before Task 3 starts
    result_b = await simulate_fetch("Order History", 1.5)
    
    # Task 3 executes last
    result_c = await simulate_fetch("Notification Log", 1.0)

    end_time = time.monotonic()
    total_time = end_time - start_time
    
    print("\n--- Sequential Summary ---")
    print(f"Results: [{result_a}, {result_b}, {result_c}]")
    print(f"Total Sequential Time: {total_time:.2f} seconds.")
    print("Expected Time (Additive): 2.0 + 1.5 + 1.0 = 4.5 seconds.")


# --- 3. Concurrent Execution using asyncio.gather ---

async def concurrent_execution():
    """
    Runs the same three tasks simultaneously using asyncio.gather.
    The total time is determined by the longest running task (2.0 seconds).
    """
    print("\n" + "="*50)
    print("--- Starting Concurrent Execution (using gather) ---")
    print("="*50)
    start_time = time.monotonic()

    # A list of coroutine objects (Awaitables) is created.
    # Note: We are defining the calls here, but not running them yet.
    tasks: List[Awaitable[str]] = [
        simulate_fetch("User Profile", 2.0),
        simulate_fetch("Order History", 1.5),
        simulate_fetch("Notification Log", 1.0),
    ]

    # asyncio.gather takes multiple Awaitables (or Tasks/Futures) as positional arguments.
    # The '*' operator unpacks the 'tasks' list into individual arguments.
    concurrent_results: List[str] = await asyncio.gather(*tasks)

    end_time = time.monotonic()
    total_time = end_time - start_time
    
    print("\n--- Concurrent Summary ---")
    # gather guarantees that the results are returned in the same order as the input coroutines.
    print(f"Results: {concurrent_results}")
    print(f"Total Concurrent Time: {total_time:.2f} seconds.")
    print("Expected Time (Max Task): 2.0 seconds.")


# --- 4. Main Runner ---

def main():
    # Execute the sequential benchmark first
    asyncio.run(sequential_execution())

    # Execute the concurrent benchmark second
    asyncio.run(concurrent_execution())

if __name__ == "__main__":
    main()

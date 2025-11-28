
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
from typing import Awaitable, Any

# --- 1. Define the Coroutine Function ---

async def fetch_data(task_name: str, delay: int) -> str:
    """
    A coroutine that simulates an I/O-bound operation.
    
    The 'async def' keyword marks this function as a coroutine, meaning 
    it can be scheduled and paused by the event loop.
    """
    start_time = time.perf_counter()
    print(f"[{task_name}] Starting fetch. Will require {delay} seconds of waiting.")
    
    # The 'await' keyword is the heart of asyncio. 
    # When this line is executed, the coroutine yields control 
    # back to the event loop, allowing other scheduled tasks to run.
    await asyncio.sleep(delay) 
    
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"[{task_name}] Finished fetch. Actual elapsed time: {elapsed:.2f}s")
    
    # The return value is what the caller (e.g., asyncio.gather) will receive.
    return f"Data result for {task_name}"

# --- 2. Define the Main Orchestrator Coroutine ---

async def main() -> None:
    """
    The top-level coroutine responsible for creating and orchestrating tasks.
    """
    print("--- Initiating Asynchronous Tasks Orchestration ---")
    
    # 2a. Create Coroutine Objects
    # These calls return coroutine objects; execution has NOT started yet.
    task_a_coroutine: Awaitable[str] = fetch_data("LLM Config Service", 3)
    task_b_coroutine: Awaitable[str] = fetch_data("User Profile DB", 2)
    
    # 2b. Schedule and Wait Concurrently
    # asyncio.gather wraps the coroutine objects into Task objects and 
    # schedules them on the event loop simultaneously. The 'await' here 
    # means 'wait until all gathered tasks are complete'.
    results: list[str] = await asyncio.gather(
        task_a_coroutine,
        task_b_coroutine
    )
    
    print("\n--- All Tasks Complete. Processing Results ---")
    for result in results:
        print(f"-> Retrieved: {result}")
        
# --- 3. Entry Point and Event Loop Management ---

if __name__ == "__main__":
    # Record the overall start time for performance comparison.
    overall_start = time.perf_counter()
    
    # asyncio.run() is the primary function used to run the top-level 
    # coroutine (main()) and manage the entire event loop lifecycle.
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    
    overall_end = time.perf_counter()
    total_runtime = overall_end - overall_start
    
    # The runtime should approximate the maximum delay (3s), not the sum (5s).
    print(f"\nTotal Program Runtime: {total_runtime:.2f} seconds.")


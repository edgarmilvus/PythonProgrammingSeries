
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
from typing import Awaitable, Coroutine

# 1. Define a coroutine function using 'async def'
async def fetch_data(delay: float, name: str) -> str:
    """
    Simulates a long-running, non-CPU-bound I/O operation.
    """
    print(f"[{name}] Starting data fetch (simulated I/O wait for {delay}s)...")
    
    # 2. Use 'await' to cooperatively pause execution and yield control.
    # The current coroutine (fetch_data) is suspended, and the event loop
    # is free to run other tasks until the sleep timer expires.
    await asyncio.sleep(delay)
    
    print(f"[{name}] Data fetch complete.")
    return f"Result for {name} retrieved successfully after {delay}s"

# 3. Define the primary entry point coroutine
async def main() -> None:
    """
    The orchestrator coroutine that schedules and awaits sub-tasks.
    """
    start_time = time.perf_counter()
    print("--- Starting Asynchronous Execution ---")
    
    # 4. Await the first coroutine call.
    # Execution pauses here until Task A finishes its simulated wait.
    result_A = await fetch_data(1.5, "Task A")
    
    # 5. Await the second coroutine call.
    # This task only starts after Task A has fully completed and resumed.
    result_B = await fetch_data(0.5, "Task B")
    
    end_time = time.perf_counter()
    
    print("\n--- Execution Summary ---")
    print(f"Task A Result: {result_A}")
    print(f"Task B Result: {result_B}")
    print(f"Total Wall Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # 6. The synchronous entry point to start the asyncio event loop.
    print("Initializing Asynchronous Runtime...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    print("Asynchronous Runtime finished.")


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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

import asyncio
import time
from typing import Dict, Any

# --- Exercise 7.4.1: The Asynchronous Resource Fetcher ---

async def fetch_resource(resource_name: str, latency: float) -> str:
    """
    Simulates fetching a resource with a specified latency using cooperative sleep.
    """
    start_time = time.time()
    print(f"[{start_time:.2f}] {resource_name}: Starting fetch (Latency: {latency}s)...")
    
    # Cooperative yielding: control is returned to the event loop
    await asyncio.sleep(latency)
    
    end_time = time.time()
    print(f"[{end_time:.2f}] {resource_name}: Fetch completed. Total time: {end_time - start_time:.2f}s")
    
    return f"{resource_name} Status: SUCCESS"

async def main_fetcher():
    """
    Sequentially awaits the fetching of three resources.
    """
    print("\n--- Running Exercise 7.4.1: Sequential Fetcher ---")
    
    # Await 1: Resource A
    result_a = await fetch_resource("Resource A", 2.5)
    print(f"Result A: {result_a}")
    
    # Await 2: Resource B
    result_b = await fetch_resource("Resource B", 1.0)
    print(f"Result B: {result_b}")
    
    # Await 3: Resource C
    result_c = await fetch_resource("Resource C", 1.8)
    print(f"Result C: {result_c}")

# --- Exercise 7.4.2: Cooperative State Transition Pipeline ---

async def validate_data(item_id: int):
    """Simulates data validation I/O (0.5s)."""
    print(f"[{time.time():.2f}] Item {item_id} | Validation: Starting (0.5s)")
    await asyncio.sleep(0.5)
    print(f"[{time.time():.2f}] Item {item_id} | Validation: Finished")

async def transform_data(item_id: int):
    """Simulates data transformation I/O (1.0s)."""
    print(f"[{time.time():.2f}] Item {item_id} | Transformation: Starting (1.0s)")
    await asyncio.sleep(1.0)
    print(f"[{time.time():.2f}] Item {item_id} | Transformation: Finished")

async def persist_data(item_id: int):
    """Simulates data persistence I/O (0.2s)."""
    print(f"[{time.time():.2f}] Item {item_id} | Persistence: Starting (0.2s)")
    await asyncio.sleep(0.2)
    print(f"[{time.time():.2f}] Item {item_id} | Persistence: Finished")

async def run_pipeline(item_id: int):
    """
    Runs the three stages sequentially for a single item.
    """
    print(f"\n--- Starting Pipeline for Item {item_id} ---")
    
    # Await ensures sequential completion
    await validate_data(item_id)
    await transform_data(item_id)
    await persist_data(item_id)
    
    print(f"--- Pipeline Finished for Item {item_id} ---")

async def main_pipeline():
    """
    Executes two pipeline runs sequentially.
    """
    print("\n--- Running Exercise 7.4.2: Cooperative Pipeline ---")
    
    # Item 101 must fully complete before Item 102 begins.
    await run_pipeline(101)
    await run_pipeline(102)

# --- Exercise 7.4.3: Asynchronous Configuration Aggregator ---

async def fetch_default_config() -> Dict[str, Any]:
    """Fetches default configuration settings (1.0s delay)."""
    print(f"[{time.time():.2f}] Fetching defaults...")
    await asyncio.sleep(1.0)
    defaults = {'theme': 'dark', 'timeout': 30, 'log_level': 'INFO', 'port': 8080}
    print(f"[{time.time():.2f}] Defaults fetched.")
    return defaults

async def fetch_user_overrides() -> Dict[str, Any]:
    """Fetches user-specific overrides (0.5s delay)."""
    print(f"[{time.time():.2f}] Fetching overrides...")
    await asyncio.sleep(0.5)
    overrides = {'theme': 'light', 'timeout': 60, 'port': 9000}
    print(f"[{time.time():.2f}] Overrides fetched.")
    return overrides

async def aggregate_config() -> Dict[str, Any]:
    """
    Awaits configuration sources and merges them using dict.update().
    """
    print("\n--- Running Exercise 7.4.3: Configuration Aggregator ---")
    
    # Await and retrieve the return value of the coroutines
    default_config = await fetch_default_config()
    user_config = await fetch_user_overrides()
    
    # Merge the configurations. Overrides take precedence.
    final_config = default_config.copy()
    
    # The dict.update() method merges the user_config into final_config, 
    # overwriting shared keys.
    final_config.update(user_config)
    
    return final_config

# --- Exercise 7.4.4: Interactive Challenge Refactoring ---

async def async_io_task(task_id: int, duration: float) -> str:
    """
    Asynchronous worker simulating I/O latency using cooperative sleep.
    """
    start_time = time.time()
    print(f"[{start_time:.2f}] Task {task_id}: Starting asynchronous operation.")
    
    # Replace blocking time.sleep with cooperative await asyncio.sleep
    await asyncio.sleep(duration)
    
    end_time = time.time()
    print(f"[{end_time:.2f}] Task {task_id}: Asynchronous operation finished.")
    return f"Result of Task {task_id} (Duration: {duration}s)"

async def main_async():
    """
    Asynchronous main function enforcing sequential execution using await.
    """
    print("\n--- Running Exercise 7.4.4: Refactored Asynchronous Main ---")
    start = time.time()
    results = []
    
    # Sequential execution enforced by await
    results.append(await async_io_task(1, 1.5))
    results.append(await async_io_task(2, 2.0))
    results.append(await async_io_task(3, 0.5))
    
    total_time = time.time() - start
    print(f"\nAll tasks completed.")
    print(f"Total sequential asynchronous time: {total_time:.2f}s (Expected: 4.0s)")
    print(f"Collected results: {results}")
    return results

# --- Execution Block ---

if __name__ == "__main__":
    # Exercise 7.4.1 Execution
    asyncio.run(main_fetcher())
    
    # Exercise 7.4.2 Execution
    asyncio.run(main_pipeline())
    
    # Exercise 7.4.3 Execution
    final_config = asyncio.run(aggregate_config())
    print(f"\nFinal Merged Configuration:\n{final_config}")

    # Exercise 7.4.4 Execution (Refactoring Challenge)
    asyncio.run(main_async())


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
from typing import Dict, Any

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
    
    # Await 1: Resource A (2.5s)
    result_a = await fetch_resource("Resource A", 2.5)
    print(f"Result A: {result_a}")
    
    # Await 2: Resource B (1.0s)
    result_b = await fetch_resource("Resource B", 1.0)
    print(f"Result B: {result_b}")
    
    # Await 3: Resource C (1.8s)
    result_c = await fetch_resource("Resource C", 1.8)
    print(f"Result C: {result_c}")

# Execution (placed in the final block)
# asyncio.run(main_fetcher())

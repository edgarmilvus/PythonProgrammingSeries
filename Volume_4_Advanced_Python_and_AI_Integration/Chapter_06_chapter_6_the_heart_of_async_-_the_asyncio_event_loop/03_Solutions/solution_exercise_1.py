
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
from typing import List, Awaitable, Tuple, Set

# --- Custom Exception for Exercise 6.4.4 ---
class LLMAPIError(Exception):
    """Custom exception simulating an API failure during an LLM call."""
    pass

# --- Core Coroutine Definition ---
async def simulated_fetch(doc_id: str, delay: float) -> str:
    """Simulates fetching a document over a network."""
    print(f"[{doc_id}] STARTING fetch. Expected delay: {delay:.1f}s")
    
    # Cooperative multitasking yield point
    await asyncio.sleep(delay)
    
    print(f"[{doc_id}] COMPLETED fetch.")
    return f"Document {doc_id} retrieved in {delay:.1f}s"

# --- Exercise 6.4.1 Implementations ---

async def run_sequential():
    """Executes tasks one after the other, demonstrating blocking."""
    print("\n--- 6.4.1: Starting Sequential Run ---")
    
    # Sequential execution: 3s + 2s + 1s = 6 seconds total
    await simulated_fetch("Doc A (3s)", 3.0)
    await simulated_fetch("Doc B (2s)", 2.0)
    await simulated_fetch("Doc C (1s)", 1.0)
    
    print("--- 6.4.1: Sequential Run Finished ---")
    return "Sequential execution complete."

async def run_concurrent():
    """Executes tasks using asyncio.gather(), demonstrating concurrency."""
    print("\n--- 6.4.1: Starting Concurrent Run (gather) ---")
    
    # Define the three coroutines (Doc A, B, C)
    coros = [
        simulated_fetch("Doc A (3s)", 3.0),
        simulated_fetch("Doc B (2s)", 2.0),
        simulated_fetch("Doc C (1s)", 1.0),
    ]
    
    # Use asyncio.gather() to run them concurrently.
    # Total time should be approx. 3 seconds (the max delay)
    results = await asyncio.gather(*coros)
    
    print("--- 6.4.1: Concurrent Run Finished ---")
    # print(f"Concurrent Results: {results}") # Optional: show results
    return "Concurrent execution complete."

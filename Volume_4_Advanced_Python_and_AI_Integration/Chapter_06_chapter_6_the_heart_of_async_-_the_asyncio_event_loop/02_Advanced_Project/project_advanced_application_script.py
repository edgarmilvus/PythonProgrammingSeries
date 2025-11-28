
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

import asyncio
import random
import time
from typing import Dict, Any, List, Tuple

# --- 1. Asynchronous Context Manager for Resource Management ---

class AsyncSessionManager:
    """
    Simulates an asynchronous resource (like a database connection pool or 
    HTTP session) that requires setup and teardown.
    """
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session_id = None

    async def __aenter__(self):
        """Asynchronously acquires the resource."""
        print(f"[{time.strftime('%H:%M:%S')}] Session for User {self.user_id}: Initializing connection...")
        await asyncio.sleep(0.1) # Simulate connection setup time
        self.session_id = f"SESS-{random.randint(1000, 9999)}"
        print(f"[{time.strftime('%H:%M:%S')}] Session {self.session_id} established.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Asynchronously releases the resource, ensuring cleanup."""
        print(f"[{time.strftime('%H:%M:%S')}] Session {self.session_id}: Closing connection.")
        await asyncio.sleep(0.05) # Simulate connection teardown
        if exc_type:
            print(f"[{time.strftime('%H:%M:%S')}] Session closed with exception: {exc_val}")
        return False # Propagate exceptions if they occurred

# --- 2. Simulated I/O-Bound Microservice Coroutines ---

async def fetch_profile(session: AsyncSessionManager, user_id: int) -> Dict[str, Any]:
    """Simulates fetching user profile data (usually fast)."""
    latency = random.uniform(0.2, 0.5)
    print(f"[{time.strftime('%H:%M:%S')}] Profile Service: Starting fetch (Expected latency: {latency:.2f}s)")
    await asyncio.sleep(latency)
    return {"service": "Profile", "data": f"User {user_id}", "status": "OK"}

async def fetch_recommendations(session: AsyncSessionManager, user_id: int) -> Dict[str, Any]:
    """Simulates fetching complex recommendations (variable latency)."""
    latency = random.uniform(0.5, 1.5)
    print(f"[{time.strftime('%H:%M:%S')}] Recommendation Service: Starting fetch (Expected latency: {latency:.2f}s)")
    await asyncio.sleep(latency)
    if latency > 1.2:
        # Simulate a partial failure or slow response that might time out
        return {"service": "Recommendations", "data": "Complex Model Result", "status": "SLOW_OK"}
    return {"service": "Recommendations", "data": "Fast Model Result", "status": "OK"}

async def fetch_history(session: AsyncSessionManager, user_id: int) -> Dict[str, Any]:
    """Simulates fetching large transaction history (potentially very slow)."""
    latency = random.uniform(1.0, 3.0)
    print(f"[{time.strftime('%H:%M:%S')}] History Service: Starting fetch (Expected latency: {latency:.2f}s)")
    await asyncio.sleep(latency)
    return {"service": "History", "data": f"1000 records for user {user_id}", "status": "OK"}

# --- 3. Orchestration and Timeout Management ---

async def orchestrate_dashboard_data(user_id: int, timeout: float) -> Tuple[Dict[str, Any], List[str]]:
    """
    Orchestrates all service calls concurrently using asyncio.wait() with a timeout.
    """
    results = {}
    pending_services = []
    start_time = time.monotonic()

    # Use the asynchronous context manager to ensure the session is cleaned up
    async with AsyncSessionManager(user_id) as session:
        
        # Create explicit Tasks from coroutines
        tasks = [
            asyncio.create_task(fetch_profile(session, user_id), name="ProfileTask"),
            asyncio.create_task(fetch_recommendations(session, user_id), name="RecTask"),
            asyncio.create_task(fetch_history(session, user_id), name="HistoryTask"),
        ]

        print(f"[{time.strftime('%H:%M:%S')}] Orchestrator: Waiting for tasks with max timeout of {timeout}s...")
        
        # Use asyncio.wait to manage the tasks concurrently with a hard limit
        done, pending = await asyncio.wait(
            tasks,
            timeout=timeout,
            return_when=asyncio.FIRST_EXCEPTION
        )

        # Process Done Tasks
        for task in done:
            try:
                results[task.get_name()] = task.result()
            except Exception as e:
                # Handle exceptions that occurred within the task itself
                results[task.get_name()] = {"service": task.get_name(), "status": "ERROR", "error": str(e)}

        # Process Pending Tasks (those that timed out)
        if pending:
            print(f"[{time.strftime('%H:%M:%S')}] WARNING: {len(pending)} task(s) exceeded the timeout limit.")
            for task in pending:
                # Cancel pending tasks to clean up resources and prevent them from running further
                task.cancel() 
                pending_services.append(task.get_name())
                results[task.get_name()] = {"service": task.get_name(), "status": "TIMEOUT", "error": "Operation timed out."}
                
                # Await the cancellation to ensure the task acknowledges the cancellation
                try:
                    await task 
                except asyncio.CancelledError:
                    pass # Expected exception after cancellation

    end_time = time.monotonic()
    print("-" * 50)
    print(f"[{time.strftime('%H:%M:%S')}] Orchestration Complete. Total Time: {end_time - start_time:.2f}s")
    return results, pending_services

# --- 4. Main Execution ---

if __name__ == "__main__":
    USER_ID = 42
    GLOBAL_TIMEOUT = 1.5 # Set a strict timeout

    final_results, missed_services = asyncio.run(orchestrate_dashboard_data(USER_ID, GLOBAL_TIMEOUT))

    print("\nFINAL AGGREGATED RESULTS:")
    for name, result in final_results.items():
        print(f"  {name:<15}: Status={result.get('status', 'N/A')}, Data={result.get('data', result.get('error'))}")
    
    if missed_services:
        print(f"\nCRITICAL: The following services were missed due to timeout and were cancelled: {', '.join(missed_services)}")

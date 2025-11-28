
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
import aiohttp
import time
import random
import os
from typing import List, Dict, Any, Tuple

# --- Configuration for Exercises ---
# URLs for Exercise 9.1
URLS_9_1 = [
    "https://httpbin.org/get",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/4", # Will be used to test timeout
    "http://nonexistent.domain.xyz" # DNS failure test
]

# URL for Exercise 9.4 (5MB simulated file)
LARGE_FILE_URL = "https://httpbin.org/bytes/5000000"
DOWNLOAD_PATH = "downloaded_file_9_4.bin"

# --- Exercise 9.1: Concurrent Status Checker ---

async def fetch_url(session: aiohttp.ClientSession, url: str, timeout_sec: float = 3.0) -> Dict[str, Any]:
    """Fetches a URL, handles exceptions, and reports status and latency."""
    start_time = time.monotonic()
    status = "Unknown"
    error = None
    
    try:
        # Define a request-specific timeout
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        
        async with session.get(url, timeout=timeout) as response:
            # Read content to ensure full transfer is measured
            await response.read() 
            status = response.status
            
    # EAFP Exception handling block
    except aiohttp.ClientResponseError as e:
        # Handles 4xx/5xx status codes if raise_for_status() was used, 
        # but here we catch specific client errors like redirects, etc., if they occurred.
        status = f"HTTP Error {e.status}"
        error = str(e)
    except aiohttp.ClientConnectionError as e:
        # Catches DNS failures, connection resets, etc.
        status = "ClientConnectionError"
        error = str(e)
    except asyncio.TimeoutError:
        # Catches the specific timeout defined above
        status = "TimeoutError"
        error = f"Request timed out after {timeout_sec}s"
    except Exception as e:
        # Catch unexpected errors
        status = f"Unexpected Error: {type(e).__name__}"
        error = str(e)
        
    duration = time.monotonic() - start_time
    
    return {
        "url": url,
        "status": status,
        "duration": duration,
        "error": error
    }

async def run_exercise_9_1():
    print("\n--- Exercise 9.1: Concurrent Status Code Verification and Latency Reporting ---")
    
    # Configure specific timeouts to force failures for testing
    url_timeouts = {
        "https://httpbin.org/delay/4": 0.5, # Will fail due to short timeout
        "http://nonexistent.domain.xyz": 5.0 # Should fail quickly via DNS
    }
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in URLS_9_1:
            timeout = url_timeouts.get(url, 5.0)
            tasks.append(fetch_url(session, url, timeout))
            
        # Execute all requests concurrently
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(f"URL: {result['url']}")
            print(f"  Status: {result['status']}")
            print(f"  Latency: {result['duration']:.3f}s")
            if result['error']:
                print(f"  Error Detail: {result['error']}")
            print("-" * 20)

# --- Exercise 9.2: Controlled Concurrency with Asynchronous Semaphores ---

async def rate_limited_fetch(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore, task_id: int):
    """Fetches a URL under semaphore control."""
    task_name = f"Task-{task_id}"
    
    print(f"[{task_name}] Waiting to acquire semaphore...")
    
    # Acquire the semaphore slot (critical section starts here)
    async with semaphore:
        # The semaphore value is the number of available slots. 
        # Active tasks = CONCURRENCY_LIMIT - semaphore._value.
        active_count = 10 - semaphore._value
        print(f"[{task_name}] ACQUIRED. Active tasks in critical section: {active_count}")
        
        status = "N/A"
        sleep_time = random.uniform(0.1, 0.5)
        
        try:
            # Simulate a request to an endpoint
            async with session.get(url) as response:
                # Simulate processing time while holding the semaphore
                await asyncio.sleep(sleep_time)
                status = response.status
        except aiohttp.ClientError as e:
            status = f"Error: {e.__class__.__name__}"

        print(f"[{task_name}] RELEASED. Status: {status}. Simulated work: {sleep_time:.2f}s")
        # Semaphore is automatically released upon exiting the 'async with' block

async def run_exercise_9_2():
    print("\n--- Exercise 9.2: Controlled Concurrency with Asynchronous Semaphores ---")
    
    CONCURRENCY_LIMIT = 10
    TOTAL_REQUESTS = 50
    
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    # Generate unique URLs for simulation
    urls = [f"https://httpbin.org/get?request_id={i}" for i in range(TOTAL_REQUESTS)]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            # Create tasks explicitly naming them for clearer logging
            task = asyncio.create_task(rate_limited_fetch(session, url, semaphore, i + 1), name=f"Task-{i+1}")
            tasks.append(task)
            
        await asyncio.gather(*tasks)
        
    print("\nSemaphore controlled fetching complete.")

# --- Exercise 9.3: Interactive Challenge (Conceptual Refactoring) ---

async def create_session() -> aiohttp.ClientSession:
    """Session factory function. Called once at application start."""
    print("[SYSTEM] Creating new ClientSession...")
    # Setting a base timeout for the entire session lifecycle
    timeout = aiohttp.ClientTimeout(total=60.0) 
    return aiohttp.ClientSession(timeout=timeout)

async def worker_fetch(session: aiohttp.ClientSession, index: int):
    """Worker coroutine that requires the session object (Dependency Injection)."""
    url = f"https://httpbin.org/delay/0.5?id={index}"
    
    # 4. Simulated Failure
    if index == 5:
        print(f"[WORKER {index}] Simulating pre-request processing...")
        await asyncio.sleep(0.1)
        # This error simulates a critical application failure deep within the task logic
        raise ValueError(f"Critical processing error in Task {index}")
        
    try:
        print(f"[WORKER {index}] Requesting {url}...")
        # Session is passed in, not created locally
        async with session.get(url) as response:
            await response.text()
            print(f"[WORKER {index}] Success, Status: {response.status}")
    except aiohttp.ClientError as e:
        print(f"[WORKER {index}] Network error: {e.__class__.__name__}")
    except ValueError as e:
        # Re-raising the deliberate error to propagate it up to asyncio.gather
        raise e

async def run_refactored_application():
    """Main entry point using the refactored session context manager."""
    print("\n--- Exercise 9.3: Centralized Session Management and Graceful Shutdown ---")
    
    urls_count = 10
    
    try:
        # 1 & 2. Context Manager Enforcement and Session Factory usage
        async with create_session() as session:
            print("[SYSTEM] Session is active and managed by async with block.")
            
            # 3. Dependency Injection: Passing the session explicitly
            tasks = [worker_fetch(session, i) for i in range(1, urls_count + 1)]
            
            # Use return_exceptions=True to allow the other tasks to finish 
            # and ensure the 'async with' block is eventually exited.
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle results and check for simulated failure
            for result in results:
                if isinstance(result, Exception):
                    print(f"[ERROR] An exception occurred: {result.__class__.__name__}: {result}")
                    
    except Exception as e:
        # This block catches errors during session creation/setup if they occurred.
        print(f"[CRITICAL FAILURE] Application terminated prematurely: {e.__class__.__name__}")
    finally:
        # This logic confirms the session closure guarantee
        print("[SYSTEM] Async with block exited. Session closure guaranteed.")

async def run_exercise_9_3():
    await run_refactored_application()
    
    # 5. Visualization of Flow Explanation
    print("\n--- Explanation of Refactoring Benefits (Exercise 9.3) ---")
    print("The 'async with create_session() as session:' structure enforces the EAFP (Easier to Ask for Forgiveness than Permission) principle for resource management.")
    print("1. **Resource Cleanup Guarantee:** The `__aexit__` method of `ClientSession` is *guaranteed* to be called when the `async with` block is exited, regardless of whether it exits normally or due to an exception (like the simulated `ValueError` from Task 5).")
    print("2. **Socket Leak Prevention:** This prevents socket leaks and ensures all underlying connections in the pool are properly closed, which is critical in long-running applications.")
    print("3. **Dependency Injection:** Passing the session explicitly ensures that worker functions are testable and rely on a single, shared, application-wide resource, maximizing connection reuse.")

# --- Exercise 9.4: Asynchronous Large File Streaming ---

async def download_file(session: aiohttp.ClientSession, url: str, file_path: str, chunk_size: int = 1024 * 100):
    """Downloads a file in chunks and performs integrity check."""
    
    start_time = time.monotonic()
    bytes_written = 0
    content_length = None
    
    print(f"Starting streaming download of {url} to {file_path}...")
    
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error: Received status code {response.status}")
                return
                
            content_length = response.content_length
            print(f"Header Content Length: {content_length} bytes")
            
            # Open file in binary write mode
            with open(file_path, 'wb') as f:
                # Use response.content (StreamReader) for chunked reading
                while True:
                    # 3. Chunked Reading using await
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_written += len(chunk)
                    
                    # Optional: Print progress every 1MB
                    if bytes_written % (1024 * 1024) == 0 and bytes_written > 0:
                        print(f"  Downloaded: {bytes_written / (1024 * 1024):.2f} MB...")
                        
    except aiohttp.ClientError as e:
        print(f"A client error occurred during download: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        duration = time.monotonic() - start_time
        
        print("\n--- Download Summary ---")
        print(f"Total Bytes Written: {bytes_written} bytes")
        print(f"Total Time: {duration:.3f} seconds")
        
        # 4. Performance and Integrity Reporting
        if duration > 0:
            speed_bps = bytes_written / duration
            speed_mbps = speed_bps / (1024 * 1024) # Convert B/s to MB/s
            print(f"Average Download Speed: {speed_mbps:.2f} MB/s")
            
        # Integrity Check
        if content_length is not None and bytes_written == content_length:
            print("Integrity Check: SUCCESS (Bytes written matches Content-Length header).")
        elif content_length is None:
            print("Integrity Check: WARNING (Content-Length header missing).")
        else:
            print(f"Integrity Check: FAILURE (Header: {content_length}, Written: {bytes_written}).")
            
        # 5. Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up temporary file: {file_path}")


async def run_exercise_9_4():
    print("\n--- Exercise 9.4: Asynchronous Large File Streaming and Integrity Check ---")
    
    async with aiohttp.ClientSession() as session:
        await download_file(session, LARGE_FILE_URL, DOWNLOAD_PATH)


# --- Main Runner ---

async def main_exercises():
    """Runs all exercises sequentially for clarity."""
    await run_exercise_9_1()
    await run_exercise_9_2()
    await run_exercise_9_3()
    await run_exercise_9_4()

if __name__ == "__main__":
    # Standard asyncio runner
    try:
        asyncio.run(main_exercises())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

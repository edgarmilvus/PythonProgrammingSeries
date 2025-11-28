
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
import aiohttp
import time
from typing import List, Dict, Any, Union

# 1. Configuration and Mock Data
# This list simulates critical API endpoints that must be checked.
TARGET_URLS: List[str] = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://httpbin.org/delay/3",          # Intentional 3-second delay to highlight concurrency benefits
    "https://httpbin.org/status/404",       # Intentional failure status test
    "http://nonexistent-domain-test-123.com", # Intentional DNS/Connection Error
    "https://jsonplaceholder.typicode.com/users/3",
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/comments/4",
    "https://jsonplaceholder.typicode.com/albums/5",
    "https://jsonplaceholder.typicode.com/photos/6",
]

# Type alias for clarity in result handling
HealthReportItem = Dict[str, Union[str, int]]

# 2. Asynchronous Request Handler
async def fetch_status(session: aiohttp.ClientSession, url: str) -> HealthReportItem:
    """
    Fetches the status and latency for a single URL using the shared ClientSession.
    Handles common network errors (timeouts, connection failures).
    """
    start_time = time.monotonic()
    status: Union[str, int] = "Unknown"
    
    try:
        # Define a per-request timeout to prevent a single slow service from freezing the whole check
        timeout = aiohttp.ClientTimeout(total=5.0) 
        
        # Use the shared session for persistent connections and pooling
        async with session.get(url, timeout=timeout, ssl=False) as response:
            status = response.status
            
            # CRITICAL: Read the response body even if we don't use it. 
            # This ensures the underlying connection is properly released back 
            # into the ClientSession's pool for reuse.
            await response.read() 
            
    except aiohttp.ClientConnectorError:
        # Handles DNS failures, refused connections, or network unavailability
        status = "Connection Error (DNS/Refused)"
    except asyncio.TimeoutError:
        # Handles reaching the 'total' timeout defined above
        status = "Timeout Error (5.0s)"
    except Exception as e:
        # Catch any other unexpected I/O exceptions
        status = f"Unhandled Error: {type(e).__name__}"
            
    end_time = time.monotonic()
    # Calculate latency in milliseconds
    latency = (end_time - start_time) * 1000 

    return {
        "url": url,
        "status": status,
        "latency_ms": f"{latency:.2f}"
    }

# 3. Main Orchestration Function
async def run_health_check(urls: List[str]) -> List[HealthReportItem]:
    """
    Orchestrates the concurrent execution of all health checks using asyncio.gather().
    """
    # Define connection limits for robust performance and resource control.
    # Limiting to 5 concurrent connections prevents overwhelming the target APIs or local resources.
    connector = aiohttp.TCPConnector(limit=5) 
    
    # Initialize the ClientSession within an async context manager for guaranteed cleanup
    async with aiohttp.ClientSession(connector=connector) as session:
        print(f"--- Starting Concurrent Checks for {len(urls)} Services ---")
        
        # 3a. Create Coroutine Objects
        # Map the fetch_status coroutine function over all URLs
        tasks = [fetch_status(session, url) for url in urls]
        
        # 3b. Concurrent Execution
        # asyncio.gather executes all coroutines concurrently.
        # return_exceptions=True ensures that if one fetch_status raises an exception 
        # (which shouldn't happen here due to internal try/except, but is good practice), 
        # the remaining tasks are not cancelled.
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print("--- All Checks Complete ---")
        
        # Filter results to ensure only valid dictionary reports are returned
        final_results = [r for r in results if isinstance(r, dict)]
        
        return final_results

# 4. Execution Block
if __name__ == "__main__":
    total_start = time.monotonic()
    
    # Entry point: Run the async main function
    health_report = asyncio.run(run_health_check(TARGET_URLS))
    
    total_end = time.monotonic()
    total_time = total_end - total_start

    # 5. Reporting
    print("\n=======================================================")
    # Note: Sequential time would be roughly the sum of all latencies (dominated by the 3s delay)
    print(f"| Total Execution Time: {total_time:.2f}s |")
    print("=======================================================")
    
    for item in health_report:
        # Use ANSI colors for visual clarity in the terminal
        status_code = item['status']
        if status_code == 200:
            status_color = "\033[92m" # Green
        elif isinstance(status_code, int) and status_code >= 400:
            status_color = "\033[93m" # Yellow (Client Error)
        else:
            status_color = "\033[91m" # Red (Server Error or Connection Failure)
            
        reset_color = "\033[0m"
        
        print(f"[{status_color}{status_code:<25}{reset_color}] {item['url']:<55} Latency: {item['latency_ms']} ms")

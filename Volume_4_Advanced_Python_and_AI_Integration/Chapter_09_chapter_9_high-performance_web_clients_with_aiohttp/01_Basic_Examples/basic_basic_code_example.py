
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
import aiohttp
import json
from typing import Dict, Any

# Define the structure for the data we expect to receive
TodoItem = Dict[str, Any]

# 1. Define the asynchronous coroutine responsible for fetching
async def fetch_single_todo(todo_id: int) -> TodoItem | None:
    """
    Fetches a single JSON object asynchronously using aiohttp.
    """
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    print(f"[{todo_id}] Preparing request for URL: {url}")

    # 2. Initialize the ClientSession
    # ClientSession is crucial for connection pooling and resource management.
    # The 'async with' statement ensures the session is closed automatically.
    try:
        async with aiohttp.ClientSession() as session:
            print(f"[{todo_id}] Session created. Starting GET request...")

            # 3. Perform the GET request
            # This returns a ClientResponse object (a context manager).
            # The 'await' here pauses the coroutine until the response headers are received.
            async with session.get(url) as response:
                print(f"[{todo_id}] Received headers. Status: {response.status}")

                # 4. Check status and process response body
                if response.status == 200:
                    # 'await response.json()' is an I/O operation: reading the body data.
                    # This is where the coroutine pauses again, waiting for the full payload.
                    data = await response.json()
                    print(f"[{todo_id}] Data body successfully read.")
                    return data
                else:
                    # Handle non-200 responses
                    print(f"[{todo_id}] HTTP Error: Status {response.status}")
                    response.raise_for_status() # Raises ClientResponseError for 4xx/5xx

    except aiohttp.ClientConnectorError as e:
        print(f"[{todo_id}] Connection Error occurred: {e}")
        return None
    except aiohttp.ClientResponseError as e:
        print(f"[{todo_id}] Response Error occurred: {e}")
        return None
    except Exception as e:
        print(f"[{todo_id}] An unexpected error occurred: {e}")
        return None

# 5. Define the main execution coroutine
async def main():
    """
    The entry point that schedules and executes the asynchronous client task.
    """
    print("--- Starting aiohttp Client Demo ---")
    
    # Execute the single fetch operation
    todo_item = await fetch_single_todo(todo_id=42)

    if todo_item:
        print("\n--- Final Retrieved Data ---")
        # Use json.dumps for pretty printing the resulting dictionary
        print(json.dumps(todo_item, indent=4))
        print("----------------------------")
    else:
        print("\nFailed to retrieve the todo item.")

# 6. Execute the asyncio event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    print("--- Client Demo Finished ---")

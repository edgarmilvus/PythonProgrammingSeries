
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

# --- Exercise 6.4.3 Implementations ---

async def worker_a(task_id: str) -> str:
    """Worker that returns result via standard coroutine return."""
    print(f"[{task_id}] Worker A started.")
    await asyncio.sleep(2.0)
    print(f"[{task_id}] Worker A finished.")
    return f"Result from {task_id}"

async def worker_b_future(future_obj: asyncio.Future):
    """Worker that sets result directly on a shared Future object."""
    print("[Worker B] Worker B started, will set Future result.")
    await asyncio.sleep(1.0)
    
    # Set the result on the future_obj
    if not future_obj.done():
        future_obj.set_result("Future Result Set via Worker B")
    
    print("[Worker B] Worker B set result on Future.")

async def monitor_tasks():
    """Manages tasks explicitly and awaits both a Task and a Future."""
    print("\n--- 6.4.3: Manual Task and Future Management ---")
    
    # 1. Instantiate Future
    shared_future = asyncio.Future()
    
    # 2. Explicitly create Tasks
    task_a = asyncio.create_task(worker_a("Task A"))
    task_b = asyncio.create_task(worker_b_future(shared_future))
    
    # 3. Check status immediately
    print(f"Task A done status immediately after creation: {task_a.done()}") # Expected: False
    
    # 4. Await Task A directly (waits 2 seconds)
    result_a = await task_a
    print(f"Received result from Task A: {result_a}")
    print(f"Task A done status after awaiting: {task_a.done()}") # Expected: True
    
    # 5. Await the Future object (Worker B should have finished and set the result after 1 second, 
    # but we await it here after Task A is done.)
    result_future = await shared_future
    print(f"Received result from Future: {result_future}")
    
    # Clean up Task B (it should be done, but good practice)
    if not task_b.done():
        task_b.cancel()
        
    print("--- 6.4.3: Manual Task and Future Management Finished ---")

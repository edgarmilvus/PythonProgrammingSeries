
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

# 1. Refactor the Worker: synchronous_io_task -> async_io_task
async def async_io_task(task_id: int, duration: float) -> str:
    """
    Asynchronous worker simulating I/O latency using cooperative sleep.
    """
    start_time = time.time()
    print(f"[{start_time:.2f}] Task {task_id}: Starting asynchronous operation.")
    
    # 2. Replace Blocking Call: time.sleep -> await asyncio.sleep
    # This yields control back to the event loop non-blockingly.
    await asyncio.sleep(duration)
    
    end_time = time.time()
    print(f"[{end_time:.2f}] Task {task_id}: Asynchronous operation finished.")
    return f"Result of Task {task_id} (Duration: {duration}s)"

# 3. Refactor the Main Function: main_sync -> main_async
async def main_async():
    """
    Asynchronous main function enforcing sequential execution using await.
    """
    print("\n--- Running Exercise 7.4.4: Refactored Asynchronous Main ---")
    start = time.time()
    results = []
    
    # 4. Enforce Awaiting: Sequential execution requires explicit await
    results.append(await async_io_task(1, 1.5))
    results.append(await async_io_task(2, 2.0))
    results.append(await async_io_task(3, 0.5))
    
    total_time = time.time() - start
    print(f"\nAll tasks completed.")
    print(f"Total sequential asynchronous time: {total_time:.2f}s (Expected: 4.0s)")
    print(f"Collected results: {results}")
    return results

# Execution (placed in the final block)
# asyncio.run(main_async())

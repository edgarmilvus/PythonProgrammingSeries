
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# --- Exercise 6.4.2 Implementations ---

async def query_kb(kb_name: str, delay: float):
    """Simulates querying a knowledge base with a variable delay."""
    print(f"[{kb_name}] Query started. Expected delay: {delay:.1f}s")
    
    try:
        await asyncio.sleep(delay)
        print(f"[{kb_name}] Query completed successfully.")
        return f"Result from {kb_name}"
    except asyncio.CancelledError:
        # Crucial: Handle the cancellation signal
        print(f"[{kb_name}] Task was cancelled due to timeout.")
        raise # Re-raise the cancellation error

async def manage_wait_timeout():
    """Uses asyncio.wait() to enforce a strict timeout."""
    print("\n--- 6.4.2: Starting Wait Timeout Scenario ---")
    
    # Define tasks: A (2s), B (4s - will time out), C (1s)
    task_a = asyncio.create_task(query_kb("KB-A", 2.0))
    task_b = asyncio.create_task(query_kb("KB-B (Slow)", 4.0))
    task_c = asyncio.create_task(query_kb("KB-C", 1.0))
    
    all_tasks = {task_a, task_b, task_c}
    
    print(f"Total tasks launched: {len(all_tasks)}. Waiting with 3.5s timeout...")

    # Use asyncio.wait() with a timeout of 3.5 seconds
    done, pending = await asyncio.wait(
        all_tasks,
        timeout=3.5,
        return_when=asyncio.ALL_COMPLETED # wait for timeout or all completion
    )

    print(f"\nAnalysis after 3.5s timeout:")
    print(f"Done tasks count: {len(done)}")
    print(f"Pending tasks count: {len(pending)}")
    
    # Analyze results and print status of tasks in done/pending sets
    for task in done:
        try:
            # Await the done task to retrieve its result or exception
            result = task.result()
            print(f"  [DONE] {task.get_name()}: Result received: {result}")
        except asyncio.CancelledError:
            print(f"  [DONE] {task.get_name()}: Task finished early due to cancellation (not expected here, but good practice).")
    
    # Clean Up: Iterate over pending tasks and cancel them
    if pending:
        print("\nCancelling pending tasks:")
        for task in pending:
            print(f"  [PENDING] Cancelling {task.get_name()}...")
            task.cancel()
            
            # Await the cancellation to ensure the task fully cleans up
            try:
                await task
            except asyncio.CancelledError:
                pass # Expected exception when awaiting a cancelled task
    
    print("--- 6.4.2: Wait Timeout Scenario Finished ---")

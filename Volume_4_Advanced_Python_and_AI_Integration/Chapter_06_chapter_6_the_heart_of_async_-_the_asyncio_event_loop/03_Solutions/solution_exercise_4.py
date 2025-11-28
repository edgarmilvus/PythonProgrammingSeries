
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

# --- Exercise 6.4.4 Implementations (Interactive Challenge) ---

async def simulate_llm_call(task_name: str, delay: float, token_count: int) -> str:
    """
    Simulates an LLM generating tokens incrementally over time.
    If the task name is 'Task 4', it raises an error.
    """
    print(f"[{task_name}] Starting LLM call. Total time: {delay:.1f}s, Tokens: {token_count}")
    
    if task_name == "Task 4 (Error)":
        await asyncio.sleep(2.0)
        raise LLMAPIError(f"API Error during call to {task_name}")

    # Calculate small sleep time per token
    token_delay = delay / token_count
    full_response = []
    
    # Simulate streaming token generation
    for i in range(1, token_count + 1):
        await asyncio.sleep(token_delay)
        token = f"T{i}"
        full_response.append(token)
        
    return f"[{task_name}] Response ({len(full_response)} tokens): {' '.join(full_response)}"

async def run_streaming_pipeline():
    """
    Uses asyncio.as_completed() to process results as they finish,
    mimicking real-time streaming prioritization.
    """
    print("\n--- 6.4.4: Interactive Challenge: Streaming via as_completed() ---")
    
    # Define tasks with varying delays and token counts
    tasks = [
        asyncio.create_task(simulate_llm_call("Task 1 (Fast)", 1.0, 10)),
        asyncio.create_task(simulate_llm_call("Task 2 (Medium)", 3.0, 30)),
        asyncio.create_task(simulate_llm_call("Task 3 (Slow)", 5.0, 50)),
        asyncio.create_task(simulate_llm_call("Task 4 (Error)", 4.0, 1)), # Error task
    ]
    
    start_time = time.perf_counter()
    
    # Iterate over tasks using asyncio.as_completed()
    print("Awaiting results in order of completion...")
    for future in asyncio.as_completed(tasks):
        try:
            # Await the result of the *next* completed task
            result = await future
            elapsed = time.perf_counter() - start_time
            print(f"[{elapsed:.2f}s] Processed result: {result}")
            
        except LLMAPIError as e:
            # Catch the specific error from Task 4
            elapsed = time.perf_counter() - start_time
            print(f"[{elapsed:.2f}s] ERROR CAUGHT: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            elapsed = time.perf_counter() - start_time
            print(f"[{elapsed:.2f}s] UNEXPECTED ERROR: {e}")
            
    print("--- 6.4.4: Streaming Pipeline Finished ---")


# --- Main Execution Block (Complete Code for Testing) ---

async def main():
    # --- 6.4.1 Execution ---
    start_time_seq = time.perf_counter()
    await run_sequential()
    end_time_seq = time.perf_counter()
    print(f"\nTotal Sequential Time: {end_time_seq - start_time_seq:.2f}s (Expected ~6.00s)")

    start_time_conc = time.perf_counter()
    await run_concurrent()
    end_time_conc = time.perf_counter()
    print(f"\nTotal Concurrent Time: {end_time_conc - start_time_conc:.2f}s (Expected ~3.00s)")

    # --- 6.4.2 Execution ---
    await manage_wait_timeout()

    # --- 6.4.3 Execution ---
    await monitor_tasks()

    # --- 6.4.4 Execution ---
    await run_streaming_pipeline()

if __name__ == "__main__":
    # Note: asyncio.run() handles setting up and shutting down the event loop
    # and implicitly waits for the main coroutine to complete.
    asyncio.run(main())

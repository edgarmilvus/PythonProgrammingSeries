
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

async def validate_data(item_id: int):
    """Simulates data validation I/O (0.5s)."""
    print(f"[{time.time():.2f}] Item {item_id} | Validation: Starting (0.5s)")
    await asyncio.sleep(0.5)
    print(f"[{time.time():.2f}] Item {item_id} | Validation: Finished")

async def transform_data(item_id: int):
    """Simulates data transformation I/O (1.0s)."""
    print(f"[{time.time():.2f}] Item {item_id} | Transformation: Starting (1.0s)")
    await asyncio.sleep(1.0)
    print(f"[{time.time():.2f}] Item {item_id} | Transformation: Finished")

async def persist_data(item_id: int):
    """Simulates data persistence I/O (0.2s)."""
    print(f"[{time.time():.2f}] Item {item_id} | Persistence: Starting (0.2s)")
    await asyncio.sleep(0.2)
    print(f"[{time.time():.2f}] Item {item_id} | Persistence: Finished")

async def run_pipeline(item_id: int):
    """
    Runs the three stages sequentially for a single item.
    """
    print(f"\n--- Starting Pipeline for Item {item_id} ---")
    
    # Await ensures sequential completion: Validation must finish before Transformation starts.
    await validate_data(item_id)
    await transform_data(item_id)
    await persist_data(item_id)
    
    print(f"--- Pipeline Finished for Item {item_id} ---")

async def main_pipeline():
    """
    Executes two pipeline runs sequentially.
    """
    print("\n--- Running Exercise 7.4.2: Cooperative Pipeline ---")
    
    # Item 101 must fully complete before Item 102 begins.
    await run_pipeline(101)
    await run_pipeline(102)

# Execution (placed in the final block)
# asyncio.run(main_pipeline())

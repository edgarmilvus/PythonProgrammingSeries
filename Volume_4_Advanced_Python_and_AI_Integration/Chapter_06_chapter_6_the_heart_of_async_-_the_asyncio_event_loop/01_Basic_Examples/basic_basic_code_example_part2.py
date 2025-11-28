
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

# Source File: basic_basic_code_example_part2.py
# Description: Basic Code Example
# ==========================================

import time # Synchronous module
import asyncio

async def bad_blocking_fetch(task_name: str):
    print(f"[{task_name}] Starting blocking operation...")
    
    # DANGER: This is a synchronous call!
    # It blocks the ENTIRE SINGLE THREAD for 3 seconds.
    time.sleep(3) 
    
    print(f"[{task_name}] Blocking operation finished.")

async def main_bad():
    # These tasks will now run sequentially, taking 6 seconds total.
    await asyncio.gather(
        bad_blocking_fetch("Task 1"),
        bad_blocking_fetch("Task 2")
    )

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main_bad())
    end = time.perf_counter()
    # Output will be ~6 seconds, not ~3 seconds.
    print(f"Total time: {end - start:.2f}s")

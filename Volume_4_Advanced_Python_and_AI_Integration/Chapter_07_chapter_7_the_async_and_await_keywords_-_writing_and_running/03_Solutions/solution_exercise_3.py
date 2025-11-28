
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

async def fetch_default_config() -> Dict[str, Any]:
    """Fetches default configuration settings (1.0s delay)."""
    print(f"[{time.time():.2f}] Fetching defaults...")
    await asyncio.sleep(1.0)
    defaults = {'theme': 'dark', 'timeout': 30, 'log_level': 'INFO', 'port': 8080}
    print(f"[{time.time():.2f}] Defaults fetched.")
    return defaults

async def fetch_user_overrides() -> Dict[str, Any]:
    """Fetches user-specific overrides (0.5s delay)."""
    print(f"[{time.time():.2f}] Fetching overrides...")
    await asyncio.sleep(0.5)
    overrides = {'theme': 'light', 'timeout': 60, 'port': 9000}
    print(f"[{time.time():.2f}] Overrides fetched.")
    return overrides

async def aggregate_config() -> Dict[str, Any]:
    """
    Awaits configuration sources and merges them using dict.update().
    """
    print("\n--- Running Exercise 7.4.3: Configuration Aggregator ---")
    
    # Await and retrieve the return value of the coroutines sequentially
    default_config = await fetch_default_config()
    user_config = await fetch_user_overrides()
    
    # Merge the configurations. Overrides take precedence.
    final_config = default_config.copy()
    
    # dict.update() merges user_config into final_config, overwriting shared keys.
    final_config.update(user_config)
    
    return final_config

# Execution (placed in the final block)
# final_config = asyncio.run(aggregate_config())
# print(f"\nFinal Merged Configuration:\n{final_config}")

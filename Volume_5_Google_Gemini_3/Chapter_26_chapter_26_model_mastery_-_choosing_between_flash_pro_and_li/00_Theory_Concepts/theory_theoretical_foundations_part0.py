
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

# Source File: theory_theoretical_foundations_part21.py
# Description: Theoretical Foundations
# ==========================================

import time
import os
from google import genai
from google.genai.errors import APIError
from typing import Optional

# --- 1. CONFIGURATION AND SETUP ---

# The client is initialized using an environment variable for security.
# In a production environment, this key must always be secured.
try:
    # Attempt to initialize the client.
    # Note: If the API key is not set, the API calls will raise an error, 
    # which we handle in the benchmark function.
    client = genai.Client()
except Exception as e:
    # This block handles local setup issues if the key is missing during execution
    print(f"# Warning: Client initialization failed. Ensure GEMINI_API_KEY is configured.")
    client = None # Set client to None if initialization fails

# Define the models we are comparing based on the official documentation
# We use the stable versions for reliable comparison
MODEL_FLASH = "gemini-2.5-flash"
MODEL_PRO = "gemini-2.5-pro" 

# A complex prompt designed to require deep, multi-step reasoning (favoring Pro)
COMPLEX_PROMPT = (
    "Analyze the following argument: 'All birds fly. Penguins are birds. Therefore, penguins fly.' "
    "Identify the logical fallacy (e.g., equivocation, non sequitur, etc.), explain why the conclusion is invalid "
    "by referencing the specific biological facts about penguins, and provide a corrected, logically sound "
    "syllogism using the same structure (All A are B, C is A, Therefore C is B) but with valid premises."
)

# A simple prompt designed for rapid throughput (favoring Flash)
SIMPLE_PROMPT = "Summarize the key difference between latency and throughput in exactly five words."


def benchmark_model_latency(model_name: str, prompt: str, iterations: int = 3) -> float:
    """
    Measures the average latency (response time) for a given model and prompt.
    
    The function records the time difference between the request start and response end,
    analogous to calculating a datetime.timedelta duration.
    """
    if client is None:
        print(f"# Cannot benchmark {model_name}: Client not initialized.")
        return float('inf')

    total_time = 0.0
    
    # We use a try-except block to handle potential API issues during benchmarking
    try:
        print(f"\n# Starting benchmark for {model_name}...")
        for i in range(iterations):
            start_time = time.time()
            
            # The core API call for text generation
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={"temperature": 0.1} # Low temperature ensures deterministic output for benchmarking
            )
            
            end_time = time.time()
            duration = end_time - start_time
            total_time += duration
            
            print(f"# Model: {model_name} | Iteration: {i + 1} | Latency: {duration:.4f} seconds | Output Length: {len(response.text.split())} words")
            
        return total_time / iterations

    except APIError as e:
        print(f"# Error calling model {model_name}: API Error encountered: {e}")
        return float('inf') # Indicate failure
    except Exception as e:
        print(f"# An unexpected error occurred during benchmarking: {e}")
        return float('inf')

# --- 2. EXECUTION DEMONSTRATION (Conceptual) ---

print("\n--- Conceptual Latency and Cost Benchmarking Setup ---")
print("# Note: Actual execution requires a valid API key and network connection.")

# 1. Test Flash with a Simple Task (Expected Low Latency)
avg_flash_simple = benchmark_model_latency(MODEL_FLASH, SIMPLE_PROMPT)
print(f"\nAverage {MODEL_FLASH} (Simple Task) Latency: {avg_flash_simple:.4f} seconds")

# 2. Test Pro with a Complex Task (Expected Higher Latency, Better Accuracy)
avg_pro_complex = benchmark_model_latency(MODEL_PRO, COMPLEX_PROMPT)
print(f"\nAverage {MODEL_PRO} (Complex Task) Latency: {avg_pro_complex:.4f} seconds")

# 3. Test Flash with a Complex Task (To check if the capability threshold is met)
avg_flash_complex = benchmark_model_latency(MODEL_FLASH, COMPLEX_PROMPT)
print(f"\nAverage {MODEL_FLASH} (Complex Task) Latency: {avg_flash_complex:.4f} seconds")


# 4. Decision Point Simulation (Conceptual Analysis)
print("\n--- Model Selection Analysis ---")

if avg_flash_simple < avg_pro_complex:
    print(f"# Observation 1: {MODEL_FLASH} is faster than {MODEL_PRO} for simple tasks, confirming the latency optimization.")
else:
    print(f"# Observation 1: Latency difference is negligible or {MODEL_PRO} was faster (unlikely for simple tasks).")

# The true decision relies on the quality of the COMPLEX_PROMPT response.
# If Flash's complex response quality is acceptable, we choose Flash due to cost/latency benefits.
# If Pro's complex response quality is significantly better, we must choose Pro, accepting the higher cost and latency.

# Conceptualizing the cost difference (based on typical tier pricing ratios)
if avg_flash_simple != float('inf') and avg_pro_complex != float('inf'):
    print("\n# ECONOMIC FACTOR: If Flash costs 1/10th of Pro, using Pro for simple tasks results in significant overspending.")
    print("# The engineering challenge is to use Flash for 80% of tasks and reserve Pro for the remaining 20% that demand peak reasoning.")


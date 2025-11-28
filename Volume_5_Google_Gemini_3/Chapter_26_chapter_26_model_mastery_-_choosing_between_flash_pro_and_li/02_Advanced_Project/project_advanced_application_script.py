
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

import os
import time
import concurrent.futures
from typing import List, Dict, Any, Tuple

# We are using the standard google-genai SDK
from google import genai
from google.genai.errors import APIError

# --- 1. Configuration and Model Definitions ---

# NOTE: Ensure your GEMINI_API_KEY is set in your environment variables.
try:
    CLIENT = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Check API Key configuration: {e}")
    # Exit gracefully if the client cannot be initialized
    exit()

# Define the models based on the official documentation provided.
# Flash: Optimized for speed, cost, and high-volume tasks.
FLASH_MODEL = "gemini-2.5-flash"
# Pro: Optimized for complex reasoning and high-quality output.
PRO_MODEL = "gemini-2.5-pro"

# Define hypothetical relative costs for simulation purposes (per million input tokens).
# These are relative factors, not actual prices.
COST_FACTOR_FLASH = 1.0  # Baseline cost
COST_FACTOR_PRO = 5.0    # Pro is significantly more expensive per token

# --- 2. Task Definitions (Prompts) ---

# Task A: High-Volume, Low-Complexity (Data Extraction/Summarization)
# Requires basic pattern matching and summarization.
SIMPLE_TASK_PROMPT = """
Analyze the following legal clause and extract two pieces of information:
1. The full name of the 'First Party'.
2. The exact date the agreement commences.
Return the result as a simple JSON object with keys 'party_name' and 'commencement_date'.

Clause: 'This Master Service Agreement, effective as of 2024-09-15, is hereby entered into by and between
Acme Corp. (referred to hereafter as the 'First Party') and Beta Solutions Inc. (the 'Second Party').
The First Party commits to delivering all specified services within 90 days of the commencement date.'
"""

# Task B: Low-Volume, High-Complexity (Reasoning/Contradiction Analysis)
# Requires deep logical analysis and cross-referencing.
COMPLEX_TASK_PROMPT = """
You are a legal risk analyst. Analyze the following two clauses and determine if they present a material contradiction.
If they contradict, explain why and suggest a single word change to resolve the conflict.
If they do not contradict, explain why they are compatible.

Clause 1 (Termination): 'Either party may terminate this agreement with cause by providing 30 days written notice.'
Clause 2 (Notice Period): 'The notice period for any termination, regardless of cause, must be 60 calendar days.'

Provide a detailed analysis and conclusion in a markdown format.
"""

# --- 3. Core Benchmarking Logic ---

def execute_single_request(model_name: str, prompt: str) -> Tuple[float, int]:
    """
    Executes a single synchronous API call and measures the latency and token usage.
    This function is designed to be run concurrently by the ThreadPoolExecutor.
    """
    start_time = time.perf_counter()
    
    try:
        # Generate content using the specified model
        response = CLIENT.models.generate_content(
            model=model_name,
            contents=prompt,
            config={"temperature": 0.1}
        )
        
        end_time = time.perf_counter()
        latency = end_time - start_time
        
        # Calculate total tokens used (input + output)
        total_tokens = (
            response.usage_metadata.prompt_token_count +
            response.usage_metadata.candidates_token_count
        )
        
        return latency, total_tokens
        
    except APIError as e:
        # Handle API errors gracefully during concurrent execution
        print(f"[{model_name}] API Error encountered: {e}")
        return 0.0, 0
    except Exception as e:
        print(f"[{model_name}] Unexpected Error: {e}")
        return 0.0, 0


def benchmark_model_concurrency(
    model_name: str,
    prompt: str,
    num_requests: int,
    max_workers: int = 10
) -> Dict[str, Any]:
    """
    Runs multiple requests concurrently using a ThreadPoolExecutor to simulate load.
    The maximum number of workers simulates the available threads in a WSGI environment.
    """
    print(f"\n--- Starting Benchmark for {model_name} (Requests: {num_requests}) ---")
    
    start_total_time = time.perf_counter()
    
    # Prepare the list of tasks (model_name and prompt tuples)
    tasks = [(model_name, prompt)] * num_requests
    
    # Use ThreadPoolExecutor to run tasks concurrently
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the execute_single_request function to all tasks
        # We use executor.submit to pass arguments easily
        future_to_request = {
            executor.submit(execute_single_request, model_name, prompt): i
            for i in range(num_requests)
        }
        
        # Wait for all futures to complete and gather results
        for future in concurrent.futures.as_completed(future_to_request):
            latency, tokens = future.result()
            if latency > 0:
                results.append((latency, tokens))
                
    end_total_time = time.perf_counter()
    
    # --- 4. Analysis and Reporting ---
    
    if not results:
        return {"model": model_name, "error": "No successful requests completed."}

    total_time = end_total_time - start_total_time
    total_latency = sum(r[0] for r in results)
    total_tokens_used = sum(r[1] for r in results)
    
    # Average Latency is the total latency divided by the number of successful requests.
    avg_latency = total_latency / len(results)
    
    # Throughput (Requests Per Second)
    throughput = len(results) / total_time
    
    # Cost Simulation
    cost_factor = COST_FACTOR_FLASH if "flash" in model_name.lower() else COST_FACTOR_PRO
    hypothetical_cost = (total_tokens_used / 1_000_000) * cost_factor
    
    return {
        "model": model_name,
        "requests": len(results),
        "prompt_length": len(prompt),
        "total_time_s": round(total_time, 3),
        "avg_latency_s": round(avg_latency, 3),
        "throughput_rps": round(throughput, 2),
        "total_tokens": total_tokens_used,
        "hypothetical_cost": round(hypothetical_cost, 6)
    }


def print_results(task_name: str, results: List[Dict[str, Any]]):
    """
    Helper function to display benchmark results in a readable format.
    """
    print("\n" + "="*80)
    print(f"BENCHMARK RESULTS: {task_name}")
    print("="*80)
    
    for result in results:
        print(f"\nModel: {result['model']}")
        print("-" * 30)
        print(f"| Total Requests Executed: {result['requests']}")
        print(f"| Total Wall Time (s):     {result['total_time_s']}")
        print(f"| Average Latency (s):     {result['avg_latency_s']}")
        print(f"| Throughput (Req/s):      {result['throughput_rps']}")
        print(f"| Total Tokens Consumed:   {result['total_tokens']:,}")
        print(f"| Hypothetical Cost ($):   {result['hypothetical_cost']:.6f}")
    
    # Compare the two models for the task
    if len(results) == 2:
        flash_res = results[0] if 'flash' in results[0]['model'].lower() else results[1]
        pro_res = results[0] if 'pro' in results[0]['model'].lower() else results[1]

        # Cost Comparison
        cost_diff = pro_res['hypothetical_cost'] / flash_res['hypothetical_cost']
        print(f"\n[COST ANALYSIS]: Pro model costs {cost_diff:.1f}x more than Flash for this task.")

        # Speed Comparison
        speed_ratio = flash_res['throughput_rps'] / pro_res['throughput_rps']
        print(f"[LATENCY ANALYSIS]: Flash model is {speed_ratio:.1f}x faster (higher throughput) than Pro.")


# --- 5. Main Execution Block ---

def main():
    """
    Runs the full battery of benchmarks for comparison.
    """
    # Define the simulation parameters
    CONCURRENT_REQUESTS = 100
    MAX_WORKERS = 20 # Simulates 20 concurrent threads available in the web server pool

    # --- Scenario 1: High-Volume, Low-Complexity Task (Data Extraction) ---
    print("\n\n################################################################################")
    print("SCENARIO 1: HIGH-VOLUME DATA EXTRACTION (Focus: Latency & Cost)")
    print("################################################################################")
    
    results_simple = []
    
    # Benchmark Flash for the simple task
    flash_simple = benchmark_model_concurrency(
        model_name=FLASH_MODEL,
        prompt=SIMPLE_TASK_PROMPT,
        num_requests=CONCURRENT_REQUESTS,
        max_workers=MAX_WORKERS
    )
    results_simple.append(flash_simple)

    # Benchmark Pro for the simple task (to see the performance penalty)
    pro_simple = benchmark_model_concurrency(
        model_name=PRO_MODEL,
        prompt=SIMPLE_TASK_PROMPT,
        num_requests=CONCURRENT_REQUESTS,
        max_workers=MAX_WORKERS
    )
    results_simple.append(pro_simple)
    
    print_results("Simple Data Extraction (100 Requests)", results_simple)


    # --- Scenario 2: Low-Volume, High-Complexity Task (Reasoning) ---
    print("\n\n################################################################################")
    print("SCENARIO 2: HIGH-COMPLEXITY REASONING (Focus: Quality & Cost)")
    print("################################################################################")
    
    # Since complex reasoning is slower, we might reduce the number of requests to keep the run time reasonable.
    COMPLEX_REQUESTS = 50 
    
    results_complex = []
    
    # Benchmark Flash for the complex task (will likely fail in quality, but we measure speed)
    flash_complex = benchmark_model_concurrency(
        model_name=FLASH_MODEL,
        prompt=COMPLEX_TASK_PROMPT,
        num_requests=COMPLEX_REQUESTS,
        max_workers=MAX_WORKERS
    )
    results_complex.append(flash_complex)

    # Benchmark Pro for the complex task (where it should excel in quality and reasoning)
    pro_complex = benchmark_model_concurrency(
        model_name=PRO_MODEL,
        prompt=COMPLEX_TASK_PROMPT,
        num_requests=COMPLEX_REQUESTS,
        max_workers=MAX_WORKERS
    )
    results_complex.append(pro_complex)
    
    print_results("Complex Legal Reasoning (50 Requests)", results_complex)


if __name__ == "__main__":
    main()


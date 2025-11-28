
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

import asyncio
import time
from typing import Dict, Any, List

# --- Configuration: Simulated Database ---
PRODUCT_DATABASE = {
    "P101": {"name": "Quantum Laptop X", "desc": "High-performance, low-latency machine. Perfect for developers.", "latency": 1.5},
    "P102": {"name": "Ergo Mouse Z", "desc": "Ergonomically designed for comfort. Battery life is questionable.", "latency": 0.8},
    "P103": {"name": "4K Monitor Alpha", "desc": "Stunning visuals and color accuracy. Extremely heavy.", "latency": 2.0},
    # P104 is intentionally missing to simulate a database error
}

# --- Core Asynchronous Functions (Tasks) ---

async def fetch_product_data(product_id: str) -> Dict[str, Any]:
    """
    Simulates an I/O bound operation: fetching product details from an external API/DB.
    Raises an exception if the product is not found, demonstrating task failure.
    """
    if product_id not in PRODUCT_DATABASE:
        await asyncio.sleep(0.5) # Simulate connection delay before failure
        raise ValueError(f"Product ID '{product_id}' not found in database.")
    
    data = PRODUCT_DATABASE[product_id]
    
    # Simulate network latency (I/O wait) based on product data complexity
    await asyncio.sleep(data["latency"]) 
    
    print(f"[{time.strftime('%H:%M:%S')}] Data fetched successfully for {product_id} ({data['name']}).")
    
    return {
        "id": product_id,
        "name": data["name"],
        "description": data["desc"]
    }

async def analyze_description(product_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Simulates a CPU/I/O bound operation: sending a description to an LLM 
    for sentiment analysis and key feature extraction (Tooling simulation).
    """
    description = product_data["description"]
    product_id = product_data["id"]
    
    # Simulate LLM API call latency (typically substantial I/O wait)
    await asyncio.sleep(3.0) 
    
    # Simple simulated LLM output logic
    sentiment = "Positive" if "Perfect" in description or "Stunning" in description else "Mixed"
    key_feature = description.split(',')[0].strip()
    
    print(f"[{time.strftime('%H:%M:%S')}] Analysis complete for {product_id}. Sentiment: {sentiment}")
    
    return {
        "id": product_id,
        "sentiment": sentiment,
        "key_feature": key_feature
    }

# --- Orchestration and Structured Concurrency Management ---

async def orchestrate_comparison(product_ids: List[str]):
    """
    Manages the entire workflow using two stages of asyncio.gather for efficiency.
    Implements structured error handling for reliability.
    """
    start_time = time.monotonic()
    print(f"[{time.strftime('%H:%M:%S')}] Starting data fetching phase...")

    # Phase 1: Concurrent Data Fetching Setup
    fetch_tasks = [fetch_product_data(pid) for pid in product_ids]
    
    fetched_results = []
    analysis_tasks = []
    
    try:
        # EXECUTION POINT 1: Use asyncio.gather for parallel I/O tasks.
        # return_exceptions=True ensures that if P104 fails, P101, P102, and P103 
        # still complete and their results are returned in the `results` list.
        results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        
        print(f"[{time.strftime('%H:%M:%S')}] Data fetching phase completed.")

        # Phase 2: Process results, filter errors, and prepare analysis tasks
        for result in results:
            if isinstance(result, Exception):
                # Structured Concurrency: Log the error but continue processing the successful tasks
                print(f"--- ERROR: Skipping task due to exception: {result}")
                continue
            
            fetched_results.append(result)
            # Create analysis coroutines only for successfully fetched data
            analysis_tasks.append(analyze_description(result))

        if not analysis_tasks:
            print("No valid products fetched. Exiting orchestration.")
            return

        print(f"[{time.strftime('%H:%M:%S')}] Starting concurrent LLM analysis phase...")

        # EXECUTION POINT 2: Use asyncio.gather for parallel LLM processing tasks.
        analysis_results = await asyncio.gather(*analysis_tasks)

        # Phase 3: Aggregate and Report
        final_report = {}
        for fetch_data in fetched_results:
            # We assume order preservation or manually map results for robustness
            analysis_data = next((a for a in analysis_results if a['id'] == fetch_data['id']), {})
            
            final_report[fetch_data['id']] = {
                "name": fetch_data['name'],
                "sentiment": analysis_data.get('sentiment', 'N/A'),
                "feature": analysis_data.get('key_feature', 'N/A')
            }

        print("\n" + "="*50)
        print("FINAL CONCURRENT PROCESSING REPORT")
        print("="*50)
        for pid, data in final_report.items():
            print(f"Product {pid} ({data['name']}):")
            print(f"  -> Sentiment: {data['sentiment']}")
            print(f"  -> Key Feature: {data['feature']}")
        
    except Exception as e:
        # Catch unexpected system errors (e.g., event loop failure)
        print(f"\n[CRITICAL FAILURE] Unhandled system exception during orchestration: {e}")
        
    finally:
        end_time = time.monotonic()
        print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    # P104 is missing, triggering the structured error handling mechanism
    PRODUCTS_TO_COMPARE = ["P101", "P102", "P103", "P104"]
    
    try:
        asyncio.run(orchestrate_comparison(PRODUCTS_TO_COMPARE))
    except KeyboardInterrupt:
        print("Process stopped by user.")

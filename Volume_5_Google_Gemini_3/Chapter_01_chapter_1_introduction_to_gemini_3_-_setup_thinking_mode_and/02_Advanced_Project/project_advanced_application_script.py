
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
import os
from google import genai
from google.genai import types
from typing import Dict, Any

# --- 1. Configuration and Setup ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    # Initialize the Gemini Client
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the 'google-genai' library is installed and your GEMINI_API_KEY is set.")
    exit()

# --- 2. Mock Data for Demonstration ---

# Mock data for the complex, high-reasoning task
COMPLEX_RISK_REPORT = """
FINANCIAL REPORT: Quantum Dynamics (QDX) - Q3 2025
Summary: QDX reported strong revenue growth (22% YoY) driven primarily by its legacy hardware division (70% of total revenue). 
However, the forward-looking statement reveals a critical dependency: 45% of the next quarter's projected revenue relies on a single, 
unpatented AI algorithm (Project Chimera) which is currently in beta testing with a major competitor, 'Aether Corp'. 
Furthermore, the CEO's compensation structure is tied directly to Q4 stock price, creating a potential conflict of interest 
regarding the timely disclosure of Project Chimera's competitive vulnerability.
Balance Sheet Note: The company holds $50M in short-term convertible debt due in 90 days, callable if the stock drops below $150. 
Current stock price: $165. The risk disclosure section (page 42) mentions "unforeseen regulatory shifts in patent law enforcement."
"""

# Mock data for the simple, low-reasoning task
MARKET_HEADLINES = [
    "Tech stocks surge on favorable inflation report.",
    "Oil prices dip slightly after OPEC meeting.",
    "Local bank merger announced, shares up 5%.",
    "New environmental regulations pose long-term threat to manufacturing sector.",
    "Consumer confidence remains high across key demographics."
]


# --- 3. Asynchronous Task Functions ---

async def analyze_risk_high(report_text: str) -> Dict[str, Any]:
    """
    Performs deep, complex analysis using the default (HIGH) thinking level.
    This task prioritizes accuracy and detailed reasoning over speed.
    """
    print("\n[TASK 1: DEEP ANALYSIS] Starting complex risk assessment (Thinking Level: HIGH)...")
    
    # The thinking_level defaults to "high" for gemini-3-pro-preview, 
    # so we omit the config entirely to use the default optimized reasoning.
    prompt = (
        f"Analyze the following financial report excerpt. Identify three specific, non-obvious systemic risks "
        f"and explain the chain of events that could lead to financial instability, referencing specific figures or facts. "
        f"\n\nREPORT:\n{report_text}"
    )

    try:
        # Note: The synchronous genai.Client() methods are wrapped automatically 
        # by the SDK to be non-blocking when run inside an asyncio loop.
        response = await client.models.generate_content_async(
            model="gemini-3-pro-preview",
            contents=prompt,
        )
        
        return {
            "status": "Success",
            "thinking_level": "HIGH (Default)",
            "result": response.text.strip()
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}


async def analyze_sentiment_low(headlines: list[str]) -> Dict[str, Any]:
    """
    Performs rapid, high-throughput summarization using the LOW thinking level.
    This task prioritizes low latency and cost.
    """
    print("[TASK 2: RAPID SENTIMENT] Starting rapid market sentiment check (Thinking Level: LOW)...")
    
    prompt = (
        f"Based ONLY on the following headlines, provide a single-word market sentiment score (Bullish, Bearish, Neutral) "
        f"and a one-sentence justification. \n\nHEADLINES:\n" + "\n".join(headlines)
    )

    try:
        # Explicitly configure the model for low thinking
        low_thinking_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low")
        )

        response = await client.models.generate_content_async(
            model="gemini-3-pro-preview",
            contents=prompt,
            config=low_thinking_config
        )
        
        return {
            "status": "Success",
            "thinking_level": "LOW",
            "result": response.text.strip()
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}


# --- 4. Main Execution and Concurrency Management ---

async def main_concurrent():
    """
    Manages the concurrent execution of both tasks using asyncio.TaskGroup.
    """
    print("--- Gemini 3 Concurrent Reasoning Engine Initialized ---")
    start_time = time.time()
    
    # Use asyncio.TaskGroup (Python 3.11+) for robust concurrent execution
    try:
        async with asyncio.TaskGroup() as tg:
            # Schedule the high-reasoning task
            task_high = tg.create_task(analyze_risk_high(COMPLEX_RISK_REPORT))
            
            # Schedule the low-reasoning task
            task_low = tg.create_task(analyze_sentiment_low(MARKET_HEADLINES))

        # Retrieve results after the TaskGroup completes
        result_high = task_high.result()
        result_low = task_low.result()
        
    except* ExceptionGroup as eg:
        # Handle exceptions from any task within the TaskGroup
        print(f"\nFATAL ERROR: One or more tasks failed during concurrent execution: {eg}")
        return

    end_time = time.time()
    total_duration = end_time - start_time

    # --- 5. Output Results and Analysis ---
    
    print("\n" + "="*80)
    print(f"CONCURRENT EXECUTION COMPLETE | Total Duration: {total_duration:.2f} seconds")
    print("="*80)

    # Display High-Thinking Result
    print("\n[RESULT 1: DEEP ANALYSIS (HIGH THINKING)]")
    print(f"Status: {result_high['status']}")
    print(f"Reasoning Level: {result_high['thinking_level']}")
    print("-" * 30)
    print(result_high['result'])
    
    # Display Low-Thinking Result
    print("\n[RESULT 2: RAPID SENTIMENT (LOW THINKING)]")
    print(f"Status: {result_low['status']}")
    print(f"Reasoning Level: {result_low['thinking_level']}")
    print("-" * 30)
    print(result_low['result'])
    
    print("\n--- Practical Conclusion ---")
    print("Both high-complexity and high-speed tasks were executed simultaneously,")
    print("optimizing overall throughput while ensuring critical analysis received maximum reasoning depth.")


if __name__ == "__main__":
    # Check for API Key before running
    if not os.getenv("GEMINI_API_KEY"):
        print("CRITICAL: The GEMINI_API_KEY environment variable is not set.")
    else:
        asyncio.run(main_concurrent())

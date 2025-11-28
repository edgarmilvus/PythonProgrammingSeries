
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

from google import genai
from google.genai import types
import os
import json
from typing import List, Dict, Any

# --- Configuration and Setup ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Ensure the API key is set: {e}")
    exit()

# 1. Define the Built-in Tools
# We specify the tools the model is allowed to use.
# For built-in tools, we pass an empty dictionary {} as the configuration,
# indicating we accept the default managed settings.
BUILT_IN_TOOLS: List[Dict[str, Any]] = [
    {"google_search": {}},  # Enables real-time web access and grounding
    {"code_execution": {}}  # Enables running Python code for math/logic
]

# --- Core Agent Function ---

def run_dynamic_analyst_agent(prompt: str):
    """
    Sends a prompt to Gemini, enabling built-in tools for dynamic problem-solving.
    """
    print("=" * 70)
    print(f"PROMPT: {prompt}")
    print("-" * 70)

    try:
        # Call the API, passing the list of tools available to the model.
        response = client.models.generate_content(
            model='gemini-2.5-pro',  # Using a powerful model optimized for reasoning and tools
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=BUILT_IN_TOOLS,
                # Set temperature low for factual/analytical tasks
                temperature=0.1
            )
        )

        # 2. Analyze Tool Usage Metadata (Optional but informative)
        # Check if the response contains information about tool usage
        tool_use = response.candidates[0].grounding_metadata.web if response.candidates and response.candidates[0].grounding_metadata else None

        if tool_use:
            print(f"Tool Used: Google Search (Confidence: {tool_use.grounding_chunks_confidence})")
            # Note: Detailed Code Execution steps are often abstracted in the final response metadata,
            # but the model's response text will clearly indicate computation.

        # 3. Print the Final Response
        print("\n--- GEMINI RESPONSE ---")
        print(response.text)
        print("-" * 70)
        
    except Exception as e:
        print(f"\nAn error occurred during API call: {e}")


# --- Demonstration Prompts ---

if __name__ == "__main__":
    
    # SCENARIO 1: Pure Search Requirement (Real-time data)
    # The model must use Google Search to find current, up-to-date information.
    search_prompt = "What were the key announcements from the latest Google I/O developer conference?"
    run_dynamic_analyst_agent(search_prompt)

    # SCENARIO 2: Pure Code Execution Requirement (Complex computation)
    # The model must use the Code Execution tool to guarantee accuracy.
    code_prompt = (
        "I have a principal investment of $15,000. If the interest rate is 7.5% "
        "compounded quarterly for 12 years, what is the final future value? "
        "Show the Python calculation used."
    )
    run_dynamic_analyst_agent(code_prompt)

    # SCENARIO 3: Combined Search and Code Execution (The Complex Analyst Task)
    # The model must first use Google Search to find two data points (historical and current price)
    # and then use Code Execution to calculate the Compound Annual Growth Rate (CAGR).
    combined_prompt = (
        "Calculate the Compound Annual Growth Rate (CAGR) for NVIDIA (NVDA) stock "
        "over the last 5 years. Assume the starting date was exactly 5 years ago. "
        "First, find the closing price 5 years ago and the current price. "
        "Then, use Python to calculate the CAGR. Show the final result and the formula used."
    )
    run_dynamic_analyst_agent(combined_prompt)



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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

import json
import time
from typing import Dict, Any, List

# --- 1. Mock LLM Simulation ---
class MockLLM:
    """
    Simulates an external Language Model API call, mimicking the structure 
    and latency of a real provider (e.g., handling deep JSON responses).
    """
    def __init__(self, model_name: str = "Simulated-GPT-4"):
        # Store the model identifier, useful for logging and multi-model systems
        self.model_name = model_name

    def generate(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Generates a response based on the prompts, simulating API structure and latency.
        This function simulates the expensive network call and processing time.
        """
        print(f"[{self.model_name}] Processing prompt...")
        # Simulate typical network latency and processing delay
        time.sleep(0.1) 

        # --- Internal Logic Simulation ---
        # We check keywords in the prompt to return contextually relevant mock data.
        if "summarize" in user_prompt.lower():
            # Simulated output for the summarization task
            content = (
                "The core concept explained is the necessity of orchestration "
                "frameworks (like LangChain) to manage the complexity arising from "
                "sequential LLM calls, state transfer, and robust error handling "
                "in production AI applications. This complexity necessitates an "
                "abstraction layer."
            )
            
        elif "rewrite" in user_prompt.lower() and "pirate" in user_prompt.lower():
            # Simulated output for the stylistic rewrite task
            content = (
                "Ahoy there, matey! The heart o' the matter be this: we need sturdy "
                "frameworks, like a good ship's rigging, to handle the tricky "
                "business o' sequential calls, passin' the loot (data) between 'em, "
                "and makin' sure the whole voyage doesn't end in a watery grave o' errors. "
                "Aye, that be the orchestration imperative!"
            )
            
        else:
            # Fallback content if the task is unrecognized
            content = "I could not determine the specific task for this simulated LLM call."

        # Simulate the full, deeply nested API response structure, which often 
        # includes metadata, usage metrics, and the actual content buried deep.
        return {
            "id": f"sim-call-{int(time.time() * 1000)}",
            "model": self.model_name,
            "usage": {"prompt_tokens": len(user_prompt), "completion_tokens": len(content)},
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": content
                    },
                    "finish_reason": "stop"
                }
            ]
        }

def extract_content(api_response: Dict[str, Any]) -> str:
    """
    CRITICAL STEP: Helper function to manually parse the deep JSON structure 
    of the API response to retrieve the actual text content.
    """
    try:
        # Navigating the deep structure: choices[0] -> message -> content
        return api_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        # Robust error handling for unexpected API response formats
        print(f"Error parsing API response structure: {e}")
        return "Parsing Error: Could not retrieve content."

# --- 2. The Manual Orchestration Logic ---

def execute_multi_step_reasoning(input_text: str, style: str) -> str:
    """
    Manually executes a two-step reasoning process. This function is the 
    'orchestrator' that we are trying to abstract away.
    """
    print("\n--- Starting Manual Orchestration Process ---")
    # 2a. Initialization: Instantiate the necessary component
    llm = MockLLM()
    
    # --- Step 1: Summarization (First LLM Call) ---
    print("\n[STEP 1/2] Generating Summary...")
    
    # 1a. Prompt Engineering for Step 1
    summary_system_prompt = "You are an expert summarizer. Your goal is to extract the core thesis of the provided text in exactly two sentences."
    summary_user_prompt = f"Please summarize the following text:\n\n---\n{input_text}"
    
    # 1b. Execute the first API call
    raw_summary_response = llm.generate(
        system_prompt=summary_system_prompt, 
        user_prompt=summary_user_prompt
    )
    
    # 1c. Manual Parsing and State Management
    # We must explicitly call the parser to get the clean output.
    summary_result = extract_content(raw_summary_response)
    print(f"Step 1 Complete. Summary Length: {len(summary_result)} characters.")
    
    # 1d. Manual Error/Validation Check
    if "Parsing Error" in summary_result:
        # Crucial: If Step 1 fails, we must manually halt the entire chain.
        return "Orchestration Failed at Step 1: Parsing Error."

    # --- Step 2: Stylistic Rewrite (Second LLM Call) ---
    # The output of Step 1 (`summary_result`) becomes the input for Step 2.
    print("\n[STEP 2/2] Rewriting Summary in specific style...")

    # 2a. Prompt Engineering for Step 2
    rewrite_system_prompt = f"You are a master stylist. Rewrite the provided text in the style of a {style}."
    # CRITICAL STATE TRANSFER: Injecting the intermediate result into the new prompt.
    rewrite_user_prompt = f"Rewrite the following summary in the specified style:\n\n---\n{summary_result}"
    
    # 2b. Execute the second API call
    raw_rewrite_response = llm.generate(
        system_prompt=rewrite_system_prompt,
        user_prompt=rewrite_user_prompt
    )
    
    # 2c. Manual Parsing of the final output
    final_result = extract_content(raw_rewrite_response)

    print("\n--- Manual Orchestration Process Complete ---")
    return final_result

# --- 3. Execution ---
if __name__ == "__main__":
    initial_document = (
        "In the advanced stages of Python development, especially when integrating "
        "Large Language Models (LLMs) into production systems, developers quickly "
        "encounter significant architectural challenges. These challenges include "
        "managing the state across multiple sequential API calls, ensuring robust "
        "input/output parsing, handling complex error propagation, and abstracting "
        "the underlying model providers. Without a dedicated orchestration layer, "
        "the resulting code becomes brittle, tightly coupled, and difficult to maintain. "
        "This necessity drives the adoption of frameworks like LangChain."
    )
    
    target_style = "pirate captain"

    final_output = execute_multi_step_reasoning(initial_document, target_style)
    
    print("\n==========================================")
    print("FINAL ORCHESTRATED OUTPUT (Manual Process):")
    print("==========================================")
    print(final_output)

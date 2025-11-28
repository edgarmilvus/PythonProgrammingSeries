
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

import os
import time
from google import genai
from google.genai import types

# --- Configuration and Setup ---

# Ensure the API key is set in your environment variables
# For production use, always manage keys securely
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

MODEL_NAME = 'gemini-2.5-flash'

# The complex, multi-step problem for the retail audit
PROBLEM_STATEMENT = (
    "A product costs $150. There is a 20% discount applied first, "
    "and then a 5% sales tax is calculated on the discounted price. "
    "What is the final price, rounded to the nearest cent? "
    "Provide only the final numerical value."
)

# --- Strategy 1: Native Reasoning (Zero-Shot) ---

def run_native_reasoning(problem: str):
    """
    Runs the prompt without explicit instructions to show work.
    Relies on Gemini's internal, optimized reasoning.
    """
    print("\n" + "="*50)
    print("STRATEGY 1: NATIVE REASONING (Zero-Shot)")
    print("="*50)
    
    # We use a system instruction to ensure the model adheres strictly to the output format
    system_instruction = "You are an expert financial calculator. Your only output must be the final numerical result of the calculation, with no surrounding text or explanation."
    
    # Start timer for latency measurement
    start_time = time.time()
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=problem,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0 # Low temperature for deterministic math tasks
            )
        )
        
        end_time = time.time()
        
        # Display results
        print(f"Prompt: {problem.split('.')[0]}...")
        print("-" * 20)
        print(f"Final Answer: {response.text.strip()}")
        print(f"Latency: {end_time - start_time:.4f} seconds")
        
        # Display token usage metrics
        usage = response.usage_metadata
        print(f"Tokens Used (Input/Output): {usage.prompt_token_count} / {usage.candidates_token_count}")
        return response.text.strip()

    except Exception as e:
        print(f"An error occurred during Native Reasoning: {e}")
        return None

# --- Strategy 2: Chain of Thought (CoT) ---

def run_chain_of_thought(problem: str):
    """
    Runs the prompt with explicit instructions to perform CoT.
    Forces the model to output intermediate steps before the final answer.
    """
    print("\n" + "="*50)
    print("STRATEGY 2: CHAIN OF THOUGHT (CoT)")
    print("="*50)
    
    # Modify the prompt to enforce explicit, step-by-step reasoning
    cot_prompt = (
        "You are an expert financial calculator. Before providing the final answer, "
        "you must first show the step-by-step calculation, including the discounted price, "
        "the tax amount, and finally the total price. "
        "Finally, provide the final numerical value on a new line, prefixed with 'FINAL RESULT:'"
        f"\n\nQuestion: {problem}"
    )
    
    # Start timer for latency measurement
    start_time = time.time()
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=cot_prompt,
            config=types.GenerateContentConfig(
                temperature=0.0 # Maintain deterministic behavior
            )
        )
        
        end_time = time.time()
        
        # Display results
        print(f"Prompt: {cot_prompt.split('.')[0]}...")
        print("-" * 20)
        print("Model Output (includes reasoning):")
        print(response.text.strip())
        print(f"\nLatency: {end_time - start_time:.4f} seconds")
        
        # Display token usage metrics
        usage = response.usage_metadata
        print(f"Tokens Used (Input/Output): {usage.prompt_token_count} / {usage.candidates_token_count}")
        
        # Extract the final result for comparison
        final_result = [line.split('FINAL RESULT:')[-1].strip() 
                        for line in response.text.split('\n') 
                        if 'FINAL RESULT:' in line]
        return final_result[0] if final_result else "Extraction Error"

    except Exception as e:
        print(f"An error occurred during CoT: {e}")
        return None

# --- Execution and Comparison ---

if __name__ == "__main__":
    
    # Run both strategies
    native_result = run_native_reasoning(PROBLEM_STATEMENT)
    cot_result = run_chain_of_thought(PROBLEM_STATEMENT)

    # Final comparison summary
    print("\n" + "#"*50)
    print("SUMMARY COMPARISON")
    print(f"Native Reasoning Result: {native_result}")
    print(f"Chain of Thought Result: {cot_result}")
    
    # Verify mathematical consistency
    if native_result == cot_result and native_result is not None:
        print("\nConclusion: Both strategies yielded the identical, correct result.")
    else:
        print("\nConclusion: Results differ or an error occurred.")



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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

import os
import time
import json
from google import genai
from google.genai import types

# --- Configuration Setup ---
# Assumes GEMINI_API_KEY is set in your environment
try:
    # Attempt to initialize the client
    # NOTE: In a real environment, the API key should be set via environment variables.
    # client = genai.Client() 
    
    # Using a placeholder initialization method if running locally without environment setup
    if os.getenv("GEMINI_API_KEY"):
        client = genai.Client()
        print("Gemini client initialized successfully.")
    else:
        # Fallback for demonstration if key is missing, but will fail actual API calls
        client = None
        print("WARNING: GEMINI_API_KEY environment variable not set. Client initialization skipped.")

except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

# Helper function to generate content
def generate_response(prompt_text, system_instruction=None, temperature=1.0, max_output_tokens=2048):
    if not client:
        return "Client not initialized due to API key error."
        
    config_params = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens
    }
    
    if system_instruction:
        config_params["system_instruction"] = system_instruction
        
    generation_config = types.GenerateContentConfig(**config_params)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text,
            config=generation_config
        )
        return response.text
    except Exception as e:
        return f"An error occurred during generation: {e}"

print("-" * 50)


### Exercise 1: Enforcing Strict Output Format via System Instructions and Constraints

ex1_system_instruction = (
    "You are a critical system monitoring agent. Your task is to classify incoming event logs into one of three categories: "
    "CRITICAL (immediate action required), WARNING (monitor closely), or INFO (standard operation). "
    "You MUST return the output exclusively as a valid JSON object with the keys 'classification', 'text', and 'confidence'. "
    "The confidence score must be a float between 0.8 and 1.0. Do not include any surrounding markdown (like 
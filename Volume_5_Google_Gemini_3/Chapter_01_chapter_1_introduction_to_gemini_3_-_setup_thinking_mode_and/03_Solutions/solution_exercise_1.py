
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
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import Dict, Any
import time
import json
# Note: For structured output (Ex 4), we simulate the Pydantic schema structure
# as required by the API, avoiding external library dependencies for simplicity.

# --- Setup and Initialization ---
# Ensure the GEMINI_API_KEY environment variable is set securely.

try:
    # 1. Initialize the Client
    client = genai.Client()
    MODEL_ID = "gemini-3-pro-preview"
    print("--- Gemini 3 Client Initialized Successfully ---")
except Exception as e:
    print(f"Error initializing client. Check API key setup: {e}")
    # In a real environment, you might raise or exit here.
    # For this exercise, we assume success to run the following blocks.
    client = None

if client:
    
    # --- Exercise 1: Validating Setup and Observing High Thinking Mode (Default) ---
    print("\n--- Exercise 1: Default High Thinking Mode (Advanced Reasoning) ---")

    high_thinking_prompt = (
        "Analyze the following multi-threaded C++ snippet designed for concurrent data processing. "
        "Identify the exact location and nature of the race condition, and suggest a fix using "
        "a standard C++ synchronization primitive. Be thorough and provide detailed reasoning."
    )

    start_time_high = time.time()
    try:
        # No config parameter means thinking_level defaults to 'high'
        response_high = client.models.generate_content(
            model=MODEL_ID,
            contents=high_thinking_prompt,
        )
        duration_high = time.time() - start_time_high
        print(f"Result (High Thinking, Default):")
        print(f"Response received in {duration_high:.2f} seconds.")
        print(response_high.text[:300].replace('\n', ' ') + "...") 
        print(f"(Expected: Detailed analysis, higher latency.)")
    except APIError as e:
        print(f"API Error during High Thinking call: {e}")


    # --- Exercise 2: Implementing Low Thinking for High Throughput ---
    print("\n--- Exercise 2: Explicit Low Thinking Mode (High Throughput) ---")

    low_thinking_prompt = "What is the capital of France, and what is the primary river that flows through it? Answer concisely."

    # 1. Define the ThinkingConfig for 'low'
    low_thinking_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    )

    start_time_low = time.time()
    try:
        # 2. Pass the explicit low configuration
        response_low = client.models.generate_content(
            model=MODEL_ID,
            contents=low_thinking_prompt,
            config=low_thinking_config,
        )
        duration_low = time.time() - start_time_low
        print(f"Result (Low Thinking):")
        print(f"Response received in {duration_low:.2f} seconds.")
        print(response_low.text)
        print(f"(Expected: Fast, concise answer. Latency {duration_low:.2f}s should be lower than {duration_high:.2f}s.)")
    except APIError as e:
        print(f"API Error during Low Thinking call: {e}")


    # --- Exercise 3: Defensive Programming with EAFP (Easier to Ask for Forgiveness) ---
    print("\n--- Exercise 3: EAFP for Invalid Configuration Handling ---")

    def attempt_invalid_call(client: genai.Client):
        """
        Attempts a call designed to fail due to an invalid configuration 
        (simulating the documented thinking_level/thinking_budget conflict or 
        a non-existent model error) and handles the APIError gracefully.
        """
        # We intentionally use a non-existent model ID to guarantee an APIError (404/400).
        # This demonstrates the EAFP pattern for handling remote configuration/setup errors.
        
        try:
            print("Attempting call with intentionally invalid model ID...")
            
            client.models.generate_content(
                model="gemini-3-nonexistent-model-trigger-error", 
                contents="This prompt should fail validation.",
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="low")
                )
            )
            print("EAFP Check: Call succeeded (unexpectedly).")

        except APIError as e:
            # Forgiveness: Catch the specific API exception (e.g., 400 Bad Request or 404 Not Found)
            print("--- EAFP Success ---")
            print(f"Caught expected API Error: {type(e).__name__}")
            print(f"Error Detail Snippet: {str(e)[:100]}...")
            print("\nAction taken: The program successfully caught the remote configuration/setup error (simulating the thinking_level conflict) and handled the failure gracefully without crashing.")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"EAFP Failure: Caught unexpected local error: {type(e).__name__}: {e}")

    attempt_invalid_call(client)


    # --- Exercise 4: Advanced Configuration Merging using dict.update() ---
    print("\n--- Exercise 4: Dynamic Configuration Merging (Tools + Thinking Level) ---")

    # Hypothetical JSON Schema structure (as required by the API)
    HYPOTHETICAL_JSON_SCHEMA: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "query_summary": {"type": "string", "description": "A brief summary of the search result."},
            "data_source": {"type": "string", "description": "The tool used to find the data (e.g., Google Search)."}
        },
        "required": ["query_summary", "data_source"]
    }

    # 1. Base Configuration (Tools and Structured Output)
    base_config_dict: Dict[str, Any] = {
        "tools": [
            {"google_search": {}}, # Enable Google Search grounding
        ],
        "response_mime_type": "application/json",
        "response_json_schema": HYPOTHETICAL_JSON_SCHEMA,
    }

    # 2. Thinking Override (We want to set the thinking level dynamically to 'high')
    # Note: We must instantiate the nested object first.
    thinking_override: Dict[str, Any] = {
        "thinking_config": types.ThinkingConfig(thinking_level="high")
    }

    print(f"Initial base config keys: {list(base_config_dict.keys())}")

    # 3. Use dict.update() to merge the thinking configuration
    base_config_dict.update(thinking_override)

    print(f"Merged config keys: {list(base_config_dict.keys())}")

    # 4. Instantiate the final GenerateContentConfig object using dictionary unpacking
    final_config = types.GenerateContentConfig(**base_config_dict)

    advanced_prompt = "Using the search tool, what was the biggest news event of the last 24 hours?"

    try:
        print("Executing complex call with merged configuration (High Thinking + Google Search + JSON Schema)...")
        
        response_advanced = client.models.generate_content(
            model=MODEL_ID,
            contents=advanced_prompt,
            config=final_config,
        )
        
        print("\nResponse (Structured JSON):")
        # Validate that the response is JSON and conforms to the schema
        parsed_json = json.loads(response_advanced.text)
        print(json.dumps(parsed_json, indent=2))
        print(f"\nConfiguration Check: Successfully used 'high' thinking level and structured output/tools.")
        
    except APIError as e:
        print(f"API Error during Advanced Merged Configuration call: {e}")
    except json.JSONDecodeError:
        print("Error: Response was not valid JSON, indicating a failure in structured output.")

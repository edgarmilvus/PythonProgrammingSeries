
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

# Source File: theory_theoretical_foundations_part3.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
from google.genai import types
import os
from typing import Optional

# --- Configuration Constants ---
GEMINI_MODEL = "gemini-3-pro-preview"

# --- 1. Client Initialization (EAFP Principle) ---
# The client assumes the GEMINI_API_KEY is set in the environment.
# We will use a try-except block to demonstrate robust initialization 
# (although the SDK handles the environment check internally).
def initialize_client() -> Optional[genai.Client]:
    """Initializes the Gemini client, handling potential API key errors."""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            print("Warning: GEMINI_API_KEY environment variable not set.")
            # The client will raise an error internally if the key is missing 
            # and an API call is made, but we proceed for demonstration.
        
        # Initialize the client. The default API version is v1beta.
        client = genai.Client()
        print("Client initialized successfully.")
        return client
    except Exception as e:
        print(f"Error initializing client: {e}")
        return None

client = initialize_client()

if client:
    # --- 2. Default (High) Thinking Mode ---
    # When no config is provided, Gemini 3 Pro defaults to high reasoning depth.
    print("\n--- Running in Default (High) Thinking Mode ---")
    print("Task: Complex reasoning (finding a race condition).")
    
    # Example C++ snippet requiring deep analysis
    cpp_snippet = """
    #include <iostream>
    #include <thread>
    #include <mutex>

    int counter = 0;
    std::mutex mtx;

    void increment() {
        for (int i = 0; i < 10000; ++i) {
            // Missing lock here!
            counter++;
        }
    }

    int main() {
        std::thread t1(increment);
        std::thread t2(increment);

        t1.join();
        t2.join();

        // The expected value is 20000, but the output will be less due to the race condition.
        std::cout << "Final counter: " << counter << std::endl;
        return 0;
    }
    """
    
    # No config parameter means thinking_level="high"
    response_high = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"Find the race condition in this multi-threaded C++ snippet: {cpp_snippet}",
    )
    
    print("\nModel Response (High Thinking):\n" + response_high.text[:400] + "...")


    # --- 3. Low Thinking Mode Configuration ---
    # Explicitly constraining the model for speed and low cost.
    print("\n--- Running in Low Thinking Mode ---")
    print("Task: Simple instruction following (definition).")
    
    # Define the configuration object to set the thinking level to 'low'
    low_thinking_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="low"
        )
    )

    response_low = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Define the concept of dynamic thinking in AI in two sentences.",
        config=low_thinking_config,
    )

    print("\nModel Response (Low Thinking):\n" + response_low.text)

    # --- 4. Structured Output Example (Conceptual) ---
    # Demonstrating the use of Pydantic for guaranteed JSON output 
    # combined with a tool (Google Search).
    try:
        from pydantic import BaseModel, Field
        from typing import List

        class SimpleSummary(BaseModel):
            topic: str = Field(description="The main topic of the query.")
            summary_sentence: str = Field(description="A concise summary sentence.")
            
        print("\n--- Conceptual Structured Output Setup ---")
        
        # The configuration structure required for structured output
        structured_config = {
            "tools": [
                {"google_search": {}} # Using a tool
            ],
            "response_mime_type": "application/json",
            "response_json_schema": SimpleSummary.model_json_schema(),
        }

        print(f"Structured Output Config (JSON Schema):\n{structured_config['response_json_schema']}")
        print("Note: This request combines advanced reasoning (Gemini 3), a tool (Google Search), and guaranteed output format (JSON Schema).")

    except ImportError:
        print("\nSkipping Pydantic setup demo. Install 'pydantic' to use structured output.")

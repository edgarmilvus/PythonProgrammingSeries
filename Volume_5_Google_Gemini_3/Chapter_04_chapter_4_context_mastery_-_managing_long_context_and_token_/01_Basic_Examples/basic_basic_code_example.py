
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
import textwrap
import random
import string
from google import genai
from google.genai.errors import APIError

# --- Configuration and Setup ---

# 1. Initialize the Gemini Client.
# Assumes GEMINI_API_KEY is set in the environment variables.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is configured correctly.")
    exit()

# We select a powerful model suitable for long-context reasoning.
MODEL_NAME = 'gemini-2.5-pro' 

# Target size for the context window simulation (in characters).
# This simulates a document that would consume hundreds of thousands of tokens.
TARGET_CONTEXT_CHARS = 500000 

# The critical piece of information (the "needle") we want the model to find.
NEEDLE_FACT = "The official corporate mascot, which was adopted in 2024 after a board vote, is named 'Sir Reginald Fluffington III', and his favorite food is artisanal salmon."

# --- Context Generation Functions ---

def generate_filler_text(length):
    """Generates random, repetitive text to simulate a large document."""
    words = ["protocol", "compliance", "synergy", "optimization", "framework", "governance", "stakeholder", "implementation", "documentation", "retrieval", "architecture", "strategy", "deployment", "integration"]
    # Create a stream of random words
    filler = ' '.join(random.choice(words) for _ in range(length // 10))
    # Ensure the text is long enough
    return filler[:length]

def generate_massive_context(target_length):
    """
    Creates a simulated massive document with the 'needle' buried deep inside.
    We place the needle near the middle of the document to test the model's 
    ability to retrieve non-local information.
    """
    print(f"Generating massive context, targeting ~{target_length:,} characters...")
    
    # Calculate insertion point (e.g., 40% of the way through)
    insertion_index = int(target_length * 0.4)
    
    # Generate the first part of the text
    text_part_1 = generate_filler_text(insertion_index)
    
    # Insert the needle fact, surrounded by padding for realism
    padded_needle = "\n\n--- CRITICAL SECTION 304.B ---\n" + NEEDLE_FACT + "\n--- END CRITICAL SECTION ---\n\n"
    
    # Calculate remaining length needed
    remaining_length = target_length - len(text_part_1) - len(padded_needle)
    
    # Generate the second part of the text
    text_part_2 = generate_filler_text(remaining_length)
    
    # Combine the parts
    full_context = text_part_1 + padded_needle + text_part_2
    
    print(f"Context generated. Total characters: {len(full_context):,}")
    return full_context

# --- Main Execution Logic ---

def run_long_context_retrieval():
    """
    Executes the long-context query by passing the massive text directly to the model.
    """
    
    # 1. Generate the simulated document
    document_context = generate_massive_context(TARGET_CONTEXT_CHARS)
    
    # 2. Define the specific question (The Query)
    # CRITICAL: Per best practices, the query should be placed at the end 
    # of the prompt after all the context has been provided.
    question = (
        "\n\n--- ANALYST QUERY ---\n"
        "Based ONLY on the preceding massive corporate document, what is the name "
        "of the official corporate mascot and what is its favorite food? "
        "Respond concisely with only the mascot's name and food, separated by a comma."
    )
    
    # 3. Combine the document and the query into a single, massive prompt
    full_prompt = document_context + question
    
    print(f"\nSending prompt to {MODEL_NAME}...")
    print(f"Estimated Input Token Count: (Varies, but > 100,000 tokens)")

    try:
        # 4. Call the Gemini API for generation
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.0 # Use low temperature for factual retrieval
            )
        )

        # 5. Display the results
        print("\n" + "="*50)
        print("✅ SUCCESS: Retrieval from Massive Context")
        print("="*50)
        print(f"Model Used: {MODEL_NAME}")
        print(f"Input Character Length: {len(full_prompt):,}")
        print(f"Extracted Answer: {response.text.strip()}")
        print("="*50)
        
        # Optional: Display token usage metrics if available (requires API response parsing)
        # Note: Token counting is crucial for cost management in long context usage.
        if response.usage_metadata:
            print(f"Token Usage Summary:")
            print(f"  Prompt Tokens: {response.usage_metadata.prompt_token_count}")
            print(f"  Response Tokens: {response.usage_metadata.candidates_token_count}")
            print(f"  Total Tokens: {response.usage_metadata.total_token_count}")
        
    except APIError as e:
        print(f"\n[API ERROR] Failed to complete generation: {e}")
        print("Check if the model name is correct and if the API key is valid.")
    except Exception as e:
        print(f"\n[GENERAL ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_long_context_retrieval()

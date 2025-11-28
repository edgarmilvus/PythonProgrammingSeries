
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
from google import genai
from google.genai import types

# --- 1. Setup and Initialization ---

# Ensure your GEMINI_API_KEY is set as an environment variable
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is correctly configured.")
    exit()

MODEL_NAME = "gemini-2.5-flash"

# --- 2. Define the Grounding Tool ---

# The Google Search tool is defined using the types.Tool object.
# This structure exposes the external capability (Google Search) to the model.
# The internal object types.GoogleSearch() is an empty configuration object,
# indicating we want the default, automatic search behavior.
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# --- 3. Configure the Generation Request ---

# The tools must be passed to the model via the GenerateContentConfig object.
# The 'tools' parameter expects a list, allowing for future expansion to
# multiple tools (e.g., search + custom functions).
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# --- 4. Define the Time-Sensitive Prompt ---

# We ask a question that requires knowledge beyond the model's training cutoff.
PROMPT = "Who won the most recent major global chess tournament and what country are they from?"

print(f"--- Querying Model ({MODEL_NAME}) with Search Grounding Enabled ---")
print(f"Prompt: {PROMPT}\n")

# --- 5. Generate Content and Enable Grounding ---

# The config object containing the tool is passed into the API call.
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=PROMPT,
    config=config,
)

# --- 6. Process and Display Results ---

# The primary response text
print("--- Model Response (Grounded) ---")
print(response.text)
print("-" * 40)

# Check for grounding metadata to confirm the search was executed
if response.candidates and response.candidates[0].grounding_metadata:
    metadata = response.candidates[0].grounding_metadata

    print("\n--- Grounding Verification (Proof of Search) ---")

    # Display the specific search queries the model generated automatically
    if metadata.web_search_queries:
        print("Search Queries Used:")
        for query in metadata.web_search_queries:
            print(f"  - {query}")

    # Display the sources (chunks) the model used to synthesize the answer
    if metadata.grounding_chunks:
        print("\nTop Web Sources Used for Grounding:")
        for i, chunk in enumerate(metadata.grounding_chunks):
            # The chunk object contains the source URI and Title
            if chunk.web:
                print(f"  [{i+1}] Title: {chunk.web.title}")
                print(f"      URI: {chunk.web.uri}")

else:
    print("\n[WARNING] No Grounding Metadata found. The model may have answered from internal knowledge.")

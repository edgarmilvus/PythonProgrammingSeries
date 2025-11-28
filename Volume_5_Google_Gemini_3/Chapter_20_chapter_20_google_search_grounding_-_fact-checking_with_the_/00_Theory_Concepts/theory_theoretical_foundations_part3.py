
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

import os
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import Optional, List, Dict, Any

# --- 1. Client Setup and Configuration ---

# Assume the GOOGLE_API_KEY environment variable is set
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    # In a real application, handle API key missing gracefully

MODEL_ID = "gemini-2.5-flash"

# 1. Define the Google Search Tool
# This object tells the model that it has access to real-time search capabilities.
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# 2. Define the configuration to include the tool
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

def generate_grounded_content(prompt: str, model: str = MODEL_ID) -> Optional[types.GenerateContentResponse]:
    """
    Sends a prompt to the Gemini API with the Google Search tool enabled.
    """
    print(f"--- Sending Prompt: '{prompt}' to {model} (Grounding Enabled) ---")
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        return response
    except APIError as e:
        print(f"An API error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# --- 2. Citation Parsing Engine ---

def add_citations(response: types.GenerateContentResponse) -> str:
    """
    Processes the groundingMetadata to insert inline, clickable citations
    into the model's response text.

    This function relies on the critical step of sorting supports in reverse
    order by end_index to prevent index shifting during string modification.
    """
    if not response.candidates:
        return response.text if response.text else "No response candidates found."
        
    candidate = response.candidates[0]
    text = response.text
    
    # EAFP principle: Check if grounding metadata exists before proceeding
    if not candidate.grounding_metadata:
        print("Warning: No grounding metadata found. Returning raw text.")
        return text

    metadata = candidate.grounding_metadata
    
    # Ensure necessary components exist
    if not metadata.grounding_supports or not metadata.grounding_chunks:
        print("Warning: Missing grounding supports or chunks. Returning raw text.")
        return text

    supports = metadata.grounding_supports
    chunks = metadata.grounding_chunks

    # CRITICAL STEP: Sort supports by end_index in descending order.
    # This prevents subsequent insertions from invalidating earlier indices.
    sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    for support in sorted_supports:
        # Use EAFP style access, providing defaults if segment or indices are missing
        end_index = getattr(support.segment, 'end_index', None)
        chunk_indices = getattr(support, 'grounding_chunk_indices', [])
        
        if end_index is None or not chunk_indices:
            continue

        citation_links = []
        
        # Iterate through the indices that support this text segment
        for i in chunk_indices:
            # LBYL check to ensure the index is valid for the chunks list
            if i < len(chunks):
                # Use EAFP for deeply nested web URI access
                try:
                    uri = chunks[i].web.uri
                    # Citation format: [Index + 1](URL)
                    citation_links.append(f"[{i + 1}]({uri})")
                except AttributeError:
                    # Handle case where chunk or web/uri structure is missing
                    print(f"Skipping citation for index {i}: URI not found.")
                    continue

        if citation_links:
            citation_string = ", ".join(citation_links)
            
            # Insert the citation string at the specified end_index
            text = text[:end_index] + citation_string + text[end_index:]

    return text

# --- 3. Example Execution (Illustrative) ---

# Example prompt requiring real-time data
# response_obj = generate_grounded_content("Who won the 2024 F1 Grand Prix in Monza?")
# 
# if response_obj:
#     print("\n--- Raw Response Text ---")
#     print(response_obj.text)
#     
#     # Display the generated search queries for debugging
#     if response_obj.candidates and response_obj.candidates[0].grounding_metadata:
#         queries = response_obj.candidates[0].grounding_metadata.web_search_queries
#         print(f"\nSearch Queries Used: {queries}")
#         
#     # Generate and print the text with inline citations
#     text_with_citations = add_citations(response_obj)
#     print("\n--- Grounded Response with Inline Citations ---")
#     print(text_with_citations)


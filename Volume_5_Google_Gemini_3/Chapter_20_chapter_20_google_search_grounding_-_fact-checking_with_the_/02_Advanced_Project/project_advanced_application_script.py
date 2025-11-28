
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

import os
from google import genai
from google.genai import types
from typing import Dict, List, Any

# --- Configuration and Initialization ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Is the API key set? Details: {e}")
    exit()

# Define the model to use. Gemini 2.5 Flash supports the google_search tool.
MODEL_NAME = "gemini-2.5-flash"

# 1. Function to insert inline citations into the text
# This function is critical for linking specific text segments to their sources.
def add_inline_citations(response: types.GenerateContentResponse) -> str:
    """
    Processes the grounding metadata to insert markdown-formatted inline citations
    [N](URI) into the model's response text.

    Args:
        response: The Gemini API response object containing grounding_metadata.

    Returns:
        The response text with inline citations inserted.
    """
    # Check if grounding metadata exists
    if not response.candidates or not response.candidates[0].grounding_metadata:
        return response.text

    text = response.text
    metadata = response.candidates[0].grounding_metadata
    supports = metadata.grounding_supports
    chunks = metadata.grounding_chunks

    # CRITICAL: Sort supports by end_index in descending order.
    # This prevents index shifting issues. If we insert citations at the start
    # first, all subsequent end_indices become incorrect. Sorting descendingly
    # ensures insertions happen from the end of the string backwards.
    sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    for support in sorted_supports:
        end_index = support.segment.end_index
        
        # Check if the support segment actually links to any chunk indices
        if support.grounding_chunk_indices:
            citation_links = []
            
            # Iterate through the indices linked to this text segment
            for i in support.grounding_chunk_indices:
                if i < len(chunks):
                    # Grounding chunks contain the actual source information (URI, title)
                    uri = chunks[i].web.uri
                    # Create citation string: [Index + 1](URI)
                    citation_links.append(f"[{i + 1}]({uri})")

            # Join all citation links for this segment (e.g., "[1](link1), [2](link2)")
            citation_string = ", ".join(citation_links)
            
            # Insert the citation string at the segment's end index
            text = text[:end_index] + citation_string + text[end_index:]

    return text

# 2. Function to extract and format a clean list of all sources
def extract_and_format_sources(response: types.GenerateContentResponse) -> List[Dict[str, Any]]:
    """
    Extracts the unique web sources (grounding chunks) and formats them into a list.
    """
    if not response.candidates or not response.candidates[0].grounding_metadata:
        return []

    metadata = response.candidates[0].grounding_metadata
    chunks = metadata.grounding_chunks
    
    formatted_sources = []
    
    # Iterate through each grounding chunk to extract source details
    for i, chunk in enumerate(chunks):
        if chunk.web:
            source_info = {
                "index": i + 1,
                "title": chunk.web.title,
                "uri": chunk.web.uri,
            }
            formatted_sources.append(source_info)
            
    return formatted_sources

# 3. Main function to execute the grounded generation
def get_grounded_response(prompt: str) -> types.GenerateContentResponse:
    """
    Sends a prompt to Gemini with the Google Search tool enabled.
    """
    print(f"--- Sending Prompt to Gemini ({MODEL_NAME}) ---")
    print(f"Query: {prompt}\n")
    
    # Define the Google Search tool configuration
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    # Configure the generation request to include the tool
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    # Execute the API call
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    
    return response

# --- Execution Block ---

if __name__ == "__main__":
    # A time-sensitive query requiring external, real-time grounding
    news_query = (
        "Provide a summary of the latest major developments regarding the "
        "global semiconductor supply chain crisis, focusing on the current "
        "inventory levels and projected recovery timeline."
    )

    # 1. Get the grounded response from Gemini
    gemini_response = get_grounded_response(news_query)

    # 2. Process the text to add inline citations
    final_summary_text = add_inline_citations(gemini_response)

    # 3. Extract and format the source list
    source_list = extract_and_format_sources(gemini_response)
    
    # 4. Extract search queries used by the model (for debugging/transparency)
    search_queries = []
    if gemini_response.candidates and gemini_response.candidates[0].grounding_metadata:
        search_queries = gemini_response.candidates[0].grounding_metadata.web_search_queries

    # --- Output the Results ---
    
    print("\n" + "="*80)
    print("      REAL-TIME NEWS VERIFICATION ENGINE RESULTS")
    print("="*80)
    
    # Display the search queries the model decided to execute
    if search_queries:
        print("\n[A] MODEL'S GROUNDING STRATEGY (Search Queries Executed):")
        for q in search_queries:
            print(f"- {q}")
        print("-" * 40)
        
    # Display the final summary with embedded citations
    print("\n[B] GROUNDED SUMMARY (with Inline Citations):")
    print(final_summary_text)
    
    # Display the formatted list of verifiable sources
    if source_list:
        print("\n\n[C] VERIFIED SOURCE AUDIT TRAIL:")
        for source in source_list:
            print(f"  [{source['index']}] {source['title']}")
            print(f"      URI: {source['uri']}")
    else:
        print("\n[C] No grounding metadata found. Response may be based on internal knowledge.")
    
    print("\n" + "="*80)


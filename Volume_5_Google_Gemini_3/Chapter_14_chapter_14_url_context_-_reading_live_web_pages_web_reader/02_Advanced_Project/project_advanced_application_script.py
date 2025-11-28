
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
import json
from google import genai
from google.genai.types import GenerateContentConfig, Tool
from typing import List, Dict, Any

# --- Configuration and Setup ---

# 1. Initialize the client using the GEMINI_API_KEY environment variable.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Ensure GEMINI_API_KEY is set. Error: {e}")
    exit()

MODEL_ID = "gemini-2.5-flash" # A powerful and cost-effective model supporting tools

# Define the URLs for deep analysis (using reliable examples from documentation)
RECIPE_URL_1 = "https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592"
RECIPE_URL_2 = "https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/"
TARGET_URLS = [RECIPE_URL_1, RECIPE_URL_2]

def perform_deep_web_analysis(urls: List[str], prompt: str) -> Dict[str, Any]:
    """
    Performs content generation using both URL Context and Google Search tools.

    Args:
        urls: A list of specific URLs for deep context retrieval.
        prompt: The instruction for the model.

    Returns:
        A dictionary containing the response text and metadata.
    """
    print(f"--- Starting Analysis on {len(urls)} URLs ---")

    # 2. Configure the Tools: URL Context for deep reading, Google Search for grounding.
    # Note: The URLs are embedded directly into the prompt string.
    tools: List[Tool] = [
        {"url_context": {}},  # Enable the URL Context tool
        {"google_search": {}} # Enable the Google Search tool for real-time grounding
    ]

    # Combine URLs into a string for the prompt insertion
    url_list_str = "\n".join(urls)
    
    # Construct the final content string
    full_contents = f"{prompt}\n\nAnalyze the following URLs for context:\n{url_list_str}"

    # 3. Create the GenerateContentConfig object
    config = GenerateContentConfig(
        tools=tools,
    )

    try:
        # 4. Execute the API call
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=full_contents,
            config=config
        )

        # 5. Extract results and metadata
        result = {
            "text": response.text,
            "url_metadata": getattr(response.candidates[0], 'url_context_metadata', None),
            "usage_metadata": response.usage_metadata,
        }
        return result

    except Exception as e:
        print(f"\n[ERROR] An API call failed: {e}")
        return {"text": "API call failed.", "url_metadata": None, "usage_metadata": None}

# --- Main Execution Block ---

if __name__ == "__main__":
    # The complex prompt requiring synthesis, comparison, and external search
    analysis_prompt = (
        "You are a culinary analyst. Based on the two provided roast chicken recipes, "
        "perform a comparative analysis. Specifically, synthesize a report addressing "
        "the following three points: "
        "1. **Efficiency for a Novice:** Which recipe requires simpler ingredients and less complex preparation steps? "
        "2. **Flavor Profile:** Compare the herb and spice usage. Which recipe is designed for a richer, more complex flavor? "
        "3. **External Tip Integration:** Use the Google Search tool to find the single best tip for achieving the crispiest chicken skin, and integrate that tip at the end of your report."
    )

    analysis_result = perform_deep_web_analysis(TARGET_URLS, analysis_prompt)

    print("\n" + "="*80)
    print("           COMPREHENSIVE WEB DATA SYNTHESIS REPORT (GEMINI-POWERED)         ")
    print("="*80 + "\n")

    # 6. Display the synthesized analysis
    print("--- 1. Generated Synthesis Report ---")
    print(analysis_result["text"])
    print("\n" + "-"*40)

    # 7. Display URL Context Verification Metadata
    print("\n--- 2. URL Retrieval Status (Verification) ---")
    url_meta = analysis_result["url_metadata"]
    if url_meta and url_meta.url_metadata:
        for item in url_meta.url_metadata:
            status_color = "\033[92m" if item.url_retrieval_status == "URL_RETRIEVAL_STATUS_SUCCESS" else "\033[91m"
            print(f"  [STATUS: {status_color}{item.url_retrieval_status}\033[0m] URL: {item.retrieved_url}")
    else:
        print("  No URL context metadata found or tool was not used.")
    print("-" * 40)

    # 8. Display Token Usage and Cost Transparency
    print("\n--- 3. Token Usage and Cost Transparency ---")
    usage_meta = analysis_result["usage_metadata"]
    if usage_meta:
        print(f"  Total Tokens Consumed (Input + Output): {usage_meta.total_token_count}")
        print(f"  Prompt Tokens (User Request): {usage_meta.prompt_token_count}")
        print(f"  Tool Use Tokens (URL Content + Search Query): {usage_meta.tool_use_prompt_token_count}")
        print(f"  Candidates Tokens (Model Response): {usage_meta.candidates_token_count}")
        print("\n  *Note: The Tool Use Tokens represent the costliest part, including the raw text retrieved from the live URLs.")
    print("="*80)


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
import json
from google import genai
from google.genai.types import GenerateContentConfig

# --- Configuration ---
# Ensure the GEMINI_API_KEY environment variable is set
try:
    # Initialize the client. It automatically picks up the API key from environment variables.
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is configured correctly.")
    # In a real environment, you might exit here, but for a complete solution, we continue.

MODEL_ID = "gemini-2.5-flash"

# --- Utility Function for Metadata Check ---
def print_metadata(response):
    """Prints the retrieval status for all URLs used in the request."""
    print("\n--- URL CONTEXT METADATA VERIFICATION ---")
    try:
        # Access the metadata structure provided by the API
        metadata = response.candidates[0].url_context_metadata
        if metadata and metadata.url_metadata:
            for item in metadata.url_metadata:
                print(f"  URL: {item.retrieved_url}")
                print(f"  Status: {item.url_retrieval_status}")
        else:
            print("  No URL context metadata found.")
    except (AttributeError, IndexError):
        print("  Error accessing URL context metadata.")
    print("----------------------------------------")


# --- Exercise 1: The Single-Page Deep Dive and Verification ---
def exercise_1_single_page_summary():
    print("\n\n===== EXERCISE 1: SINGLE-PAGE DEEP DIVE AND VERIFICATION =====")
    
    # Target URL for deep analysis
    target_url = "https://en.wikipedia.org/wiki/Large_Language_Model"
    
    prompt = (
        f"Analyze the article at the following URL: {target_url}. "
        "Provide a concise summary of the article, and specifically extract "
        "the year the first transformer model was introduced, the name of the "
        "paper, and the primary benefit of the attention mechanism described."
    )
    
    # Configure the URL Context tool
    tools = [
      {"url_context": {}},
    ]

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=GenerateContentConfig(
                tools=tools,
            )
        )
        
        print("\n--- Gemini Summary and Key Findings ---")
        for part in response.candidates[0].content.parts:
            print(part.text)
        
        # Verification Step 4: Check metadata
        print_metadata(response)

    except Exception as e:
        print(f"An error occurred in Exercise 1: {e}")


# --- Exercise 2: Comparative Analysis of Multiple Live Sources ---
def exercise_2_comparative_analysis():
    print("\n\n===== EXERCISE 2: COMPARATIVE ANALYSIS OF MULTIPLE LIVE SOURCES =====")
    
    # Two distinct URLs for comparison
    url_a = "https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592"
    url_b = "https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/"
    
    prompt = (
        f"Compare the recipes at {url_a} and {url_b}. "
        "Create a Markdown table comparing the primary seasonings used, "
        "the total estimated cooking time, and the suggested serving size for each."
    )
    
    tools = [
      {"url_context": {}},
    ]

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=GenerateContentConfig(
                tools=tools,
            )
        )
        
        print("\n--- Comparative Analysis Table (Markdown) ---")
        for part in response.candidates[0].content.parts:
            print(part.text)
        
        print_metadata(response)

    except Exception as e:
        print(f"An error occurred in Exercise 2: {e}")


# --- Exercise 3: The Advanced Challenge: Live Event Planning with Grounding ---
def exercise_3_advanced_grounding():
    print("\n\n===== EXERCISE 3: ADVANCED CHALLENGE (URL CONTEXT + GOOGLE SEARCH) =====")
    
    # Using a recent tech news URL as a stand-in for an event schedule
    event_url = "https://www.theverge.com/24169727/google-io-2024-announcements-recap-ai-search-android"
    
    prompt = (
        f"Based on the event recap at {event_url}, summarize the three most important "
        "AI announcements. Additionally, use Google Search to provide a brief "
        "advisory on the current weather and any major public transit delays "
        "in Mountain View, California today."
    )
    
    # CRITICAL: Enabling both tools simultaneously
    tools = [
          {"url_context": {}},
          {"google_search": {}}
      ]

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=GenerateContentConfig(
                tools=tools,
            )
        )
        
        print("\n--- Combined Analysis (URL Content + Live Search) ---")
        for part in response.candidates[0].content.parts:
            print(part.text)
        
        # Check metadata for URL retrieval success
        print_metadata(response) 

    except Exception as e:
        print(f"An error occurred in Exercise 3: {e}")


# --- Exercise 4: Robustness Check: Analyzing Retrieval Status Codes ---
def exercise_4_robustness_check():
    print("\n\n===== EXERCISE 4: ROBUSTNESS CHECK (ANALYZING STATUS CODES) =====")
    
    # List of URLs including valid and intentionally invalid/inaccessible ones
    test_urls = [
        "https://ai.google.dev/gemini-api/docs/url-context", # Valid documentation page
        "https://example.com/nonexistent-page-123",         # Placeholder for a likely 404/failure
        "https://www.nasa.gov/general-info"                 # Another valid page
    ]
    
    # Constructing a prompt that includes all test URLs
    prompt = (
        "Please analyze the content of the following pages and provide a one-sentence "
        "summary for each. The URLs are: " + ", ".join(test_urls)
    )
    
    tools = [
      {"url_context": {}},
    ]

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=GenerateContentConfig(
                tools=tools,
            )
        )
        
        print("\n--- Model Response (Summary) ---")
        for part in response.candidates[0].content.parts:
            print(part.text)
        
        # CRITICAL: Programmatic check of retrieval status
        print("\n--- PROGRAMMATIC STATUS REPORT ---")
        metadata = response.candidates[0].url_context_metadata
        if metadata and metadata.url_metadata:
            for item in metadata.url_metadata:
                status = item.url_retrieval_status
                if status == "URL_RETRIEVAL_STATUS_SUCCESS":
                    print(f"[SUCCESS] {item.retrieved_url}")
                else:
                    # Reports failure status (e.g., URL_RETRIEVAL_STATUS_FAILURE)
                    print(f"[FAILURE] {item.retrieved_url} - Status: {status}")
        else:
            print("No URL metadata returned for analysis.")
            
    except Exception as e:
        print(f"An error occurred in Exercise 4: {e}")


# --- Exercise 5: Structured Data Extraction from a Financial Report ---
def exercise_5_structured_extraction():
    print("\n\n===== EXERCISE 5: STRUCTURED DATA EXTRACTION (JSON OUTPUT) =====")
    
    # Using a general news article for structured data extraction
    finance_url = "https://www.reuters.com/markets/companies/GOOGL.OQ/" 
    
    prompt = (
        f"From the article at {finance_url}, extract the following three data points: "
        "The current stock ticker symbol, the reported market capitalization (or related financial metric), "
        "and the date of the article's publication. "
        "RESPOND ONLY with a valid JSON object containing keys 'ticker', 'market_cap', and 'pub_date'."
    )
    
    tools = [
      {"url_context": {}},
    ]

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=GenerateContentConfig(
                tools=tools,
            )
        )
        
        json_string = response.candidates[0].content.parts[0].text
        print("\n--- Structured JSON Output ---")
        print(json_string)
        
        # Demonstration of Python's ability to process the structured output
        print("\n--- Python Processing Example ---")
        try:
            # Attempt to parse the string into a Python dictionary
            data = json.loads(json_string)
            print(f"Successfully parsed JSON. Extracted Ticker: {data.get('ticker', 'N/A')}")
        except json.JSONDecodeError:
            print("ERROR: Failed to parse the output as valid JSON.")
        
        print_metadata(response)

    except Exception as e:
        print(f"An error occurred in Exercise 5: {e}")


if __name__ == "__main__":
    # Note: Execution time depends on network latency and model response time.
    exercise_1_single_page_summary()
    exercise_2_comparative_analysis()
    exercise_3_advanced_grounding()
    exercise_4_robustness_check()
    exercise_5_structured_extraction()


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

# --- Configuration ---
# Ensure GEMINI_API_KEY is set in your environment variables
try:
    # Initialize the client. This assumes GEMINI_API_KEY is available.
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Ensure API key is set. Details: {e}")
    # Exit gracefully if the client cannot be initialized due to missing credentials
    exit()

# Helper function to print grounding sources cleanly, adhering to attribution requirements
def print_grounding_sources(grounding_metadata):
    """Prints formatted source citations from the grounding metadata, attributing to Google Maps."""
    if not grounding_metadata:
        print("No grounding metadata found.")
        return

    chunks = grounding_metadata.grounding_chunks
    if chunks:
        print("-" * 50)
        print("🌍 Grounding Sources (Google Maps):")
        for chunk in chunks:
            # Check if the chunk contains Maps data
            if chunk.maps:
                title = chunk.maps.title
                uri = chunk.maps.uri
                # Display the source title and link, attributing to Google Maps
                # Note: The actual display of the link/title should follow the Maps attribution guidelines
                print(f"  - [Source: Google Maps] {title} -> {uri}")
        print("-" * 50)
    else:
        print("Query was answered, but no specific Maps chunks were cited.")

# =============================================================================
# --- Exercise 1 Solution: Basic Geographical Grounding (Rome) ---
# =============================================================================
print("\n=== Exercise 1: Basic Geographical Grounding (Rome) ===")

prompt_e1 = "What are the three most iconic historical landmarks in Rome, Italy, and what makes them famous?"

response_e1 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt_e1,
    config=types.GenerateContentConfig(
        # Simply enable the Maps tool
        tools=[types.Tool(google_maps=types.GoogleMaps())],
    ),
)

print("\nGenerated Response:")
print(response_e1.text)

if response_e1.candidates and response_e1.candidates[0].grounding_metadata:
    print_grounding_sources(response_e1.candidates[0].grounding_metadata)
else:
    print("\nNo grounding metadata returned for this general query.")


# =============================================================================
# --- Exercise 2 Solution: Personalized Proximity Search (Sydney) ---
# =============================================================================
print("\n=== Exercise 2: Personalized Proximity Search (Sydney Opera House) ===")

# Sydney Opera House Coordinates
SYDNEY_LAT = -33.8568
SYDNEY_LNG = 151.2153

prompt_e2 = "Where can I find a highly-rated coffee shop open right now that is within a 10-minute walk from here?"

response_e2 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt_e2,
    config=types.GenerateContentConfig(
        # Enable the Maps tool
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        # Inject the specific location context using tool_config and retrieval_config
        tool_config=types.ToolConfig(
            retrieval_config=types.RetrievalConfig(
                lat_lng=types.LatLng(
                    latitude=SYDNEY_LAT, 
                    longitude=SYDNEY_LNG
                )
            )
        ),
    ),
)

print("\nGenerated Response:")
print(response_e2.text)

if response_e2.candidates and response_e2.candidates[0].grounding_metadata:
    print_grounding_sources(response_e2.candidates[0].grounding_metadata)
else:
    print("\nNo grounding metadata returned.")


# =============================================================================
# --- Exercise 3 Solution: Advanced Output Extraction and Widget Request (NYC) ---
# =============================================================================
print("\n=== Exercise 3: Advanced Output Extraction and Widget Request (NYC) ===")

# Coordinates near New York Stock Exchange
NYC_LAT = 40.7063
NYC_LNG = -74.0094

prompt_e3 = "Plan a three-hour walking tour of downtown Manhattan, starting at the New York Stock Exchange. Include historical sites and a good lunch spot."

response_e3 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt_e3,
    config=types.GenerateContentConfig(
        # Enable the Maps tool and request the widget token
        tools=[types.Tool(google_maps=types.GoogleMaps(enable_widget=True))],
        tool_config=types.ToolConfig(
            retrieval_config=types.RetrievalConfig(
                lat_lng=types.LatLng(
                    latitude=NYC_LAT, 
                    longitude=NYC_LNG
                )
            )
        ),
    ),
)

print("\nGenerated Response:")
print(response_e3.text)

if grounding_e3 := response_e3.candidates[0].grounding_metadata:
    # 1. Print Sources
    print_grounding_sources(grounding_e3)

    # 2. Extract and print the widget token
    if widget_token := grounding_e3.google_maps_widget_context_token:
        print("\n🗺️ Contextual Maps Widget Token Found:")
        print("This token can be used with the Google Maps JavaScript API.")
        # Display the token formatted as an HTML placeholder component
        print(f'HTML Placeholder: <gmp-place-contextual context-token="{widget_token}"></gmp-place-contextual>')
    else:
        print("\nWidget token was not returned.")


# =============================================================================
# --- Exercise 4 Solution: Dynamic Geo-Agent Function (Challenge) ---
# =============================================================================
print("\n=== Exercise 4: Dynamic Geo-Agent Function (Seattle Bookstores) ===")

def generate_grounded_itinerary(city: str, constraint: str, latitude: float, longitude: float) -> dict:
    """
    Generates a location-aware itinerary using Maps Grounding based on dynamic inputs.
    Returns a dictionary containing the generated text, sources, and widget token.
    """
    dynamic_prompt = (
        f"Plan an evening in {city} focused on finding {constraint}. "
        f"List three specific, highly-rated places near here, including their names and addresses."
    )
    
    print(f"Agent Prompting: Searching {constraint} in {city}...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=dynamic_prompt,
            config=types.GenerateContentConfig(
                # Enable Maps and request widget for maximum context
                tools=[types.Tool(google_maps=types.GoogleMaps(enable_widget=True))],
                tool_config=types.ToolConfig(
                    retrieval_config=types.RetrievalConfig(
                        lat_lng=types.LatLng(
                            latitude=latitude, 
                            longitude=longitude
                        )
                    )
                ),
            ),
        )

        output = {
            "text": response.text,
            "sources": [],
            "widget_token": None
        }

        # Extract structured data
        if response.candidates and (grounding := response.candidates[0].grounding_metadata):
            
            # Extract sources
            if chunks := grounding.grounding_chunks:
                for chunk in chunks:
                    if chunk.maps:
                        output["sources"].append({
                            "title": chunk.maps.title,
                            "uri": chunk.maps.uri
                        })
            
            # Extract widget token
            if token := grounding.google_maps_widget_context_token:
                output["widget_token"] = token
        
        return output

    except Exception as e:
        return {"error": f"API call failed: {e}", "text": "", "sources": [], "widget_token": None}

# Test Case: Seattle, WA - Historic Bookstores
SEATTLE_LAT = 47.6062
SEATTLE_LNG = -122.3321
CONSTRAINT = "historic bookstores"
CITY = "Seattle, WA"

results = generate_grounded_itinerary(
    city=CITY,
    constraint=CONSTRAINT,
    latitude=SEATTLE_LAT,
    longitude=SEATTLE_LNG
)

print(f"\n--- Results for {CITY} ({CONSTRAINT}) ---")
print("Generated Itinerary:")
print(results["text"])

# Display structured data
if results.get("sources"):
    print("-" * 50)
    print("📚 Grounded Sources:")
    for src in results["sources"]:
        print(f"  - [Google Maps] {src['title']} -> {src['uri']}")

if results.get("widget_token"):
    print("-" * 50)
    print("🗺️ Widget Token (for visual display):")
    print(results["widget_token"])

if "error" in results:
    print(f"Error encountered: {results['error']}")


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

# --- Configuration ---

# 1. Initialize the client, which automatically looks for the GEMINI_API_KEY
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    exit()

# Define a default location (e.g., San Francisco, CA) for demonstration
DEFAULT_LATITUDE = 37.7749
DEFAULT_LONGITUDE = -122.4194

# --- Core Agent Functions ---

def generate_grounded_itinerary(
    user_prompt: str, 
    latitude: float, 
    longitude: float, 
    enable_widget: bool = True
) -> dict:
    """
    Generates content grounded in Google Maps data for location-aware responses.

    Args:
        user_prompt: The user's specific request (e.g., "Plan a day for a foodie").
        latitude: The latitude of the user's current or desired location.
        longitude: The longitude of the user's current or desired location.
        enable_widget: If True, requests a context token for a map widget.

    Returns:
        A dictionary containing the generated text, sources, and widget token.
    """
    print(f"--- Sending request to Gemini (Location: {latitude}, {longitude}) ---")

    # 1. Define the Google Maps Tool Configuration
    # We enable the tool and optionally request the widget token.
    maps_tool = types.Tool(
        google_maps=types.GoogleMaps(enable_widget=enable_widget)
    )

    # 2. Define the Location Context Configuration
    # This crucial step injects the precise geographical coordinates into the model's context
    # via the RetrievalConfig, allowing the Maps tool to perform local searches.
    location_config = types.ToolConfig(
        retrieval_config=types.RetrievalConfig(
            lat_lng=types.LatLng(latitude=latitude, longitude=longitude)
        )
    )

    # 3. Execute the API call
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Use a model known to support Maps Grounding
        contents=user_prompt,
        config=types.GenerateContentConfig(
            tools=[maps_tool],
            tool_config=location_config,
        ),
    )

    # 4. Parse the response and extract structured metadata
    result = {
        "text": response.text,
        "sources": [],
        "widget_token": None
    }

    # Check if grounding metadata exists (meaning the tool was successfully invoked)
    if response.candidates and response.candidates[0].grounding_metadata:
        grounding = response.candidates[0].grounding_metadata
        
        # Extract grounding chunks (the citations/sources)
        if grounding.grounding_chunks:
            result["sources"] = [
                {
                    "title": chunk.maps.title,
                    "uri": chunk.maps.uri,
                    "place_id": chunk.maps.place_id
                }
                for chunk in grounding.grounding_chunks if chunk.maps
            ]
        
        # Extract the contextual widget token
        if grounding.google_maps_widget_context_token:
            result["widget_token"] = grounding.google_maps_widget_context_token

    return result


def display_results(results: dict):
    """
    Prints the generated content, citations, and widget token, adhering to 
    the Google Maps attribution guidelines (by displaying sources).
    """
    print("\n" + "="*80)
    print("           D Y N A M I C   G E O - C O N C I E R G E   R E S P O N S E")
    print("="*80)
    
    # 1. Display the Generated Itinerary Text
    print("\n[ITINERARY GENERATED BY GEMINI]:")
    print(results['text'])
    
    # 2. Display Grounding Sources (Mandatory Attribution)
    if results['sources']:
        print("\n" + "-"*40)
        print("FACTUAL GROUNDING SOURCES (Google Maps Attribution Required):")
        for i, source in enumerate(results['sources']):
            # Display source title and link (URI) as required by usage guidelines
            print(f"  {i+1}. [{source['title']}] - Link: {source['uri']}")
            print(f"     (Place ID: {source['place_id']})")
        print("-" * 40)
    else:
        print("\n[INFO]: No specific Google Maps sources were used for grounding this response.")
        
    # 3. Display the Contextual Widget Token
    if results['widget_token']:
        print("\n[INTERACTIVE MAP WIDGET TOKEN]:")
        print("Token successfully retrieved. Use this token in a web frontend to render the contextual map widget.")
        # Example HTML snippet for rendering (as shown in documentation)
        print(f'HTML Snippet Example: <gmp-place-contextual context-token="{results["widget_token"]}"></gmp-place-contextual>')
    else:
        print("\n[INFO]: Map widget token was not requested or not returned.")
    
    print("\n" + "="*80)


# --- Main Execution Block ---

if __name__ == "__main__":
    
    # 1. Define the user's dynamic input
    user_theme = "Plan a half-day itinerary for a history and architecture enthusiast."
    
    # 2. Define the location (using the default San Francisco coordinates)
    current_lat = DEFAULT_LATITUDE
    current_lng = DEFAULT_LONGITUDE
    
    # Construct the full prompt, emphasizing the geographical context
    full_prompt = (
        f"You are a local travel guide. Based on the location context ({current_lat}, {current_lng}), "
        f"{user_theme} The plan should include specific locations, addresses, and estimated travel times."
    )

    try:
        # Run the agent with widget request enabled
        itinerary_data = generate_grounded_itinerary(
            user_prompt=full_prompt,
            latitude=current_lat,
            longitude=current_lng,
            enable_widget=True # Request the contextual map token
        )
        
        # Display the results
        display_results(itinerary_data)

    except genai.errors.APIError as e:
        print(f"\n[CRITICAL API ERROR]: Failed to generate content. Details: {e}")
    except Exception as e:
        print(f"\n[CRITICAL SYSTEM ERROR]: An unexpected error occurred: {e}")


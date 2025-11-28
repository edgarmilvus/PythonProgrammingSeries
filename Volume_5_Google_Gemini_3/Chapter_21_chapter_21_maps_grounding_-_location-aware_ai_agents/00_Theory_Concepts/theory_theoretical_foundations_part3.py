
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

# Ensure the GEMINI_API_KEY environment variable is set
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is configured.")
    exit()


def plan_grounded_itinerary(user_prompt: str, lat: float, lng: float):
    """
    Generates a location-aware itinerary using Maps Grounding,
    requesting the contextual widget token.
    """
    print(f"--- Processing Query: {user_prompt} ---")

    # 1. Define the specific location context
    location_context = types.LatLng(latitude=lat, longitude=lng)

    # 2. Configure the request: Enable Maps tool and request the widget
    config = types.GenerateContentConfig(
        # Enable the Google Maps tool and set enable_widget=True
        tools=[types.Tool(google_maps=types.GoogleMaps(enable_widget=True))],
        
        # Inject the location context into the tool configuration
        tool_config=types.ToolConfig(
            retrieval_config=types.RetrievalConfig(
                lat_lng=location_context
            )
        ),
    )

    # 3. Call the API
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=config,
        )
    except Exception as e:
        print(f"An API error occurred: {e}")
        return

    # 4. Process the response
    print("\n[Generated Response Text]")
    print(response.text)

    # 5. Extract and display grounding metadata
    if candidates := response.candidates:
        if grounding := candidates[0].grounding_metadata:
            
            # Display Sources (Mandatory Attribution)
            if chunks := grounding.grounding_chunks:
                print('\n' + '-' * 50)
                print("[Google Maps Sources (Mandatory Attribution)]")
                for i, chunk in enumerate(chunks):
                    # Displaying the required title and URI for compliance
                    print(f'{i+1}. [{chunk.maps.title}]({chunk.maps.uri})')

            # Display Widget Token (Optional but Recommended)
            if widget_token := grounding.google_maps_widget_context_token:
                print('\n' + '-' * 50)
                print("[Contextual Widget Token]")
                # This token is used on the frontend (e.g., JavaScript) 
                # to render the interactive map component.
                print(f'Token: {widget_token[:20]}... (truncated)')
                print(f'HTML Snippet Example:')
                print(f'<gmp-place-contextual context-token="{widget_token}"></gmp-place-contextual>')
                print('-' * 50)
        else:
            print("\n[INFO] Response was not grounded in Google Maps data.")


# Example execution: Plan a day in San Francisco (latitude: 37.78193, longitude: -122.40476)
prompt_sf = "Plan a day in San Francisco for me. I want to see the Golden Gate Bridge, visit a museum, and have a nice dinner."
plan_grounded_itinerary(prompt_sf, 37.78193, -122.40476)

# Example execution: Find local dining options in Los Angeles
prompt_la = "What are the best Italian restaurants within a 15-minute walk from here?"
plan_grounded_itinerary(prompt_la, 34.050481, -118.248526)

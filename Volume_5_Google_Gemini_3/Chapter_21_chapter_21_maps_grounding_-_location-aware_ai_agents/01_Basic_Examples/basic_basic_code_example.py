
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

# --- 1. Configuration and Setup ---

# Ensure your GEMINI_API_KEY is set as an environment variable
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

# Define the location context (Los Angeles City Hall area)
LA_LATITUDE = 34.050481
LA_LONGITUDE = -118.248526

# The user's prompt, which implicitly requires location awareness ("near here")
USER_PROMPT = "What is the highest-rated coffee shop within a 10-minute walk from here?"

print(f"Querying Gemini (Location: {LA_LATITUDE}, {LA_LONGITUDE})...")
print(f"Prompt: {USER_PROMPT}\n")

# --- 2. Defining the Grounding Tool and Location Context ---

# Create the LatLng object using the defined coordinates
location_context = types.LatLng(
    latitude=LA_LATITUDE,
    longitude=LA_LONGITUDE
)

# Define the Google Maps tool configuration
maps_tool = types.Tool(
    google_maps=types.GoogleMaps()  # Explicitly enables the Maps tool
)

# Define the tool configuration to inject the location context
tool_config = types.ToolConfig(
    retrieval_config=types.RetrievalConfig(
        lat_lng=location_context  # Passes the coordinates to the grounding tool
    )
)

# --- 3. Generating Content with Grounding ---

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',  # A model that supports Maps Grounding
        contents=USER_PROMPT,
        config=types.GenerateContentConfig(
            tools=[maps_tool],  # Pass the list containing the Maps tool
            tool_config=tool_config, # Pass the location configuration
        ),
    )

    # --- 4. Processing and Displaying the Response ---

    print("-" * 50)
    print("🤖 Grounded Response Text:")
    print(response.text)
    print("-" * 50)

    # Check if grounding metadata exists (i.e., the Maps tool was successfully used)
    grounding = response.candidates[0].grounding_metadata

    if grounding and grounding.grounding_chunks:
        print("🌍 Location Sources (Citations):")
        # Iterate through the chunks to display the specific Maps data used
        for i, chunk in enumerate(grounding.grounding_chunks):
            # Check specifically for maps data within the chunk
            if chunk.maps:
                title = chunk.maps.title
                uri = chunk.maps.uri
                print(f"  {i+1}. [{title}]")
                print(f"     Link: {uri}")
    else:
        print("⚠️ Warning: No Google Maps grounding data was returned for this query.")

except Exception as e:
    print(f"\nAn API error occurred: {e}")


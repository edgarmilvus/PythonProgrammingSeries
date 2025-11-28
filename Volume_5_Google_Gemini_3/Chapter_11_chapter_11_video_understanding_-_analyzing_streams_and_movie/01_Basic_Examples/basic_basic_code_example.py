
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
from google.genai.errors import APIError

# --- 1. Configuration and Client Setup ---

# Ensure the GOOGLE_API_KEY environment variable is set before running.
try:
    # Initialize the client. This automatically picks up the API key 
    # from the environment variables (PEP 8 compliance: snake_case for variables).
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Please ensure GOOGLE_API_KEY is configured: {e}")
    # Exit gracefully if setup fails
    exit()

# Define constants for the model and the video source
MODEL_NAME = 'gemini-2.5-flash'
# CRITICAL: Replace this with a public YouTube video URL for testing.
# NOTE: Private or unlisted videos are not supported.
YOUTUBE_URL = 'https://www.youtube.com/watch?v=9hE5-98ZeCg' 

# --- 2. Define the Multimodal Prompt ---

# Define the detailed instruction for the model.
# We explicitly request the required timestamp format (MM:SS).
video_prompt = (
    "Analyze this video. Provide a concise summary (max 4 sentences). "
    "Then, identify three key events and report their exact timestamps (MM:SS format) "
    "and a brief description of what is happening visually and audibly at that moment."
)

print(f"--- Starting Gemini 3 Video Analysis for: {YOUTUBE_URL} ---")
print(f"Prompt: '{video_prompt}'")
print("-" * 60)

# --- 3. Construct the Multimodal Request Payload ---

try:
    # A multimodal request requires defining multiple 'Part' objects within the 'contents' array.
    
    # Part A: The Video Input
    # When using a URL, we use the 'file_data' field with 'file_uri'.
    video_part = types.Part(
        file_data=types.FileData(
            file_uri=YOUTUBE_URL,
            # We specify the mime type, even for a URL, though 'video/*' is often acceptable.
            mime_type='video/mp4' 
        )
    )

    # Part B: The Text Prompt
    text_part = types.Part(text=video_prompt)

    # Combine the parts into the contents structure. 
    # Best Practice: Place the text prompt *after* the video part.
    contents = [video_part, text_part]

    # --- 4. Execute the API Call ---
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
    )

    # --- 5. Display Results and Metadata ---
    
    print("\n[AI Analysis Complete]")
    print("=" * 60)
    print(response.text)
    print("=" * 60)

    # Display token usage for cost awareness
    if response.usage_metadata:
        print("\n[Token Metrics]")
        # The prompt token count includes the tokenization cost of the entire video and the text prompt.
        print(f"Input Tokens (Video + Text): {response.usage_metadata.prompt_token_count}")
        print(f"Output Tokens: {response.usage_metadata.candidates_token_count}")
        print("-" * 60)

except APIError as e:
    # Catch specific API errors (e.g., authentication, invalid URL, content safety)
    print(f"\n[CRITICAL ERROR] Gemini API Error occurred: {e}")
except Exception as e:
    # Catch unexpected errors
    print(f"\n[UNEXPECTED ERROR] An error occurred during processing: {e}")


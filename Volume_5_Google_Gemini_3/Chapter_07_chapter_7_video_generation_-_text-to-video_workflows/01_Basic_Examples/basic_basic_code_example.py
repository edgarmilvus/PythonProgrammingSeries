
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

import time
import os
from google import genai
from google.genai import types

# --- Configuration and Initialization ---

# Define the model to use for video generation (Veo 3.1)
VEO_MODEL = "veo-3.1-generate-preview"
# Define the interval (in seconds) to check the job status
API_POLL_INTERVAL = 10 
# Define the desired output filename
OUTPUT_FILENAME = "cinematic_lighthouse_scene.mp4"

# Initialize the client. The client automatically uses the GEMINI_API_KEY 
# stored in your environment variables.
client = genai.Client()

# --- 1. Prompt Definition ---
# A detailed, cinematic prompt is crucial for high-quality results.
CINEMATIC_PROMPT = """
A sweeping, cinematic wide shot of a lone, ancient lighthouse standing on a jagged,
mist-shrouded cliff face at dawn. The camera slowly pans left, revealing turbulent,
deep blue ocean waves crashing dramatically against the rocks below. Moody, realistic lighting.
(Sound: distant foghorn, crashing waves).
"""

print(f"--- Veo 3.1 Video Generation Workflow ---")
print(f"1. Submitting request for video generation using model: {VEO_MODEL}")

# --- 2. Initiate the Long-Running Operation (LRO) ---
try:
    # The generate_videos method immediately returns an operation object, not the video itself.
    operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=CINEMATIC_PROMPT,
        # Optional configuration to specify resolution (720p is default)
        config=types.GenerateVideosConfig(resolution="720p")
    )

    print(f"   Operation started successfully. LRO Name: {operation.name}")

except Exception as e:
    print(f"Error initiating video generation: {e}")
    exit()

# --- 3. Poll the Operation Status ---
# This loop is essential for handling the asynchronous nature of video generation.
while not operation.done:
    print(f"2. Waiting for generation... Status: {operation.metadata.state}. Checking again in {API_POLL_INTERVAL} seconds.")
    
    # Pause execution to avoid excessive API calls and rate limiting.
    time.sleep(API_POLL_INTERVAL)
    
    # Refresh the operation object to get the latest status from the server.
    # This updates the 'operation.done' flag.
    operation = client.operations.get(operation)

print("3. Video generation complete. Status: DONE.")

# --- 4. Retrieval and Saving ---
try:
    # Check for success before attempting to access the response structure.
    if operation.response and operation.response.generated_videos:
        # The result is stored in the 'response' attribute of the completed operation.
        # We access the first (and only) generated video asset in the list.
        generated_video_asset = operation.response.generated_videos[0]
        
        # The actual video data is contained within the 'video' field of the asset.
        video_file_object = generated_video_asset.video
        
        # Download the file data from Google's servers.
        client.files.download(file=video_file_object)
        
        # Save the file object's bytes to the specified local path.
        video_file_object.save(OUTPUT_FILENAME)
        
        print(f"4. Success! Video saved locally as: {OUTPUT_FILENAME}")
        
    else:
        print("Generation failed or returned no video assets.")

except Exception as e:
    print(f"An error occurred during download or saving: {e}")
    print("Review the operation status for detailed error messages.")


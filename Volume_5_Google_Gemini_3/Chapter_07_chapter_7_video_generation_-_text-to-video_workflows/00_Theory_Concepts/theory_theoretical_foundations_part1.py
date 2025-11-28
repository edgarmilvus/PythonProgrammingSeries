
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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

import time
import os
from google import genai
from google.genai import types

# --- Configuration and Setup ---
# NOTE: Ensure your GEMINI_API_KEY is set in your environment variables.
client = genai.Client()

# Define the model names as per documentation
VEO_MODEL = "veo-3.1-generate-preview"
IMAGE_MODEL = "gemini-2.5-flash-image"

# --- 1. Define Cinematic Prompts ---
# The overall narrative for the video generation
VIDEO_PROMPT = """
A cinematic, haunting video. A ghostly woman with long white hair and a flowing dress swings gently on a rope swing beneath a massive, gnarled tree in a foggy, moonlit clearing. 
The fog thickens and swirls around her, and she slowly fades away, vanishing completely. 
The empty swing is left swaying rhythmically on its own in the eerie silence.
"""

# The prompt for the starting image (must be consistent with the video prompt)
FIRST_IMAGE_PROMPT = "A ghostly woman with long white hair and a flowing dress swings gently on a rope swing beneath a massive, gnarled tree in a foggy, moonlit clearing. Cinematic lighting, high detail."

# The prompt for the ending image (the result of the action)
LAST_IMAGE_PROMPT = "A massive, gnarled tree in a foggy, moonlit clearing. The rope swing hangs empty and swaying rhythmically. Haunting, eerie silence."

OUTPUT_FILENAME = "veo3_interpolation_scene.mp4"

def poll_operation_status(operation: types.GenerateVideosOperation) -> types.GenerateVideosOperation:
    """
    Handles the asynchronous polling loop required for long-running video generation jobs.
    """
    print(f"\n--- Starting Asynchronous Polling for Operation: {operation.name} ---")
    
    start_time = time.time()
    
    while not operation.done:
        elapsed = int(time.time() - start_time)
        print(f"[{elapsed}s] Waiting for video generation to complete... (Checking status in 10s)")
        time.sleep(10)
        
        # Refresh the operation object to get the latest status from the API
        operation = client.operations.get(operation)

        # Safety break for demonstration purposes (optional)
        if elapsed > 300: # 5 minutes
             print("Polling timeout reached. Aborting.")
             break

    if operation.done:
        print("\n--- Video Generation Complete ---")
    else:
        print("\n--- Operation Failed or Timed Out ---")
    
    return operation


def generate_image_part(prompt: str, filename: str) -> types.Part:
    """
    Generates a single image using gemini-2.5-flash-image and returns the image part.
    """
    print(f"\n[Step 1] Generating Image: {filename}...")
    
    # Generate the image content
    image_response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
        config={
            "response_modalities":['IMAGE']
        }
    )

    # Validate and extract the image part
    if not image_response.generated_images:
        raise ValueError(f"Image generation failed for prompt: {prompt}")
        
    generated_image_part = image_response.generated_images[0].image
    
    # Save the generated image locally for verification (optional)
    try:
        if generated_image_part.image_bytes:
            with open(f"{filename}.png", "wb") as f:
                f.write(generated_image_part.image_bytes)
            print(f"Successfully generated and saved {filename}.png")
        
        # Convert the raw image bytes into the required Image object format for Veo
        return types.Image(image_bytes=generated_image_part.image_bytes, mime_type="image/png")

    except Exception as e:
        print(f"Error saving image: {e}")
        # Proceeding with the in-memory object even if saving failed
        return types.Image(image_bytes=generated_image_part.image_bytes, mime_type="image/png")


# --- Main Execution Flow ---
try:
    # --- STEP 1: Generate the First and Last Frames using Nano Banana ---
    
    # Generate the starting frame (Ghostly Woman)
    first_image = generate_image_part(FIRST_IMAGE_PROMPT, "first_frame")
    
    # Generate the ending frame (Empty Swing)
    last_image = generate_image_part(LAST_IMAGE_PROMPT, "last_frame")
    
    print("\n[Step 2] Initiating Veo 3.1 Video Interpolation Job...")

    # --- STEP 2: Initiate the Video Generation Job (Interpolation) ---
    # We use the 'image' parameter for the start frame and 'config.last_frame' for the end frame.
    initial_operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=VIDEO_PROMPT,
        image=first_image, # The starting frame (Image object)
        config=types.GenerateVideosConfig(
          last_frame=last_image, # The ending frame (Image object)
          # Interpolation videos must be 8 seconds long and use 16:9 or 9:16 aspect ratio
          duration_seconds="8", 
          resolution="720p",
          aspect_ratio="16:9"
        ),
    )

    print(f"Video generation job started. Operation Name: {initial_operation.name}")

    # --- STEP 3: Poll the operation status until the video is ready ---
    final_operation = poll_operation_status(initial_operation)

    # --- STEP 4: Download and Save the Generated Video ---
    if final_operation.done and final_operation.response.generated_videos:
        generated_video_item = final_operation.response.generated_videos[0]
        video_file_ref = generated_video_item.video
        
        print(f"\n[Step 4] Downloading generated video file reference: {video_file_ref.name}")

        # Download the file content
        client.files.download(file=video_file_ref)
        
        # Save the content to a local file
        video_file_ref.save(OUTPUT_FILENAME)
        
        print(f"Success! Generated video saved to {OUTPUT_FILENAME}")
        
    else:
        print("Video generation failed or no video was returned in the response.")

except Exception as e:
    print(f"\nAn error occurred during the T2V workflow: {e}")


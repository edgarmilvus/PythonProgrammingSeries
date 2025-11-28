
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

import time
import os
from google import genai
from google.genai import types

# --- Configuration and Initialization ---
# Ensure your GEMINI_API_KEY is set in your environment variables.
# Note: Video generation is a long-running, resource-intensive task.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Ensure API key is set correctly: {e}")
    # We exit here if the client cannot be initialized
    exit()

# Define the models used
VEO_MODEL = "veo-3.1-generate-preview"
IMAGE_MODEL = "gemini-2.5-flash-image"

# --- Helper Function for Polling Long Running Operations (LROs) ---

def poll_operation_status(operation: types.GenerateVideosOperation, filename: str) -> types.Video | None:
    """
    Polls the status of a video generation operation until it is complete.
    Downloads and saves the resulting video file.
    Returns the generated Video object or None on failure.
    """
    print(f"\n--- Starting Polling for {filename} (Operation: {operation.name}) ---")
    start_time = time.time()
    
    # Set a reasonable timeout for video generation (e.g., 10 minutes)
    MAX_WAIT_SECONDS = 600 

    while not operation.done:
        elapsed = int(time.time() - start_time)
        if elapsed > MAX_WAIT_SECONDS:
            print(f"Error: Operation timed out after {MAX_WAIT_SECONDS} seconds.")
            return None
            
        print(f"[{elapsed}s elapsed] Waiting for video generation to complete...")
        time.sleep(10)
        
        # Refresh the operation object to get the latest status
        try:
            # We use client.operations.get() as shown in the docs
            operation = client.operations.get(operation)
        except Exception as e:
            print(f"Error fetching operation status: {e}")
            return None

    # Check for successful response
    if operation.response and operation.response.generated_videos:
        print("Video generation complete. Downloading asset...")
        generated_video = operation.response.generated_videos[0]
        
        # Download the file reference
        client.files.download(file=generated_video.video)
        
        # Save the file locally using the Video object's save method
        generated_video.video.save(filename)
        print(f"Success: Generated video saved to {filename}")
        return generated_video.video
    else:
        print(f"Error: Operation completed but no video asset was found. Details: {operation.error}")
        return None

# --- Helper Function for Image Generation ---

def generate_asset_image(prompt: str) -> types.Image | None:
    """Generates an Image object using Nano Banana (gemini-2.5-flash-image)."""
    print(f"\n[ASSET GENERATION] Generating image for prompt: '{prompt[:50]}...'")
    
    try:
        # Step 1: Generate an image with Nano Banana.
        image_response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            # Config required to specify image output
            config={"response_modalities":['IMAGE']} 
        )
        
        # Check if the image part is available
        if image_response.parts and image_response.parts[0].as_image():
            print("[ASSET GENERATION] Image asset successfully created.")
            return image_response.parts[0].as_image()
        else:
            print("[ASSET GENERATION] Image generation failed: No image part found.")
            return None
            
    except Exception as e:
        print(f"[ASSET GENERATION] Image generation failed: {e}")
        return None

# ====================================================================
# Exercise Solutions
# ====================================================================

### Exercise 1: The Standard Cinematic Generation Workflow

def solution_1():
    print("\n\n--- Running Exercise 1: Standard Cinematic Generation ---")
    prompt_1 = "A drone shot flying over a misty, ancient temple ruins at sunrise. Cinematic lighting, 8-second clip."
    output_filename = "ex1_cinematic_shot.mp4"

    # 1. Initiate the long-running operation
    operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=prompt_1,
    )

    # 2 & 3 & 4. Implement polling, download, and save
    poll_operation_status(operation, output_filename)

### Exercise 2: Mastering Configuration and Constraints

def solution_2():
    print("\n\n--- Running Exercise 2: Mastering Configuration and Constraints ---")
    prompt_2 = "A photorealistic Bengal tiger slowly emerging from dense jungle foliage during a tropical downpour."
    output_filename = "ex2_constrained_1080p.mp4"
    
    # 1. Define the strict configuration using types.GenerateVideosConfig
    config = types.GenerateVideosConfig(
        resolution="1080p", # Set video resolution to 1080p
        duration_seconds="8", # Set duration to 8 seconds
        # 2. Apply a strict negative prompt
        negative_prompt="low quality, black and white, cartoon, drawing, blurry, amateur footage, noisy, static camera", 
    )

    # 3. Initiate the operation with the configuration object
    operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=prompt_2,
        config=config,
    )

    poll_operation_status(operation, output_filename)

### Exercise 3: Multi-Modal Workflow - Image-Guided Start Frame

def solution_3():
    print("\n\n--- Running Exercise 3: Image-Guided Start Frame ---")
    prompt_3 = "A solitary astronaut standing on a red Martian dune, looking up at Earth glowing faintly in the black sky. The astronaut slowly turns their head to face the camera."
    output_filename = "ex3_image_start.mp4"

    # 1. Generate the starting image asset (Simulated)
    start_image_asset = generate_asset_image(prompt_3)
    
    if not start_image_asset:
        print("Skipping Solution 3 due to image asset failure.")
        return

    # 2. Generate video using the image as the starting frame
    # The 'image' parameter is used for the initial frame
    operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=prompt_3,
        image=start_image_asset, 
    )

    # 3. Save the final video
    poll_operation_status(operation, output_filename)

### Exercise 4: Advanced Challenge - Interpolation Transition

def solution_4():
    print("\n\n--- Running Exercise 4: Interpolation Transition ---")
    
    # 1. Define narrative and prompts
    prompt_interpolation = "A dramatic, 8-second transition video. The camera slowly pans across the futuristic cyberpunk city skyline, transforming into an ancient, overgrown jungle ruin."
    
    first_image_prompt = "A futuristic cyberpunk city skyline at dusk, neon lights reflecting off wet streets. High contrast, cinematic."
    last_image_prompt = "The same city skyline, now completely overgrown with vibrant neon jungle foliage, moss covering all buildings. Eerie, silent atmosphere."
    output_filename = "ex4_interpolation_transition.mp4"

    # 2. Generate the two required image assets
    first_image = generate_asset_image(first_image_prompt)
    last_image = generate_asset_image(last_image_prompt)
    
    if not first_image or not last_image:
        print("Skipping Solution 4 due to required image asset failure.")
        return

    # 3. Generate the video using both frames for interpolation
    # The 'last_frame' must be placed inside the GenerateVideosConfig
    config = types.GenerateVideosConfig(
        last_frame=last_image, # The target end frame
        duration_seconds="8", # Required duration for interpolation
    )

    operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=prompt_interpolation,
        image=first_image, # The required starting frame
        config=config,
    )

    # 4. Save the final video
    poll_operation_status(operation, output_filename)

### Exercise 5: State Management and Video Extension

def solution_5():
    print("\n\n--- Running Exercise 5: State Management and Video Extension ---")

    # Phase 1: Generate the initial video asset (MUST be 720p for extension)
    initial_prompt = "A fluffy white puppy runs playfully across a green lawn on a sunny day."
    initial_video_name = "ex5_initial_video.mp4"
    
    print("PHASE 1: Generating initial 8-second video asset...")
    initial_operation = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=initial_prompt,
        # 720p is required for video extension input
        config=types.GenerateVideosConfig(resolution="720p") 
    )
    previous_video_asset = poll_operation_status(initial_operation, initial_video_name)
    
    if not previous_video_asset:
        print("Skipping Solution 5 Phase 2: Failed to generate initial video asset.")
        return

    # Phase 2: Use the previous asset for extension
    extension_prompt = "Track the puppy as it stops abruptly and barks playfully at a small, curious squirrel climbing a nearby oak tree."
    output_filename = "ex5_extended_pipeline.mp4"

    # 3. Call generate_videos, using the 'video' parameter
    operation = client.models.generate_videos(
        model=VEO_MODEL,
        video=previous_video_asset, # Input asset for extension
        prompt=extension_prompt,
        config=types.GenerateVideosConfig(
            resolution="720p", # Required resolution for extension
        ),
    )

    print("\nPHASE 2: Generating video extension...")
    # The output video will be the combined (initial + extension) clip
    poll_operation_status(operation, output_filename)

# ====================================================================
# Execution Block
# ====================================================================
if __name__ == "__main__":
    print("WARNING: Video generation is a long-running process and may incur costs.")
    print("Uncomment the solutions below to run them.")
    
    # solution_1()
    # solution_2()
    # solution_3()
    # solution_4()
    # solution_5()
    
    print("\n\n--- Execution complete. Check your directory for generated .mp4 files. ---")

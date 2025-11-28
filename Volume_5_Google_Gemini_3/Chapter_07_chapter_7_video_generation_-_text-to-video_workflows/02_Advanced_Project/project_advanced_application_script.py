
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

import time
import os
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- Configuration and Setup ---

# Define the model to use for video generation
VEO_MODEL = "veo-3.1-generate-preview"
OUTPUT_DIR = "generated_veo_sequences"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize the Gemini client. Assumes GEMINI_API_KEY is set in environment variables.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is configured.")
    exit()

# --- Helper Function for Asynchronous Polling ---

def poll_video_operation(operation: types.GenerateVideosOperation, client: genai.Client) -> types.GenerateVideosOperation:
    """
    Handles the asynchronous polling loop for long-running video generation jobs.
    
    Args:
        operation: The initial operation object returned upon job submission.
        client: The initialized genai.Client object.
        
    Returns:
        The final, completed operation object containing the video response.
    """
    print(f"\n--- Starting Polling for Operation: {operation.name} ---")
    
    # Poll the operation status until the video is ready.
    start_time = time.time()
    
    while not operation.done:
        elapsed = int(time.time() - start_time)
        print(f"Waiting for video generation to complete... ({elapsed}s elapsed)")
        
        # Wait for 10 seconds before checking the status again, as recommended by docs.
        time.sleep(10)
        
        try:
            # Refresh the operation object to get the latest status from the server.
            operation = client.operations.get(operation)
        except APIError as e:
            print(f"An API error occurred during polling: {e}")
            return None
        
        # Safety break for extremely long operations (e.g., 5 minutes)
        if elapsed > 300:
            print("Operation timed out after 5 minutes. Check job status manually later.")
            return None

    print(f"--- Video Generation Complete! Total time: {int(time.time() - start_time)}s ---\n")
    return operation

# --- Phase 1: Initial Text-to-Video Generation (T2V) ---

def generate_initial_scene(client: genai.Client) -> types.Video | None:
    """Generates the first video clip with specific cinematic configurations."""
    
    print("PHASE 1: Generating Initial Cinematic Scene (T2V)")
    
    # 1. Define the detailed prompt for the initial scene.
    prompt_p1 = (
        "A close-up, cinematic shot of a vintage brass compass spinning rapidly on a dark wooden desk. "
        "Dust motes float in the single shaft of morning light cutting across the scene. "
        "The atmosphere is mysterious and quiet. Shot on 35mm film."
    )
    
    # 2. Define the configuration for cinematic control.
    config_p1 = types.GenerateVideosConfig(
        negative_prompt="cartoon, drawing, low quality, shaky camera, hand in frame",
        aspect_ratio="16:9",
        resolution="720p",        # 720p is used to ensure compatibility for the extension phase.
        duration_seconds=8,
    )

    try:
        # Start the video generation job.
        initial_operation = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt_p1,
            config=config_p1,
        )
    except APIError as e:
        print(f"Error starting Phase 1 generation: {e}")
        return None

    # 3. Poll the operation until completion.
    completed_operation = poll_video_operation(initial_operation, client)
    
    if completed_operation and completed_operation.response:
        # 4. Extract the generated video object.
        generated_video_p1 = completed_operation.response.generated_videos[0]
        video_file_p1 = generated_video_p1.video
        
        # 5. Download and save the raw clip.
        output_path_p1 = os.path.join(OUTPUT_DIR, "sequence_part1_initial.mp4")
        client.files.download(file=video_file_p1)
        video_file_p1.save(output_path_p1)
        print(f"-> Phase 1 Video saved successfully to {output_path_p1}")
        
        # Return the Video object needed for the next phase.
        return video_file_p1
    
    return None

# --- Phase 2: Video Extension for Narrative Continuity ---

def extend_scene(client: genai.Client, input_video: types.Video) -> None:
    """Extends a previously generated video using a new prompt."""
    
    print("\nPHASE 2: Extending Video for Narrative Continuity")
    
    # 1. Define the new prompt to continue the action seamlessly.
    prompt_p2 = (
        "The compass slows down, pointing steadily north. A gloved hand enters the frame from the left "
        "and gently picks up the compass, revealing an old, leather-bound map underneath. "
        "Maintain the cinematic lighting and atmosphere."
    )
    
    # 2. Define configuration for the extension.
    # Note: Extension duration is fixed (around 7s) and resolution must match or be compatible (720p).
    config_p2 = types.GenerateVideosConfig(
        resolution="720p",
        # We don't need to specify durationSeconds here, as extension uses a fixed length.
    )

    try:
        # Start the video extension job, passing the previous video object as input.
        extension_operation = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt_p2,
            video=input_video,  # CRITICAL: Input is the Video object from Phase 1
            config=config_p2,
        )
    except APIError as e:
        print(f"Error starting Phase 2 extension: {e}")
        return

    # 3. Poll the operation until completion.
    completed_operation = poll_video_operation(extension_operation, client)
    
    if completed_operation and completed_operation.response:
        # 4. Extract the generated video object (this is the combined clip).
        generated_video_p2 = completed_operation.response.generated_videos[0]
        video_file_p2 = generated_video_p2.video
        
        # 5. Download and save the final combined sequence.
        output_path_p2 = os.path.join(OUTPUT_DIR, "sequence_part2_extended_final.mp4")
        client.files.download(file=video_file_p2)
        video_file_p2.save(output_path_p2)
        print(f"-> Phase 2 Final Combined Video saved successfully to {output_path_p2}")
        print(f"\nWorkflow complete. Check the '{OUTPUT_DIR}' directory for both clips.")
    else:
        print("Phase 2 failed or returned an empty response.")

# --- Main Execution ---

if __name__ == "__main__":
    # Execute Phase 1: Generate the base clip
    base_video_object = generate_initial_scene(client)
    
    if base_video_object:
        # Execute Phase 2: Extend the base clip
        extend_scene(client, base_video_object)
    else:
        print("Cannot proceed to Phase 2: Initial video generation failed.")


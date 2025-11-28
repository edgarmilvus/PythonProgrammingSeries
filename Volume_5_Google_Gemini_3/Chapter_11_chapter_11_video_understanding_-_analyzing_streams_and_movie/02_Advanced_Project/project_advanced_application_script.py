
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
import sys
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- Configuration Constants ---
# Use a model capable of advanced multimodal processing (Gemini 2.5 series or later)
MODEL_NAME = 'gemini-2.5-flash' 

# Example YouTube URL (Replace with a real public video URL for execution)
# NOTE: For testing, ensure the video is public and the timestamps below are valid.
YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Placeholder URL 

# Define the critical segment for detailed analysis (e.g., a 3-minute demonstration)
# Start at 120 seconds (2:00)
START_OFFSET_SECONDS = '120s'
# End at 300 seconds (5:00)
END_OFFSET_SECONDS = '300s'
# Custom Frame Rate: 5 FPS (default is 1 FPS)
CUSTOM_FPS = 5

def analyze_full_video_summary(client: genai.Client, video_uri: str) -> str:
    """
    Analyzes the entire video URL using default settings (1 FPS) for a high-level summary.
    This is token-efficient for long videos when high detail is not needed.
    """
    print(f"\n--- 1. Generating Full Video Summary for: {video_uri} ---")
    
    # Prompt for broad summarization
    prompt_text = (
        "Provide a comprehensive, high-level summary of this entire video. "
        "Identify the main topic, the speaker's core thesis, and the conclusion."
    )
    
    try:
        # Create the content parts: Video URI first, then the text prompt (Best Practice)
        contents = types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(file_uri=video_uri)
                ),
                types.Part(text=prompt_text)
            ]
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        
        return response.text

    except APIError as e:
        return f"An API error occurred during full analysis: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def analyze_clipped_segment(client: genai.Client, video_uri: str, start_s: str, end_s: str, fps: int) -> str:
    """
    Analyzes a specific clipped segment of the video at a custom, higher FPS.
    This maximizes detail and temporal precision within a focused window.
    """
    print(f"\n--- 2. Analyzing Clipped Segment ({start_s} to {end_s}) at {fps} FPS ---")
    
    # Prompt for detailed event extraction and timestamping
    prompt_text = (
        "Perform a detailed, frame-by-frame analysis of this clip. "
        "Identify every major action, event, or change in the visual or audio stream. "
        "For each event, provide a precise timestamp in MM:SS format and a brief description. "
        "Structure the output as a chronological list of key events."
    )
    
    try:
        # 1. Define the VideoMetadata for clipping and custom FPS
        metadata = types.VideoMetadata(
            start_offset=start_s,
            end_offset=end_s,
            fps=fps  # Override the default 1 FPS sampling rate
        )

        # 2. Create the content part, attaching the metadata to the video part
        video_part = types.Part(
            file_data=types.FileData(file_uri=video_uri),
            video_metadata=metadata  # Apply the clipping and FPS settings here
        )
        
        # 3. Assemble the final contents array
        contents = types.Content(
            parts=[
                video_part,
                types.Part(text=prompt_text)
            ]
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        
        return response.text

    except APIError as e:
        return f"An API error occurred during clipped analysis: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def main():
    """Main execution function to run the video indexing pipeline."""
    # Ensure the API key is set
    if 'GEMINI_API_KEY' not in os.environ:
        print("Error: The GEMINI_API_KEY environment variable is not set.")
        print("Please set your API key to run this script.")
        sys.exit(1)

    # Initialize the client
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")
        sys.exit(1)

    print("--- Starting Advanced Video Indexing Pipeline ---")
    print(f"Target Video: {YOUTUBE_URL}")
    print(f"Model Used: {MODEL_NAME}")
    
    start_time = time.time()

    # --- Step 1: Broad Analysis (Full Video Summary) ---
    full_summary = analyze_full_video_summary(client, YOUTUBE_URL)
    print("\n==================================================")
    print("✅ Full Video Summary (Default 1 FPS Analysis):")
    print("==================================================")
    print(full_summary)

    # --- Step 2: Targeted Analysis (Clipped Segment Detail) ---
    detailed_analysis = analyze_clipped_segment(
        client, 
        YOUTUBE_URL, 
        START_OFFSET_SECONDS, 
        END_OFFSET_SECONDS, 
        CUSTOM_FPS
    )
    print("\n==================================================")
    print(f"🔬 Detailed Segment Analysis (Clipped, {CUSTOM_FPS} FPS):")
    print("==================================================")
    print(detailed_analysis)
    
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()

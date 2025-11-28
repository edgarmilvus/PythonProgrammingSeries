
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
import time
from typing import Optional

# --- Configuration ---
# Initialize the client. Assumes GOOGLE_API_KEY is set in the environment.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Ensure GOOGLE_API_KEY is set. Details: {e}")
    # Proceeding for demonstration purposes, but API calls will fail without a key.
    pass

# --- Utility Function for File API Cleanup ---
def delete_uploaded_file(file_handle: Optional[types.File] = None):
    """Deletes an uploaded file if a valid file handle is provided."""
    if file_handle:
        try:
            print(f"\nAttempting to delete file: {file_handle.name}...")
            client.files.delete(name=file_handle.name)
            print("File deleted successfully.")
        except Exception as e:
            print(f"Warning: Could not delete file {file_handle.name}. Error: {e}")

# --- Placeholder Variables ---
# In a real-world scenario, you would replace these paths.
LOCAL_SMALL_VIDEO_PATH = "path/to/local/small_video.mp4"  # Assume < 20MB
LOCAL_LARGE_VIDEO_PATH = "path/to/local/large_movie.mp4"  # Assume > 20MB or > 1 minute
YOUTUBE_URL = "https://www.youtube.com/watch?v=9hE5-98ZeCg" # Example public NASA video URL

# --- Simulation for inline data (Exercise 2) ---
# Since we cannot guarantee a local video file exists, we simulate the reading process.
try:
    # Mocking byte data if the file doesn't exist for demonstration purposes
    if os.path.exists(LOCAL_SMALL_VIDEO_PATH):
        with open(LOCAL_SMALL_VIDEO_PATH, 'rb') as f:
            MOCK_VIDEO_BYTES = f.read()
    else:
        # Mocking byte data for demonstration
        MOCK_VIDEO_BYTES = b'\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6f\x6d' * 1000 
except Exception:
    MOCK_VIDEO_BYTES = b''
    print(f"Warning: Could not read dummy file. Using empty bytes.")

# --- Exercise 1: Quick Summarization using YouTube URL (Foundational) ---
def exercise_1_youtube_summarization():
    """Analyzes a public YouTube video URL."""
    print("\n--- Exercise 1: YouTube URL Summarization ---")
    prompt = "Analyze this video: What is the main subject, what is the mood, and what key facts are presented? Structure your answer in three paragraphs."

    try:
        # Use types.FileData with file_uri pointing to the YouTube link
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part(
                    file_data=types.FileData(
                        file_uri=YOUTUBE_URL,
                        mime_type='video/mp4' # Mime type is recommended
                    )
                ),
                types.Part(text=prompt)
            ]
        )
        print("Response Text:")
        print(response.text)

    except Exception as e:
        print(f"An error occurred during Exercise 1 (Check API Key/Connection): {e}")

# --- Exercise 2: Inline Data Analysis (Intermediate/Constraint Awareness) ---
def exercise_2_inline_analysis():
    """Analyzes a small video file by passing data inline (<20MB)."""
    print("\n--- Exercise 2: Inline Data Analysis (<20MB Constraint) ---")

    if not MOCK_VIDEO_BYTES:
        print("Skipping Exercise 2: Mock video bytes are empty. Cannot simulate inline data.")
        return

    prompt = "Based on this short clip, identify all visible objects and describe the primary action occurring. Be concise."

    try:
        # Use types.Part with inline_data and types.Blob for binary transfer
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=types.Content(
                parts=[
                    types.Part(
                        inline_data=types.Blob(
                            data=MOCK_VIDEO_BYTES,
                            mime_type='video/mp4'
                        )
                    ),
                    types.Part(text=prompt)
                ]
            )
        )
        print("Response Text:")
        print(response.text)

    except Exception as e:
        print(f"An error occurred during Exercise 2 (Check API Key/Connection): {e}")

# --- Exercise 3: Long-Form Media Analysis using File API (Advanced/Resource Management) ---
def exercise_3_file_api_long_analysis():
    """Uploads a large video file using the File API for detailed analysis."""
    print("\n--- Exercise 3: File API Upload for Long-Form Analysis ---")

    uploaded_file = None
    try:
        # 1. Upload the file (required for files > 20MB or long duration)
        print(f"Simulating upload of large file from: {LOCAL_LARGE_VIDEO_PATH}")
        
        # NOTE: This call requires a real file path to succeed.
        uploaded_file = client.files.upload(file=LOCAL_LARGE_VIDEO_PATH)
        print(f"File uploaded successfully. File URI: {uploaded_file.uri}")

        # 2. Generate content using the file reference
        prompt = "Provide a detailed, time-stamped summary of the first five key events in this long video. Focus on scene changes and dialogue."
        
        response = client.models.generate_content(
            model="gemini-2.5-pro", # Using Pro for deeper, long-context analysis
            contents=[
                uploaded_file, # Passing the file object directly
                prompt
            ]
        )
        print("Response Text:")
        print(response.text)
        return uploaded_file

    except FileNotFoundError:
        print(f"Skipping Exercise 3: File not found at {LOCAL_LARGE_VIDEO_PATH}. Cannot simulate File API upload.")
        return None
    except Exception as e:
        print(f"An error occurred during Exercise 3: {e}")
        return None
    finally:
        # 3. Cleanup (Moved to the end of Exercise 4 to allow reuse)
        # delete_uploaded_file(uploaded_file)
        pass 

# --- Exercise 4: Temporal Focusing via Clipping and Custom FPS (Modification Challenge) ---
def exercise_4_temporal_focus(file_to_reuse: Optional[types.File]):
    """Analyzes a specific clip (1:00 to 1:30) of a video using custom FPS."""
    print("\n--- Exercise 4: Temporal Focusing (Clipping & Custom FPS) ---")
    
    # Determine the file source and cleanup strategy
    cleanup_needed = False
    
    if file_to_reuse:
        # Reuse the uploaded file from Ex 3
        print(f"Reusing File API reference: {file_to_reuse.name}")
        file_part = types.Part(
            file_data=types.FileData(file_uri=file_to_reuse.uri),
            video_metadata=types.VideoMetadata(
                start_offset='60s',   # Clip start at 60 seconds
                end_offset='90s',     # Clip end at 90 seconds (30 second clip)
                fps=5                 # Sample 5 frames per second
            )
        )
        cleanup_needed = True
    else:
        # Fallback to YouTube URL for demonstration
        print("Falling back to YouTube URL for temporal focusing demonstration.")
        file_part = types.Part(
            file_data=types.FileData(file_uri=YOUTUBE_URL),
            video_metadata=types.VideoMetadata(
                start_offset='10s', 
                end_offset='20s',  
                fps=5                 
            )
        )

    prompt = "Analyze the actions and environment shown specifically between the clip start and end points. Given the high FPS, identify any rapid movements or fleeting details."

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                file_part,
                types.Part(text=prompt)
            ]
        )
        print("Response Text:")
        print(response.text)

    except Exception as e:
        print(f"An error occurred during Exercise 4: {e}")
    finally:
        if cleanup_needed:
            delete_uploaded_file(file_to_reuse)


# --- Exercise 5: Structured Event Indexing with Timestamp RAG (Expert/Robotics) ---
def exercise_5_structured_indexing():
    """Uses System Instructions and specific timestamp references to create a structured index of events."""
    print("\n--- Exercise 5: Structured Event Indexing ---")

    # Define system instruction for structured JSON output
    system_instruction = (
        "You are an automated video indexing system for a robotic platform. "
        "Your task is to analyze the video and identify three critical events that occur around the specified timestamps (00:05, 00:15, 00:25). "
        "For each event, output a JSON object containing the 'timestamp' (MM:SS), a brief 'description' of the visual event, and a 'confidence_score' (0.0 to 1.0). "
        "Do not include any introductory or concluding text."
    )

    prompt = (
        "Generate the structured index for the events near 00:05, 00:15, and 00:25. "
        "Ensure the output is a single parsable JSON array."
    )

    try:
        # Use YouTube URL and apply the system instruction
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[
                types.Part(
                    file_data=types.FileData(file_uri=YOUTUBE_URL)
                ),
                types.Part(text=prompt)
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        print("System Instruction Used:", system_instruction)
        print("Prompt Used:", prompt)
        print("\nStructured JSON Output (Response Text):")
        print(response.text)

    except Exception as e:
        print(f"An error occurred during Exercise 5: {e}")

# --- Execution Block ---
if __name__ == "__main__":
    
    # Run Exercise 1
    exercise_1_youtube_summarization()

    # Run Exercise 2
    exercise_2_inline_analysis()

    # Run Exercise 3 (This returns the file handle if successful)
    # Note: This will likely fail if LOCAL_LARGE_VIDEO_PATH is not a real file.
    uploaded_file_handle = exercise_3_file_api_long_analysis()

    # Run Exercise 4 (Reusing the handle or falling back to URL). Cleanup happens here.
    exercise_4_temporal_focus(uploaded_file_handle)

    # Run Exercise 5
    exercise_5_structured_indexing()

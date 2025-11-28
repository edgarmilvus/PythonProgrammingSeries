
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
import sys
from google import genai
from google.genai.errors import APIError

# --- Configuration and Setup ---
# Initialize the client. Assumes GEMINI_API_KEY is set in environment.
try:
    client = genai.Client()
except Exception as e:
    # Basic error handling for initialization failure
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is configured correctly.")
    sys.exit(1)

# Define the local path to the audio file
# This name reflects the long-form content typical of a podcast.
LOCAL_AUDIO_PATH = "sample_podcast.mp3"
MODEL_TO_USE = "gemini-2.5-flash" # Excellent balance of speed and multimodal capability

# --- Utility Function for File Simulation ---
def create_placeholder_file(path):
    """Creates a dummy file to simulate the presence of a large audio file."""
    try:
        # We create a file that is non-empty to satisfy the upload requirement,
        # though in a real scenario, this must be a valid audio file (e.g., MP3, WAV).
        with open(path, 'wb') as f:
            # Writing 1MB of null bytes to simulate a substantial file size
            f.write(b'\x00' * 1024 * 1024)
        print(f"Created placeholder file: {path} (1MB)")
    except IOError as e:
        print(f"Error creating placeholder file: {e}")
        sys.exit(1)

# --- Step 1: File Preparation and Existence Check ---
if not os.path.exists(LOCAL_AUDIO_PATH):
    # In a real application, you would ensure the file is downloaded or accessible.
    print(f"Audio file '{LOCAL_AUDIO_PATH}' not found locally.")
    create_placeholder_file(LOCAL_AUDIO_PATH)

# Variable to hold the reference to the uploaded file
uploaded_file = None

try:
    # --- Step 2: Upload the Audio File using the Files API ---
    print(f"\n[INFO] Starting upload of {LOCAL_AUDIO_PATH}. Using Files API for robustness.")
    
    # The client.files.upload method handles large files efficiently, 
    # transferring the data and returning a file object reference.
    uploaded_file = client.files.upload(file=LOCAL_AUDIO_PATH)
    
    print(f"[SUCCESS] File uploaded. URI: {uploaded_file.uri}")
    print(f"MIME Type detected: {uploaded_file.mime_type}")

    # --- Step 3: Define the Prompt and Generate Content ---
    # We use a structured system instruction approach for consistent output quality.
    analysis_prompt = (
        "You are an expert podcast analyst. Analyze the uploaded audio file. "
        "Provide a summary in markdown format with the following sections:\n\n"
        "## Summary\n[Concise overview of the content]\n\n"
        "## Key Takeaways\n- [Takeaway 1]\n- [Takeaway 2]\n- [Takeaway 3]\n\n"
        "## Technical Vocabulary\n[List of 5 specific technical terms mentioned]"
    )

    print(f"\n[INFO] Sending analysis request to model: {MODEL_TO_USE}...")
    
    # The contents list is multimodal: it combines the text prompt and the file object reference.
    response = client.models.generate_content(
        model=MODEL_TO_USE,
        contents=[analysis_prompt, uploaded_file]
    )

    # --- Step 4: Display Results ---
    print("\n" + "="*50)
    print("         GEMINI AUDIO ANALYSIS RESULT")
    print("="*50)
    print(response.text)
    print("="*50)

except APIError as e:
    print(f"\n[ERROR] Gemini API call failed: {e}")
except Exception as e:
    print(f"\n[ERROR] An unexpected error occurred: {e}")

finally:
    # --- Step 5: Clean Up Resources ---
    # It is crucial to delete uploaded files to manage storage and costs.
    if uploaded_file:
        try:
            print(f"\n[INFO] Cleaning up uploaded file: {uploaded_file.name}")
            client.files.delete(name=uploaded_file.name)
            print("[SUCCESS] Remote file cleanup complete.")
        except Exception as e:
            print(f"[WARNING] Could not delete remote file: {e}")
            
    # Clean up the local placeholder file
    if os.path.exists(LOCAL_AUDIO_PATH):
        os.remove(LOCAL_AUDIO_PATH)
        print(f"[SUCCESS] Local placeholder file removed: {LOCAL_AUDIO_PATH}")


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

# All Python code for Exercises 1-5 will be contained in this block.
import os
import time
from google import genai
from google.genai import types
# Note: pydub requires ffmpeg to be installed on the system to handle MP3s.
try:
    from pydub import AudioSegment
except ImportError:
    print("Warning: pydub not found. Please install: pip install pydub")
    # Define a dummy class if pydub is missing to prevent immediate crash,
    # though the audio generation will fail if pydub is truly needed.
    class AudioSegment:
        @staticmethod
        def silent(duration, frame_rate):
            return None
        @staticmethod
        def export(self, path, format):
            raise NotImplementedError("pydub is required to generate dummy audio.")

# --- Configuration ---
# Ensure your API key is configured.
try:
    # Attempt to initialize client. Assumes GEMINI_API_KEY is set in environment.
    client = genai.Client()
except Exception as e:
    # Fallback for environment setup issues
    print(f"Error: Client initialization failed. Ensure GEMINI_API_KEY is set. Details: {e}")
    exit()

MODEL_ID = "gemini-2.5-flash"
AUDIO_FILE_PATH = "podcast_sample.mp3"

# --- Utility Function: Generate Dummy Audio ---
def generate_dummy_audio(path, duration_ms=15000):
    """Generates a silent MP3 file for testing."""
    if os.path.exists(path):
        print(f"Using existing dummy file: {path}")
        return

    print(f"Generating a {duration_ms/1000} second silent MP3 file...")
    try:
        # Create 15 seconds of silence (15000 milliseconds)
        silent_audio = AudioSegment.silent(duration=duration_ms, frame_rate=44100)
        # Exporting requires ffmpeg/libav. If this fails, the user must install it.
        silent_audio.export(path, format="mp3")
        print(f"Dummy file generated at: {path}")
    except Exception as e:
        print(f"Error generating dummy audio. Ensure pydub and ffmpeg are installed and accessible. Error: {e}")
        exit()

# --- Utility Function: Clean up uploaded files ---
def cleanup_uploaded_file(client, file_object):
    """Deletes the file from the Gemini Files API."""
    if file_object and hasattr(file_object, 'name'):
        try:
            client.files.delete(name=file_object.name)
            print(f"\n[Cleanup] Successfully deleted file: {file_object.name}")
        except Exception as e:
            # File might already be deleted or expired
            print(f"\n[Cleanup Error] Could not delete file {file_object.name}: {e}")

# Generate the required dummy audio file
generate_dummy_audio(AUDIO_FILE_PATH)

print("\n" + "="*50)
print("STARTING PRACTICAL EXERCISES")
print("="*50 + "\n")

# =====================================================================
# EXERCISE 1: Robust Long-Form Transcription and Summarization
# =====================================================================

print("--- Exercise 1: Robust Long-Form Transcription and Summarization ---")
uploaded_file_e1 = None
try:
    # 1. Upload the file using the Files API (required for large files)
    print(f"1. Uploading {AUDIO_FILE_PATH} via Files API...")
    uploaded_file_e1 = client.files.upload(file=AUDIO_FILE_PATH)
    print(f"   Upload successful. File URI: {uploaded_file_e1.uri}")

    # 2. Construct the multimodal prompt
    prompt_e1 = """
    Analyze the provided audio file. You must perform two tasks:
    1. Generate a complete, accurate transcript of the speech.
    2. Based on the transcript, provide a concise summary using three bullet points.

    Format your response clearly, separating the transcript and the summary.
    """

    # 3. Generate content
    print("2. Generating content (Transcript and Summary)...")
    response_e1 = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt_e1, uploaded_file_e1]
    )

    print("\n--- E1 Result ---")
    print(response_e1.text)
    print("-----------------\n")

except Exception as e:
    print(f"An error occurred in Exercise 1: {e}")
finally:
    # 4. Cleanup
    cleanup_uploaded_file(client, uploaded_file_e1)


# =====================================================================
# EXERCISE 2: Inline Audio Data and Token Efficiency Check
# =====================================================================

print("--- Exercise 2: Inline Audio Data and Token Efficiency Check ---")
uploaded_file_e2_token_check = None
try:
    # 1. Read audio file into bytes
    with open(AUDIO_FILE_PATH, 'rb') as f:
        audio_bytes_e2 = f.read()

    # Create the inline audio part
    inline_audio_part = types.Part.from_bytes(
        data=audio_bytes_e2,
        mime_type='audio/mp3',
    )

    # 2. Generate content using inline data
    prompt_e2 = "Identify the type of sound and describe the environment in this clip."
    print("1. Generating content using inline audio data...")
    response_e2 = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt_e2, inline_audio_part]
    )

    print("\n--- E2 Result (Inline Analysis) ---")
    print(response_e2.text)

    # 3. Count tokens (Upload temporarily for accurate token count of the media)
    print("\n2. Uploading file temporarily to count tokens...")
    uploaded_file_e2_token_check = client.files.upload(file=AUDIO_FILE_PATH)
    
    count_response_e2 = client.models.count_tokens(
        model=MODEL_ID,
        contents=[uploaded_file_e2_token_check]
    )
    
    total_tokens = count_response_e2.total_tokens
    
    # Calculate expected tokens (15 seconds * 32 tokens/sec)
    expected_tokens = 15 * 32 

    print(f"3. Audio file duration: 15 seconds")
    print(f"   Gemini calculated tokens: {total_tokens}")
    print(f"   Expected tokens (15s * 32/s): {expected_tokens}")
    
    if total_tokens >= expected_tokens:
        print("   Token count verified (meets or slightly exceeds expected audio cost).")
    else:
        print("   Warning: Token count is unexpectedly low.")

except Exception as e:
    print(f"An error occurred in Exercise 2: {e}")
finally:
    # Clean up the token check file
    cleanup_uploaded_file(client, uploaded_file_e2_token_check)


# =====================================================================
# EXERCISE 3: Segmented Analysis and Time-Based Querying
# =====================================================================

print("--- Exercise 3: Segmented Analysis and Time-Based Querying ---")
uploaded_file_e3 = None
try:
    # 1. Upload the file
    uploaded_file_e3 = client.files.upload(file=AUDIO_FILE_PATH)
    
    # 2. Construct the time-based prompt using MM:SS format
    prompt_e3 = """
    Analyze the audio clip only between the timestamps 00:05 and 00:10.
    Based strictly on this 5-second segment, describe the speaker's tone (e.g., excited, neutral, serious)
    and hypothesize the main subject being discussed.
    """
    
    # 3. Generate content
    print("1. Generating content focused on segment 00:05 to 00:10...")
    response_e3 = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt_e3, uploaded_file_e3]
    )

    print("\n--- E3 Result (Segmented Analysis) ---")
    print(response_e3.text)
    print("--------------------------------------\n")

except Exception as e:
    print(f"An error occurred in Exercise 3: {e}")
finally:
    # 4. Cleanup
    cleanup_uploaded_file(client, uploaded_file_e3)


# =====================================================================
# EXERCISE 4: Advanced Challenge - Structured Data Refinement (Modification)
# =====================================================================

# Hypothetical Output Structure (from previous step):
HYPOTHETICAL_TRANSCRIPT = """
## Podcast Transcript (Structured)
| Timestamp | Speaker | Segment Content |
|---|---|---|
| 00:01 | Speaker A | Welcome back to the AI frontier. Today we're discussing the shift from LBYL to EAFP. |
| 00:05 | Speaker B | That's right. EAFP, or Easier to Ask for Forgiveness than Permission, is inherently more Pythonic. |
| 00:09 | Speaker A | It often leads to cleaner code, especially when dealing with concurrent tasks using Context Variables. |
| 00:13 | Speaker B | Exactly. Trying to check every key beforehand, LBYL, slows down the flow and complicates asynchronous code. |
"""

# Problem: Take this existing structured transcript and use Gemini to perform a secondary, highly specific analysis.

# Define the technical context for the model
TECHNICAL_CONTEXT = """
Technical Definitions:
- EAFP (Easier to Ask for Forgiveness than Permission): A coding style common in Python that assumes the existence of valid keys or attributes and handles exceptions if the assumption proves false.
- Context Variables (`contextvars`): A mechanism for managing state that needs to be accessible across different parts of an asynchronous flow, providing a thread-safe and task-safe way to handle local global state.
- LBYL (Look Before You Leap): A coding style where explicit checks (like 'if key in dict:') are performed before attempting an action.
"""

prompt_e4 = f"""
{TECHNICAL_CONTEXT}

Analyze the following structured transcript:
---
{HYPOTHETICAL_TRANSCRIPT}
---

Your task is to perform a secondary analysis.
1. Identify all technical terms (like EAFP, LBYL, Context Variables) mentioned ONLY by 'Speaker B'.
2. Provide the definition for each identified term, using the Technical Definitions provided above.

Output the result strictly as a single JSON object with the following structure:
{{
  "speaker": "Speaker B",
  "analysis_date": "{time.strftime('%Y-%m-%d')}",
  "terms_identified": [
    {{"term": "TERM_NAME", "definition": "DEFINITION_TEXT"}},
    ...
  ]
}}
"""

try:
    print("1. Performing secondary analysis on structured text...")
    response_e4 = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt_e4]
    )

    print("\n--- E4 Result (Structured JSON Analysis) ---")
    print(response_e4.text)
    print("-------------------------------------------\n")

except Exception as e:
    print(f"An error occurred in Exercise 4: {e}")


# =====================================================================
# EXERCISE 5: Noise Reduction Simulation via System Instructions
# =====================================================================

print("--- Exercise 5: Noise Reduction Simulation via System Instructions ---")
uploaded_file_e5 = None
try:
    # 1. Upload the file
    uploaded_file_e5 = client.files.upload(file=AUDIO_FILE_PATH)
    
    # 2. Define the System Instruction to filter noise
    system_instruction_e5 = (
        "You are an expert audio transcriptionist specializing in cleaning up noisy recordings. "
        "Your primary directive is to ignore all non-speech audio (e.g., background music, static, sirens) "
        "and focus exclusively on generating a clean, accurate, and fluent transcript of the human speech."
    )
    
    # 3. Define the user prompt
    user_prompt_e5 = "Please generate the professional transcript of this recording."

    print("1. Generating transcript using strict System Instructions...")
    response_e5 = client.models.generate_content(
        model=MODEL_ID,
        contents=[user_prompt_e5, uploaded_file_e5],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction_e5
        )
    )

    print("\n--- E5 Result (Noise-Filtered Transcript) ---")
    print(f"System Instruction Used: '{system_instruction_e5[:80]}...'")
    print(response_e5.text)
    print("---------------------------------------------\n")

except Exception as e:
    print(f"An error occurred in Exercise 5: {e}")
finally:
    # 4. Cleanup
    cleanup_uploaded_file(client, uploaded_file_e5)

print("\n" + "="*50)
print("PRACTICAL EXERCISES COMPLETE")
print("Note: Since the dummy audio is silent, the transcripts will reflect silence or model inference about the environment.")
print("="*50)

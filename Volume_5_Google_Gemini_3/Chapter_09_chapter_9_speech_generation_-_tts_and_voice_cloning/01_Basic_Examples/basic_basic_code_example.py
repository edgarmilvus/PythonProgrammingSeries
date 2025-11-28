
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

from google import genai
from google.genai import types
import wave
import sys
import os

# --- 1. Helper Function: Writing PCM data to WAV file ---
# This function is crucial because the API returns raw Pulse-Code Modulation (PCM)
# audio data, which lacks the necessary header information for standard audio players.
# The 'wave' module adds this header, creating a playable .wav file.
def write_wav_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
   """
   Writes raw PCM audio data (bytes) to a standard WAV file.
   The parameters (rate=24000, channels=1, sample_width=2) match the fixed
   audio output specifications of the Gemini TTS models.
   """
   try:
      with wave.open(filename, "wb") as wf:
         # Set file parameters based on Gemini's fixed audio output format
         wf.setnchannels(channels)
         wf.setsampwidth(sample_width)
         wf.setframerate(rate)
         # Write the raw audio bytes
         wf.writeframes(pcm_data)
      print(f"\n[SUCCESS] Audio saved successfully to: {filename}")
   except Exception as e:
      print(f"\n[ERROR] Failed to write WAV file. Do you have sufficient permissions? Details: {e}")
      sys.exit(1)

# --- 2. Configuration and Client Setup ---
try:
    # Initialize the client. This assumes the GEMINI_API_KEY environment variable is set.
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client. Ensure API key is set. Details: {e}")
    sys.exit(1)

# Define the text we want the model to speak, including style guidance
TTS_PROMPT = "Say in a clear, informative tone: Welcome to the Python AI News Digest. Today, we cover the latest advancements in Retrieval-Augmented Generation and asynchronous LLM streaming."

# Define the output file name
OUTPUT_FILENAME = "news_digest_intro.wav"

# Select a voice from the 30 available options (e.g., 'Charon' is Informative)
# Refer to the voice options table for other styles (e.g., 'Kore', 'Puck', 'Zephyr').
SELECTED_VOICE = 'Charon'

print(f"Attempting to generate speech using voice: {SELECTED_VOICE}...")

# --- 3. API Call: Generating Single-Speaker TTS Content ---
try:
   response = client.models.generate_content(
      # CRITICAL: Use the specialized TTS preview model
      model="gemini-2.5-flash-preview-tts",
      contents=TTS_PROMPT,
      config=types.GenerateContentConfig(
         # CRITICAL: Specify that the desired output modality is AUDIO
         response_modalities=["AUDIO"],
         speech_config=types.SpeechConfig(
            # Configure for a single speaker using VoiceConfig
            voice_config=types.VoiceConfig(
               prebuilt_voice_config=types.PrebuiltVoiceConfig(
                  # Specify the chosen voice name string
                  voice_name=SELECTED_VOICE,
               )
            )
         ),
      )
   )

   # --- 4. Data Extraction and Handling ---
   # The audio data is nested deeply within the response candidate structure.
   # We access the raw bytes via the 'inline_data.data' path.
   
   # Use EAFP (Easier to Ask for Forgiveness than Permission) to safely access nested attributes.
   try:
      # Extract the raw PCM audio bytes (this is a bytes object)
      audio_data = response.candidates[0].content.parts[0].inline_data.data
   except (AttributeError, IndexError) as e:
      print(f"\n[FAILURE] Failed to parse audio data from response structure: {e}")
      print("Check the model response status for potential errors.")
      sys.exit(1)


   # Check if data was successfully retrieved and is in the correct format
   if audio_data and isinstance(audio_data, bytes):
      print(f"Successfully retrieved {len(audio_data)} bytes of raw PCM audio data.")
      # Write the raw data to the WAV file using the helper function
      write_wav_file(OUTPUT_FILENAME, audio_data)
   else:
      print("\n[FAILURE] Audio data was empty or not in bytes format.")
      print("This usually indicates an issue with the API request or the prompt.")

except Exception as e:
   print(f"\n[CRITICAL ERROR] An unexpected error occurred during the API call: {e}")

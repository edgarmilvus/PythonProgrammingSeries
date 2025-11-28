
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

import asyncio
import io
import wave
from pathlib import Path
from google import genai
from google.genai import types
# External libraries needed for robust audio processing and format conversion
import soundfile as sf
import librosa

# --- 1. CONFIGURATION AND INITIAL SETUP ---

# Initialize the Gemini Client
# Ensure your GEMINI_API_KEY environment variable is set
client = genai.Client()

# Define the specific model optimized for low-latency, native audio interactions
# This model is specifically tuned for real-time speech processing.
MODEL_NAME = "gemini-2.5-flash-native-audio-preview-09-2025"

# Define the configuration for the Live API session
LIVE_API_CONFIG = {
  # CRITICAL: Request the response to be streamed back as raw audio data
  "response_modalities": ["AUDIO"],
  # Set a basic persona for the assistant
  "system_instruction": "You are a friendly, concise assistant specializing in programming topics. Keep your answers brief.",
}

# Define file paths
# NOTE: You must provide a valid WAV file named 'sample_input.wav' in the same directory.
INPUT_WAV_PATH = "sample_input.wav" 
OUTPUT_WAV_PATH = "assistant_response.wav" # Where the streamed response will be saved

# --- 2. AUDIO PREPARATION UTILITY ---

def prepare_audio_for_gemini(input_path: str) -> bytes:
    """
    Loads a WAV file and converts it to the required 16kHz, 16-bit PCM mono format.
    The Live API requires this specific format for input streaming.
    """
    try:
        # Load the audio file using librosa, resampling to the required 16000 Hz
        # librosa handles complex audio loading and resampling efficiently.
        y, sr = librosa.load(input_path, sr=16000)
        
        # Use an in-memory buffer (BytesIO) to hold the raw audio data temporarily
        buffer = io.BytesIO()
        
        # Write the raw PCM 16-bit data to the buffer using soundfile
        # 'RAW' format and 'PCM_16' subtype ensure the data is uncompressed and 16-bit
        sf.write(buffer, y, sr, format='RAW', subtype='PCM_16')
        
        # Rewind the buffer pointer to the beginning so we can read the content
        buffer.seek(0)
        
        # Read the raw bytes required by the API
        return buffer.read()
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        print("ACTION REQUIRED: Please ensure you have a WAV file named 'sample_input.wav' in this directory.")
        return b''
    except Exception as e:
        print(f"An error occurred during audio preparation: {e}")
        return b''


# --- 3. MAIN ASYNCHRONOUS EXECUTION LOOP ---

async def run_live_session():
    """
    Manages the asynchronous connection, sending of audio, and receiving of the response stream.
    """
    
    # 3.1. Prepare Input Data
    print(f"Attempting to prepare audio from: {INPUT_WAV_PATH}")
    audio_input_bytes = prepare_audio_for_gemini(INPUT_WAV_PATH)
    if not audio_input_bytes:
        print("Exiting session due to input preparation failure.")
        return # Exit if file preparation failed

    print(f"Starting Live API session with model: {MODEL_NAME}")
    
    # 3.2. Establish Bidirectional WebSocket Connection
    # 'client.aio' indicates the asynchronous interface.
    # 'live.connect' initiates the WebSocket handshake.
    async with client.aio.live.connect(model=MODEL_NAME, config=LIVE_API_CONFIG) as session:
        
        # 3.3. Send the Audio Input
        print(f"Sending {len(audio_input_bytes)} bytes of pre-formatted audio data...")
        
        # The audio data is wrapped in a types.Blob object, specifying the exact format.
        await session.send_realtime_input(
            audio=types.Blob(
                data=audio_input_bytes, 
                mime_type="audio/pcm;rate=16000" # Match the prepared format
            )
        )

        # 3.4. Prepare Output File Writer (WAV format)
        # We must set the file parameters based on the API's guaranteed output format.
        wf = wave.open(OUTPUT_WAV_PATH, "wb")
        wf.setnchannels(1)       # Mono channel
        wf.setsampwidth(2)       # 16-bit depth (2 bytes)
        wf.setframerate(24000)   # Set the expected output sample rate (24kHz is standard for Gemini TTS)

        print("Awaiting streamed audio response from Gemini...")
        
        # 3.5. Process the Incoming Stream
        # The 'session.receive()' method yields responses as soon as they arrive over the socket.
        async for response in session.receive():
            # Check if the response object contains raw audio data chunks
            if response.data is not None:
                # Write the received raw audio chunk directly to the output WAV file
                wf.writeframes(response.data)
                # print(f"Received audio chunk of size {len(response.data)} bytes.")
            
            # Check the server metadata to see if the model has finished its turn
            if response.server_content and response.server_content.turnComplete:
                print("--- Model turn complete. Ending response stream. ---")
                break # Exit the loop once the full response is streamed
                
        # 3.6. Clean Up
        wf.close()
        print(f"\nSession complete. Spoken response saved to '{OUTPUT_WAV_PATH}'.")


# --- 4. ASYNCHRONOUS ENTRY POINT ---
if __name__ == "__main__":
    # The entire process must be run within an asyncio event loop
    asyncio.run(run_live_session())

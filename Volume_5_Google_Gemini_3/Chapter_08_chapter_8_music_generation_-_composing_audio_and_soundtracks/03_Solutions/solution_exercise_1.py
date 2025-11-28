
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

import asyncio
import time
import wave
import os
from google import genai
from google.genai import types

# --- Configuration (Modified per Exercise) ---
MUSIC_MODEL = 'models/lyria-realtime-exp'
# OUTPUT_FILENAME and GENERATION_DURATION_SECONDS will be defined per exercise
client = genai.Client(http_options={'api_version': 'v1alpha'})

# --- Audio Utility Class ---
class AudioFileWriter:
    """
    A utility class to handle writing raw PCM audio chunks to a WAV file.
    Specifications are fixed per Lyria RealTime docs: 48kHz, 2 channels, 16-bit PCM.
    """
    def __init__(self, filename: str, sample_rate: int = 48000, channels: int = 2, bit_depth: int = 16):
        self.filename = filename
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth
        self.wav_file = None
        self.start_time = time.time()
        
        # Calculate sample width (bytes per sample): 16 bits = 2 bytes
        self.sampwidth = self.bit_depth // 8

    def open(self):
        """Initializes the WAV file writer."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Existing file '{self.filename}' overwritten.")
            
        self.wav_file = wave.open(self.filename, 'wb')
        self.wav_file.setnchannels(self.channels)
        self.wav_file.setsampwidth(self.sampwidth)
        self.wav_file.setframerate(self.sample_rate)
        print(f"--- Starting recording to {self.filename} ---")

    def write_chunk(self, audio_data: bytes):
        """Writes a chunk of raw audio data to the file."""
        if self.wav_file:
            self.wav_file.writeframes(audio_data)

    def close(self):
        """Closes the WAV file."""
        if self.wav_file:
            self.wav_file.close()
            duration = time.time() - self.start_time
            print(f"--- Recording finished. Total duration: {duration:.2f} seconds. ---")
            print(f"Audio saved successfully to {self.filename}")


# --- Asynchronous Music Generation Logic ---

async def receive_audio(session, audio_writer: AudioFileWriter):
    """
    Background task to continuously receive and process incoming audio chunks.
    """
    print("Audio receiver task started.")
    try:
        async for message in session.receive():
            if (message.server_content and 
                message.server_content.audio_chunks and 
                message.server_content.audio_chunks[0].data):
                
                audio_data = message.server_content.audio_chunks[0].data
                audio_writer.write_chunk(audio_data)
                
            await asyncio.sleep(10**-12) 
            
    except asyncio.CancelledError:
        print("Audio receiving task cancelled.")
    except Exception as e:
        print(f"An error occurred in receive_audio: {e}")

# Note: generate_music_session will be defined/modified within each exercise solution.


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

# Source File: theory_theoretical_foundations_part5.py
# Description: Theoretical Foundations
# ==========================================

import asyncio
import time
import base64
from google import genai
from google.genai import types
from typing import Optional

# CRITICAL: Lyria RealTime is an experimental model and requires the v1alpha API version.
client = genai.Client(http_options={'api_version': 'v1alpha'})
MODEL_NAME = 'models/lyria-realtime-exp'

# --- 1. Audio Processing Placeholder ---

class AudioProcessor:
    """
    A placeholder class to simulate audio buffering and playback.
    In a real application, this would interface with a library like 'sounddevice'
    to write raw PCM data (48kHz, 16-bit stereo) to the speaker output.
    """
    def __init__(self):
        self.total_chunks = 0
        self.start_time = time.time()

    def process_chunk(self, audio_data: bytes):
        """Processes a single raw audio chunk."""
        self.total_chunks += 1
        # In a real scenario, audio_data (raw 16-bit PCM bytes) would be
        # written to an audio buffer queue here.
        if self.total_chunks % 100 == 0:
            elapsed = time.time() - self.start_time
            print(f"| [AUDIO RECEIVER] Received {self.total_chunks} chunks. Time elapsed: {elapsed:.2f}s")
            
    def get_status(self):
        return f"Processed {self.total_chunks} audio chunks."

# --- 2. Asynchronous Receiver Task ---

async def receive_audio_task(session: genai.aio.live.music.MusicSession, processor: AudioProcessor):
    """
    The concurrent task responsible for continuously receiving audio data
    via the persistent WebSocket connection.
    """
    print("--- Receiver Task Started: Waiting for audio stream... ---")
    try:
        # Use async for to non-blockingly iterate over incoming messages
        async for message in session.receive():
            
            # Check for server content and audio chunks as per documentation
            if message.server_content and message.server_content.audio_chunks:
                # The data is delivered as a base64 encoded string, which must be decoded
                for chunk in message.server_content.audio_chunks:
                    raw_pcm_data = base64.b64decode(chunk.data)
                    processor.process_chunk(raw_pcm_data)
                    
            # Check for filtered prompts (safety mechanism)
            if message.server_content and message.server_content.filtered_prompt:
                print(f"\n[WARNING] Prompt was filtered: {message.server_content.filtered_prompt}")
                
            # Yield control briefly to ensure responsiveness
            await asyncio.sleep(10**-12) 
            
    except asyncio.CancelledError:
        print("--- Receiver Task Cancelled (Session Closed) ---")
    except Exception as e:
        print(f"--- Receiver Task Error: {e} ---")

# --- 3. Main Control Flow ---

async def main():
    """
    Establishes the Lyria RealTime session and manages the control flow.
    """
    processor = AudioProcessor()
    
    print(f"Attempting to connect to Lyria RealTime model: {MODEL_NAME}")
    
    try:
        # Use the asynchronous context manager for the Live API connection
        async with (
            client.aio.live.music.connect(model=MODEL_NAME) as session,
            # Use TaskGroup to safely manage the concurrent receiver task
            asyncio.TaskGroup() as tg,
        ):
            print("Connection successful. Starting concurrent tasks.")
            
            # Start the audio receiver task in the background
            tg.create_task(receive_audio_task(session, processor))
            
            # --- PHASE 1: Initial Configuration ---
            
            print("\n[PHASE 1] Setting initial configuration and prompt...")
            
            # Set the initial weighted prompts (Genre, Instrument, Mood)
            await session.set_weighted_prompts(
                prompts=[
                    types.WeightedPrompt(text='Lo-Fi Hip Hop', weight=1.0),
                    types.WeightedPrompt(text='Rhodes Piano', weight=0.7),
                    types.WeightedPrompt(text='Subdued Melody', weight=0.5),
                ]
            )
            
            # Set the initial music generation config
            initial_config = types.LiveMusicGenerationConfig(
                bpm=80,
                density=0.6,
                temperature=1.0,
                # Explicitly setting scale requires a reset if changed later
                scale=types.Scale.C_MAJOR_A_MINOR, 
                music_generation_mode=types.MusicGenerationMode.QUALITY,
            )
            await session.set_music_generation_config(config=initial_config)
            
            # Start the music stream
            await session.play()
            print("Music started. Listening for 10 seconds...")
            await asyncio.sleep(10)
            
            # --- PHASE 2: Real-Time Steering (Morphing the Music) ---
            
            print("\n[PHASE 2] Steering music: Introducing a new element (Acid Bass)...")
            
            # Decrease Lo-Fi influence and introduce a new, stronger element
            await session.set_weighted_prompts(
                prompts=[
                    types.WeightedPrompt(text='Lo-Fi Hip Hop', weight=0.3), # Reduced
                    types.WeightedPrompt(text='Rhodes Piano', weight=0.7),
                    types.WeightedPrompt(text='303 Acid Bass', weight=1.5), # New & strong
                    types.WeightedPrompt(text='Crunchy Distortion', weight=0.9),
                ]
            )
            print("Prompts updated. Model should smoothly transition. Listening for 10 seconds...")
            await asyncio.sleep(10)
            
            # --- PHASE 3: Hard Transition (Changing BPM and Scale) ---
            
            print("\n[PHASE 3] Hard transition: Changing BPM and Scale...")
            
            new_config = types.LiveMusicGenerationConfig(
                # Must supply ALL previous parameters, plus the new ones
                bpm=130, # Drastic change
                density=0.9, # Busier
                temperature=1.1,
                scale=types.Scale.D_MAJOR_B_MINOR, # New key
                music_generation_mode=types.MusicGenerationMode.DIVERSITY,
            )
            await session.set_music_generation_config(config=new_config)
            
            # CRITICAL: Reset context to force the model to adopt the new BPM/Scale
            await session.reset_context() 
            print("Context reset and configuration updated. Music should transition abruptly. Listening for 5 seconds...")
            await asyncio.sleep(5)
            
            # Stop playback
            await session.stop()
            print("\nPlayback stopped.")
            
    except genai.errors.APIError as e:
        print(f"\n[CRITICAL ERROR] Gemini API Error: {e}")
        print("Ensure your API key is correct and the model is accessible.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] An unexpected error occurred: {e}")
        
    finally:
        print(f"\n--- Session Summary ---")
        print(processor.get_status())
        print("Main function finished. TaskGroup ensures receiver cleanup.")

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())

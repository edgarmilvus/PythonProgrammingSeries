
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

import asyncio
import base64
import sys
from queue import Queue
from google import genai
from google.genai import types

# Note: PyAudio is required for real-time PCM playback.
# Installation: pip install PyAudio
try:
    import pyaudio
except ImportError:
    print("Error: PyAudio library is required for audio playback.")
    print("Please install it using: pip install PyAudio")
    sys.exit(1)

# --- Configuration Constants ---
MODEL_NAME = 'models/lyria-realtime-exp'
API_VERSION = 'v1alpha'

# Audio specifications based on Lyria RealTime documentation
SAMPLE_RATE = 48000  # Hz
CHANNELS = 2         # Stereo
FORMAT = pyaudio.paInt16 # 16-bit PCM

# --- Shared Resources ---
# Queue to pass audio chunks from the receiver task to the playback task
audio_queue = Queue()
# PyAudio instance and stream placeholder
p = None
stream = None


def initialize_audio_stream():
    """Initializes the global PyAudio instance and stream."""
    global p, stream
    p = pyaudio.PyAudio()
    # Open a non-blocking stream
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        output=True,
        frames_per_buffer=1024 # Buffer size for smooth playback
    )
    print("PyAudio stream initialized.")

def terminate_audio_stream():
    """Closes and terminates the PyAudio resources."""
    global p, stream
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()
    print("PyAudio stream terminated.")


async def audio_playback_task():
    """
    Task 1: Continuously pulls audio data from the queue and writes it
    to the PyAudio stream for playback.
    """
    print("Playback task started. Waiting for audio data...")
    while True:
        # Use asyncio.to_thread to run the blocking queue operation
        # in a separate thread, preventing the main event loop from freezing.
        try:
            # Get data from queue (blocking call, hence the use of to_thread)
            audio_chunk = await asyncio.to_thread(audio_queue.get)

            # Write the raw bytes to the output stream
            if stream and stream.is_active():
                stream.write(audio_chunk)
            
            # Signal that the item has been processed
            audio_queue.task_done()

        except Exception as e:
            # Handle stream closure or other playback errors
            if "closed" in str(e):
                break
            # print(f"Playback error: {e}")
            await asyncio.sleep(0.001)


async def receive_audio_task(session):
    """
    Task 2: Receives streaming audio chunks from the Lyria RealTime session,
    decodes them, and places them into the audio_queue.
    """
    print("Receiver task started. Listening for model output...")
    try:
        async for message in session.receive():
            if message.server_content and message.server_content.audio_chunks:
                # The API sends base64 encoded PCM data
                for chunk in message.server_content.audio_chunks:
                    audio_data = base64.b64decode(chunk.data)
                    audio_queue.put(audio_data)
            
            # Small yield to prevent blocking the event loop entirely
            await asyncio.sleep(10**-12)
    except Exception as e:
        print(f"\nReceiver task error (Likely stream closed): {e}")


async def control_loop_task(session):
    """
    Task 3: Manages user input and sends real-time steering commands
    (prompts and config updates) to the Lyria RealTime session.
    """
    print("\n--- Adaptive DJ Control Panel ---")
    print("Commands: 1: Chill Vibe | 2: Action Mode | 3: Tempo Up | Q: Quit")
    
    current_bpm = 100
    
    while True:
        # Use asyncio.to_thread for blocking input() call
        command = await asyncio.to_thread(input, f"BPM {current_bpm} > Enter command: ").strip().upper()

        if command == 'Q':
            print("Stopping music generation...")
            await session.stop()
            break
        
        elif command == '1':
            print(">>> Transitioning to Chill Vibe (Lo-Fi Hip Hop, 80 BPM)...")
            current_bpm = 80
            
            # 1. Update Prompts (Smooth transition)
            await session.set_weighted_prompts(
                prompts=[
                    types.WeightedPrompt(text='Lo-Fi Hip Hop', weight=1.0),
                    types.WeightedPrompt(text='Warm Acoustic Guitar', weight=0.8),
                    types.WeightedPrompt(text='Chill', weight=1.2),
                ]
            )
            
            # 2. Update Config (BPM and Scale change requires context reset)
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(
                    bpm=current_bpm,
                    scale=types.Scale.C_MAJOR_A_MINOR, # White keys, gentle
                    density=0.4, # Sparser notes
                    music_generation_mode=types.MusicGenerationMode.QUALITY
                )
            )
            await session.reset_context() # Force immediate application of BPM/Scale

        elif command == '2':
            print(">>> Transitioning to Action Mode (Drum & Bass, 160 BPM)...")
            current_bpm = 160
            
            # 1. Update Prompts (Drastic change)
            await session.set_weighted_prompts(
                prompts=[
                    types.WeightedPrompt(text='Drum & Bass', weight=1.5),
                    types.WeightedPrompt(text='Dirty Synths', weight=1.0),
                    types.WeightedPrompt(text='Huge Drop', weight=0.5),
                ]
            )
            
            # 2. Update Config
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(
                    bpm=current_bpm,
                    scale=types.Scale.D_FLAT_MAJOR_B_FLAT_MINOR, # More complex key
                    density=0.8, # Busier notes
                    guidance=5.0 # High guidance for strict adherence to D&B
                )
            )
            await session.reset_context() # Force immediate application of BPM/Scale

        elif command == '3':
            # Example of granular, continuous steering
            current_bpm += 10
            if current_bpm > 200:
                current_bpm = 200
            print(f">>> Increasing tempo to {current_bpm} BPM...")
            
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(
                    bpm=current_bpm,
                    # Must include existing parameters or they reset!
                    density=0.7, 
                    music_generation_mode=types.MusicGenerationMode.QUALITY
                )
            )
            await session.reset_context() # Required for BPM change


        else:
            print("Invalid command. Use 1, 2, 3, or Q.")


async def main():
    """The main asynchronous entry point for the Adaptive DJ."""
    global p, stream
    
    # 1. Initialize API Client
    client = genai.Client(http_options={'api_version': API_VERSION})
    
    # 2. Initialize PyAudio for playback
    initialize_audio_stream()

    try:
        # 3. Establish WebSocket Connection to Lyria RealTime
        async with (
            client.aio.live.music.connect(model=MODEL_NAME) as session,
            asyncio.TaskGroup() as tg,
        ):
            print("Successfully connected to Lyria RealTime.")
            
            # 4. Set up concurrent tasks
            # Task A: Handle incoming audio data from the server
            tg.create_task(receive_audio_task(session))
            # Task B: Play the audio data from the queue
            tg.create_task(audio_playback_task())
            
            # 5. Set Initial Configuration (Default State: Minimal Techno)
            initial_bpm = 100
            
            await session.set_weighted_prompts(
                prompts=[
                    types.WeightedPrompt(text='Minimal Techno', weight=1.0),
                    types.WeightedPrompt(text='Deep House', weight=0.5),
                    types.WeightedPrompt(text='Tight Groove', weight=1.0),
                ]
            )
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(
                    bpm=initial_bpm,
                    temperature=1.1,
                    density=0.7,
                    music_generation_mode=types.MusicGenerationMode.QUALITY
                )
            )

            # 6. Start Music Generation
            await session.play()
            print(f"Music started (Initial BPM: {initial_bpm}).")
            
            # 7. Start the control loop (This task keeps the session alive)
            await control_loop_task(session)
            
    except Exception as e:
        print(f"\n--- Critical Error in Main Loop ---")
        print(f"Ensure your API key is configured and you have network access.")
        print(f"Error details: {e}")
        
    finally:
        # 8. Clean up resources
        terminate_audio_stream()
        print("Application shutdown complete.")


if __name__ == "__main__":
    # Ensure the asyncio loop is run
    asyncio.run(main())

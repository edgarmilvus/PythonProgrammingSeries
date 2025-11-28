
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
import os
from google import genai
from google.genai import types

# --- Configuration Constants ---
# NOTE: Lyria RealTime is an experimental model and requires the v1alpha API version.
API_VERSION = 'v1alpha'
MODEL_NAME = 'models/lyria-realtime-exp'
OUTPUT_FILENAME = 'ambient_sketch_raw.pcm'
GENERATION_DURATION_SEC = 15

# --- Client Initialization ---
# Initialize the client, specifying the experimental API version
client = genai.Client(http_options={'api_version': API_VERSION})

async def receive_and_save_audio(session: genai.aio.live.music.LiveMusicSession, 
                                 output_path: str, 
                                 stop_event: asyncio.Event):
    """
    Background task to continuously receive audio chunks from the Lyria stream 
    and save them to a specified file.
    """
    print(f"-> Audio Receiver: Starting to listen and save to {output_path}...")
    
    # Open the file in binary write mode ('wb')
    # The output is raw 16-bit PCM audio bytes (not a standard WAV file header)
    try:
        with open(output_path, 'wb') as f:
            # Loop until the main session signals the stop_event
            while not stop_event.is_set():
                # Asynchronously iterate over incoming server messages
                async for message in session.receive():
                    # Check if the message contains audio chunks
                    if message.server_content and message.server_content.audio_chunks:
                        for chunk in message.server_content.audio_chunks:
                            # The 'data' field contains the raw audio bytes
                            f.write(chunk.data)
                            # We yield control briefly to ensure the loop doesn't block
                            await asyncio.sleep(0) # Minimal sleep
                    
                    # If the stop event is set mid-stream, break the inner loop
                    if stop_event.is_set():
                        break
    except Exception as e:
        print(f"-> Audio Receiver: An error occurred during streaming: {e}")
    finally:
        print(f"-> Audio Receiver: Finished saving audio. Total duration: {GENERATION_DURATION_SEC}s.")


async def generate_ambient_track(output_path: str, duration_sec: int):
    """
    Main asynchronous function to connect, configure, and manage the music generation session.
    """
    print(f"--- Starting Lyria RealTime Session (Model: {MODEL_NAME}) ---")
    
    # 1. Establish the persistent WebSocket connection
    # We use 'async with' to ensure the session is properly closed upon exit.
    try:
        async with (
            client.aio.live.music.connect(model=MODEL_NAME) as session,
            asyncio.TaskGroup() as tg,
        ):
            print("-> Connection established successfully.")
            
            # Create a shared event to signal the receiver task to stop
            stop_event = asyncio.Event()

            # 2. Start the background audio receiver task
            # This task runs concurrently, listening for incoming data.
            tg.create_task(receive_and_save_audio(session, output_path, stop_event))
            
            # 3. Define and send the initial weighted prompts
            # This tells the model what kind of music to generate.
            initial_prompts = [
                types.WeightedPrompt(text='Deep House', weight=1.0),
                types.WeightedPrompt(text='Ethereal Ambience', weight=0.7),
                types.WeightedPrompt(text='Smooth Pianos', weight=0.5),
            ]
            await session.set_weighted_prompts(prompts=initial_prompts)
            print("-> Prompts set: Deep House, Ethereal Ambience, Smooth Pianos.")

            # 4. Set the music generation configuration
            # This controls technical parameters like tempo and variability.
            # We set specific values for demonstration, though many are optional.
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(
                    bpm=120,               # Standard dance tempo
                    temperature=1.5,       # Higher temperature for more diversity/creativity
                    density=0.6,           # Moderately busy composition
                    guidance=4.0,          # Default guidance for prompt adherence
                    # Setting the scale is a drastic change, but useful for initial setup
                    scale=types.Scale.D_MAJOR_B_MINOR 
                )
            )
            print("-> Configuration set: BPM 120, Scale D Major, Temperature 1.5.")

            # 5. Start streaming music playback
            await session.play()
            print(f"-> Playback initiated. Streaming for {duration_sec} seconds...")

            # 6. Wait for the specified duration
            await asyncio.sleep(duration_sec)

            # 7. Stop the generation and signal the receiver
            await session.stop()
            stop_event.set()
            print("-> Playback stopped by timer.")
            
            # The TaskGroup waits for all tasks (including the receiver) to complete
            # before exiting the 'async with' block.

    except genai.errors.APIError as e:
        print(f"\n!!! API Error encountered: {e}")
        print("Ensure your API key is valid and the model is accessible.")
    except Exception as e:
        print(f"\n!!! An unexpected error occurred: {e}")

if __name__ == "__main__":
    print(f"Starting the Lyria RealTime music generation process.")
    print(f"Output file: {os.path.abspath(OUTPUT_FILENAME)}")
    
    # Run the main asynchronous function
    asyncio.run(generate_ambient_track(OUTPUT_FILENAME, GENERATION_DURATION_SEC))
    
    print("\n--- Generation Complete ---")
    print(f"Note: The file '{OUTPUT_FILENAME}' contains raw 16-bit PCM audio data (48kHz, stereo) and requires specialized software (like Audacity) for playback.")


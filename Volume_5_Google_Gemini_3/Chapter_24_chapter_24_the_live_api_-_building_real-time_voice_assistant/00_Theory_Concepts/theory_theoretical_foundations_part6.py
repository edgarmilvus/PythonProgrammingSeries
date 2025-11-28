
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

# Source File: theory_theoretical_foundations_part6.py
# Description: Theoretical Foundations
# ==========================================

import asyncio
import io
import wave
from google import genai
from google.genai import types
import librosa
import soundfile as sf
import datetime # Used for theoretical latency management (timedelta)

# The client must be initialized for asynchronous operations
client = genai.Client()

# Specialized model for low-latency audio interaction
LIVE_MODEL = "gemini-2.5-flash-native-audio-preview-09-2025"
INPUT_SAMPLE_RATE = 16000
OUTPUT_SAMPLE_RATE = 24000

# Configuration for the session
config = {
  "response_modalities": ["AUDIO"],
  "system_instruction": "You are a helpful assistant and answer in a friendly tone.",
}

async def process_live_audio(input_file_path: str, output_file_path: str):
    """
    Demonstrates the asynchronous flow of the Live API:
    1. Establish an async session (WebSocket connection).
    2. Format input audio to the required 16-bit PCM, 16kHz mono standard.
    3. Send the input using an Awaitable call.
    4. Stream the response using an async For Loop (asynchronous iterator).
    5. Save the 24kHz output audio chunks.
    """
    
    # 1. Establish the session (Awaitable connection)
    print(f"Connecting to Live API using model: {LIVE_MODEL}...")
    async with client.aio.live.connect(model=LIVE_MODEL, config=config) as session:
        
        # --- INPUT PREPARATION ---
        # Load and convert the audio file to the required 16kHz PCM format
        # This conversion step is crucial for the API to function correctly.
        buffer = io.BytesIO()
        try:
            # y: audio time series, sr: sample rate
            y, sr = librosa.load(input_file_path, sr=INPUT_SAMPLE_RATE)
            sf.write(buffer, y, sr, format='RAW', subtype='PCM_16')
            buffer.seek(0)
            audio_bytes = buffer.read()
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return

        # 2. Send Input (Awaitable operation)
        # This operation is an Awaitable; the coroutine pauses until the data is sent.
        start_send_time = datetime.datetime.now() # Start time for latency check
        print(f"Sending {len(audio_bytes)} bytes of audio input...")
        
        await session.send_realtime_input(
            audio=types.Blob(data=audio_bytes, mime_type=f"audio/pcm;rate={INPUT_SAMPLE_RATE}")
        )
        print("Input stream sent successfully.")

        # --- OUTPUT RECEPTION ---
        # 3. Setup output WAV file structure (1 channel, 16-bit, 24kHz output rate)
        wf = wave.open(output_file_path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(OUTPUT_SAMPLE_RATE)

        first_chunk_received = False
        
        # 4. Stream Response (Async For Loop)
        # The 'async for' loop iterates over the incoming stream of audio chunks.
        # This is a non-blocking iteration, essential for real-time performance.
        async for response in session.receive():
            
            # Use datetime.timedelta to measure Time-to-First-Byte (TTFB)
            if not first_chunk_received:
                first_chunk_received = True
                latency = datetime.datetime.now() - start_send_time
                # An ideal system aims for latency significantly less than 500ms
                print(f"\n--- First chunk received! TTFB: {latency.total_seconds():.3f} seconds ---")
            
            # Check if the response contains raw audio data
            if response.data is not None:
                # Write the raw audio data (24kHz chunks) immediately
                wf.writeframes(response.data)
        
        # Cleanup
        wf.close()
        print(f"\nStreaming complete. Response saved to {output_file_path}")

# Example of running the asynchronous main function
# Note: You would need a sample.wav file and the required libraries (librosa, soundfile) installed.
# if __name__ == "__main__":
#     # asyncio.run(process_live_audio("sample.wav", "response_audio.wav"))
#     pass # Placeholder to keep the code block runnable without dependencies


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
import io
import wave
from pathlib import Path
from google import genai
from google.genai import types
import soundfile as sf
import librosa

# --- Configuration Constants ---

# The model specified for native audio processing and low-latency interaction
LIVE_AUDIO_MODEL = "gemini-2.5-flash-native-audio-preview-09-2025"

# File paths for input and output
INPUT_WAV_PATH = "input_phrase.wav"
OUTPUT_WAV_PATH = "translated_response.wav"

# Required input audio format for the Live API
INPUT_SAMPLE_RATE = 16000
INPUT_CHANNELS = 1
INPUT_BIT_DEPTH = '16' # PCM 16-bit

# Output audio format received from the Live API
OUTPUT_SAMPLE_RATE = 24000
OUTPUT_CHANNELS = 1
OUTPUT_SAMPLE_WIDTH = 2 # 16-bit audio = 2 bytes per sample

# --- Helper Functions ---

def prepare_audio_for_gemini(file_path: str) -> bytes:
    """
    Loads an audio file and converts it into the raw PCM format required 
    by the Gemini Live API (16-bit PCM, 16kHz, mono).
    
    Args:
        file_path: Path to the input WAV file.
        
    Returns:
        Raw audio bytes ready for transmission.
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}. "
            "Please create a sample WAV file for input."
        )

    print(f"1. Loading and converting audio from: {file_path}")
    
    # 1. Load the audio file using librosa, forcing the required sample rate.
    # Librosa handles resampling and channel reduction (mono conversion) automatically 
    # when specifying 'sr' and not setting 'mono=False'.
    y, sr = librosa.load(file_path, sr=INPUT_SAMPLE_RATE, mono=True)
    
    # 2. Use an in-memory buffer (BytesIO) to hold the raw audio data.
    buffer = io.BytesIO()
    
    # 3. Write the audio data to the buffer in the required raw PCM format.
    # format='RAW' and subtype='PCM_16' ensure the data is uncompressed 
    # 16-bit Pulse-Code Modulation.
    sf.write(
        buffer, 
        y, 
        sr, 
        format='RAW', 
        subtype='PCM_16'
    )
    
    # 4. Reset the buffer position and read the raw bytes.
    buffer.seek(0)
    audio_bytes = buffer.read()
    
    print(f"   -> Conversion complete. Size: {len(audio_bytes)} bytes.")
    return audio_bytes


# --- Main Asynchronous Session ---

async def run_translation_session():
    """
    Establishes a connection to the Live API, sends audio input, and 
    streams the translated audio response back in real-time.
    """
    print("\n--- Starting Gemini Live API Translator Session ---")
    
    try:
        # Initialize the client. Assumes GEMINI_API_KEY is set in environment.
        client = genai.Client()
        
        # Define the session configuration
        config = {
            # We request AUDIO as the response modality for spoken output
            "response_modalities": ["AUDIO"],
            # Critical instruction: define the assistant's role and behavior
            "system_instruction": (
                "You are an expert, low-latency, real-time language translator. "
                "Translate the user's spoken input into French and respond only "
                "with the spoken translation. Do not add commentary."
            ),
        }

        # 1. Prepare the input audio data
        input_audio_bytes = prepare_audio_for_gemini(INPUT_WAV_PATH)
        
        # 2. Establish the asynchronous Live API connection
        # The 'async with' block ensures the connection is properly closed.
        async with client.aio.live.connect(model=LIVE_AUDIO_MODEL, config=config) as session:
            
            print("2. Live API connection established. Sending audio input...")

            # 3. Send the prepared audio data to the API
            await session.send_realtime_input(
                audio=types.Blob(
                    data=input_audio_bytes, 
                    mime_type=f"audio/pcm;rate={INPUT_SAMPLE_RATE}"
                )
            )

            # 4. Prepare the output WAV file writer
            wf = wave.open(OUTPUT_WAV_PATH, "wb")
            wf.setnchannels(OUTPUT_CHANNELS)
            wf.setsampwidth(OUTPUT_SAMPLE_WIDTH)
            wf.setframerate(OUTPUT_SAMPLE_RATE)
            
            print(f"3. Waiting for streamed response... Saving to {OUTPUT_WAV_PATH}")
            
            # 5. Process the streaming response chunks
            audio_chunks_received = 0
            async for response in session.receive():
                # The response object contains various fields (metadata, errors, data)
                
                # Check if the response contains raw audio data
                if response.data is not None:
                    # Write the received chunk immediately to the WAV file
                    wf.writeframes(response.data)
                    audio_chunks_received += 1
                    
                    # Optional: Print progress to simulate real-time feedback
                    if audio_chunks_received % 50 == 0:
                        print(f"   [Stream Progress] Received {audio_chunks_received} audio chunks...")

                # Check for server content, which includes metadata like turn completion
                if response.server_content:
                    # Check for turn completion signal
                    if response.server_content.turn_complete:
                        print("\n4. Model turn complete. Translation finished.")
                        break # Exit the loop once the response is fully received
                    
                    # Check for potential transcription or model text output
                    if response.server_content.model_turn and response.server_content.model_turn.parts:
                        # This section is useful for debugging the text content 
                        # generated by the model before it is converted to audio.
                        text_part = response.server_content.model_turn.parts[0]
                        if text_part.text:
                            print(f"   [Model Text] Intermediate Text: {text_part.text[:50]}...")

            # 6. Close the output file handle
            wf.close()
            
            if audio_chunks_received == 0:
                print("Error: No audio data was received from the API.")
            else:
                print(f"5. Session complete. Total audio chunks received: {audio_chunks_received}")

    except FileNotFoundError as e:
        print(f"\nCRITICAL ERROR: {e}")
        print("Please ensure your input audio file exists.")
    except genai.errors.APIError as e:
        print(f"\nAPI Error during session: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Execute the asynchronous main function
    asyncio.run(run_translation_session())

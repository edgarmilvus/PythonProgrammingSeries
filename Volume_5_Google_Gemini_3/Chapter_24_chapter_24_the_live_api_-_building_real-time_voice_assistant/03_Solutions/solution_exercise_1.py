
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
import io
from pathlib import Path
import wave
from google import genai
from google.genai import types
import soundfile as sf
import librosa
import datetime
import os

# --- Configuration and Setup ---

# Initialize the client (assumes GEMINI_API_KEY is set in environment)
# Ensure you have run: pip install librosa soundfile google-genai
client = genai.Client()
MODEL = "gemini-2.5-flash-native-audio-preview-09-2025"

# Utility function to process audio input from a WAV file
def prepare_audio_input(file_path: str) -> bytes:
    """Reads a WAV file and converts it to 16-bit PCM, 16kHz, mono format."""
    if not Path(file_path).exists():
        print(f"Error: Input file '{file_path}' not found.")
        return b''
        
    try:
        # Load audio and resample to 16000 Hz (required input rate)
        y, sr = librosa.load(file_path, sr=16000)
        
        # Write to an in-memory buffer as 16-bit PCM (RAW format)
        buffer = io.BytesIO()
        sf.write(buffer, y, sr, format='RAW', subtype='PCM_16')
        buffer.seek(0)
        return buffer.read()
    except Exception as e:
        print(f"Error preparing audio: {e}")
        return b''

# Utility function for streaming text output (Used in Exercise 1 & 2)
async def process_text_response(session, turn_number: int):
    """Handles streaming text responses from the session."""
    print(f"\n--- Turn {turn_number} Response (Streaming Text) ---")
    
    # We use a loop here to handle the response stream until the turn is complete
    async for response in session.receive():
        # Check for textual content
        if response.server_content and response.server_content.model_turn:
            for part in response.server_content.model_turn.parts:
                if part.text:
                    # Print chunks as they arrive (real-time streaming)
                    print(part.text, end="", flush=True)
        
        # Check for tool calls (relevant for Exercise 4, but included here for completeness)
        if response.server_content and response.server_content.tool_calls:
            # If a tool call is detected, we return it to be handled outside this function
            return response.server_content.tool_calls
            
        # Check if the turn is complete (optional, but good practice)
        if response.server_content and response.server_content.turn_complete:
            break
            
    print("\n--- Turn Complete ---")
    return None

# --- Exercise 1 & 2: Text Streaming and Context Management ---

async def main_text_context():
    """
    Exercise 1: Text-only streaming output.
    Exercise 2: Multi-turn conversation management.
    """
    print("="*60)
    print("Starting Exercise 1 & 2: Text Streaming and Multi-Turn Context...")
    print("="*60)

    # Configuration for text responses and system instruction (Exercise 2)
    config = {
      "response_modalities": ["TEXT"], # Exercise 1: Requesting text output
      "system_instruction": "You are a geographical expert and answer questions concisely.", # Exercise 2: Context setup
    }

    # Prepare input audio
    audio_bytes = prepare_audio_input("sample.wav")
    if not audio_bytes:
        print("Skipping text context exercise due to missing/invalid audio file.")
        return

    try:
        async with client.aio.live.connect(model=MODEL, config=config) as session:
            
            # --- Turn 1: Audio Input (Asking a question) ---
            print("\n[Turn 1] Sending audio input (e.g., 'What is the largest city in France?')...")
            await session.send_realtime_input(
                audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
            )
            await process_text_response(session, 1)

            # --- Turn 2: Text Input (Follow-up question using context) ---
            await asyncio.sleep(3) # Exercise 2 Step 1: Simulate user pause
            follow_up_prompt = "Based on that information, what is the capital of that city?"
            print(f"\n[Turn 2] Sending text input: '{follow_up_prompt}'")
            
            # Sending text input for the second turn (Exercise 2 Step 2)
            await session.send_realtime_input(text=follow_up_prompt)
            await process_text_response(session, 2)

    except Exception as e:
        print(f"\nAn error occurred during the text session: {e}")

# --- Exercise 4 Tool Definition ---

def get_current_datetime() -> str:
    """Returns the current UTC date and time in ISO format."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

GET_TIME_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_current_datetime",
            description="Returns the current UTC date and time.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={},
            ),
        )
    ]
)

# --- Exercise 3, 4, & 5: VAD, Tool Use, and Robustness ---

async def main_tool_call():
    """
    Exercise 3: VAD configuration.
    Exercise 4: Tool use and function calling.
    Exercise 5: Robust error handling and resource cleanup.
    """
    print("\n\n" + "="*60)
    print("Starting Exercise 3, 4, & 5: VAD, Tool Use, and Robustness...")
    print("="*60)
    
    # Exercise 3: VAD Configuration and Audio Output
    config = {
      "response_modalities": ["AUDIO"], # Return to audio output
      "system_instruction": "You are a helpful assistant and answer in a friendly tone. Use tools when necessary.",
      "vad_config": types.VoiceActivityDetectionConfig( # Exercise 3: VAD config
          speech_end_timeout_ms=1500,
          speech_start_threshold_ms=500,
      )
    }
    
    initial_prompt = "What is the time right now?" # Prompt to trigger tool (Exercise 4)
    output_filename = "tool_response_audio.wav"
    wf = None # Initialize file handle for cleanup (Exercise 5)

    try:
        # 1. Catching connection errors (Exercise 5)
        async with client.aio.live.connect(
            model=MODEL, 
            config=config, 
            tools=[GET_TIME_TOOL] # Exercise 4: Adding the tool
        ) as session:
            
            # Setup output file (Exercise 5)
            wf = wave.open(output_filename, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000) # Output is 24kHz

            print(f"Sending prompt to trigger tool: '{initial_prompt}'")
            # Send the text input (Exercise 4)
            await session.send_realtime_input(text=initial_prompt)

            # 2. Streaming loop with tool handling
            async for response in session.receive():
                
                # A. Handle Audio Data (Exercise 3/Original Goal)
                if response.data is not None:
                    wf.writeframes(response.data)
                
                # B. Handle Tool Calls (Exercise 4)
                if response.server_content and response.server_content.tool_calls:
                    tool_calls = response.server_content.tool_calls
                    print("\n[Tool Call Detected] Executing external function...")
                    
                    tool_responses = []
                    for call in tool_calls:
                        if call.function.name == "get_current_datetime":
                            # Execute the local Python function
                            result = get_current_datetime()
                            print(f"  -> Function executed. Result: {result}")
                            
                            # Prepare the tool response to send back to Gemini
                            tool_responses.append(
                                types.ToolResponse(
                                    function_response=types.FunctionResponse(
                                        name=call.function.name,
                                        response={"current_time": result},
                                    )
                                )
                            )
                    
                    # Send the tool result back to the session for Gemini to generate the final response
                    await session.send_realtime_input(tool_response=tool_responses)
                    
            print(f"\nSuccessfully saved final audio response (Tool result narrated) to {output_filename}")

    except asyncio.CancelledError:
        print("Operation was cancelled.")
    except Exception as e:
        print(f"A critical error occurred during streaming or connection: {e}")
    finally:
        # 3. Guaranteed resource cleanup (Exercise 5)
        if wf:
            wf.close()
            print("WAV file handle closed successfully.")


# --- Main Runner ---

if __name__ == "__main__":
    
    # --- Prerequisite Setup Check ---
    # Create a silent dummy file if 'sample.wav' is missing, 
    # allowing the script structure to be tested even without real audio.
    if not Path("sample.wav").exists():
        print("WARNING: 'sample.wav' not found. Creating a silent dummy file (1 sec) for structural testing.")
        # Create a 1-second silent 16kHz WAV file (16000 frames * 2 bytes/frame = 32000 bytes)
        try:
            with wave.open("sample.wav", "wb") as wf_dummy:
                wf_dummy.setnchannels(1)
                wf_dummy.setsampwidth(2)
                wf_dummy.setframerate(16000)
                wf_dummy.writeframes(b'\x00' * 32000)
            print("Dummy 'sample.wav' created.")
        except Exception as e:
            print(f"Could not create dummy WAV file: {e}")


    # Run Exercise 1 and 2 (Text Context)
    asyncio.run(main_text_context())
    
    # Run Exercise 3, 4, and 5 (Audio Output, VAD, Tool Use, Robustness)
    asyncio.run(main_tool_call())

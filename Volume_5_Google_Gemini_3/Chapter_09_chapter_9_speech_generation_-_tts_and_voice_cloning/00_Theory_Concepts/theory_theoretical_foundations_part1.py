
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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
from google.genai import types
import wave
import os

# --- 1. Utility Function to Handle Raw PCM Data ---
# The TTS model returns raw PCM (Pulse Code Modulation) data.
# This function wraps that data in a WAV file header so it can be played.
def save_wave_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
   """
   Saves raw PCM audio data into a playable WAV file format.
   
   Args:
      filename (str): The name of the output WAV file.
      pcm_data (bytes): The raw audio data returned by the Gemini API.
      channels (int): Number of audio channels (1 for mono).
      rate (int): Sample rate in Hz (24000 is standard for Gemini TTS).
      sample_width (int): Sample size in bytes (2 for 16-bit audio).
   """
   try:
      with wave.open(filename, "wb") as wf:
         wf.setnchannels(channels)
         wf.setsampwidth(sample_width)
         wf.setframerate(rate)
         wf.writeframes(pcm_data)
      print(f"Successfully saved audio to {filename}")
   except Exception as e:
      print(f"Error saving WAV file: {e}")

# Initialize the Gemini Client
# Ensure the GEMINI_API_KEY environment variable is set
try:
    client = genai.Client()
except Exception as e:
    print(f"Client initialization failed. Ensure API key is configured. Error: {e}")
    exit()

# --- 2. Single-Speaker TTS Generation Example ---
def generate_single_speaker_audio(text_prompt, output_file, voice_name='Kore'):
    """Generates single-speaker audio with prompt control."""
    print(f"\n--- Generating Single Speaker Audio: {output_file} ---")
    
    # Use natural language to control style and tone
    contents = f"Say in a gentle, informative tone: \"{text_prompt}\""
    
    try:
        response = client.models.generate_content(
           model="gemini-2.5-flash-preview-tts", # Specialized TTS model
           contents=contents,
           config=types.GenerateContentConfig(
              response_modalities=["AUDIO"], # CRITICAL: Request audio output
              speech_config=types.SpeechConfig(
                 voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                       voice_name=voice_name, # e.g., 'Kore' (Firm) or 'Puck' (Upbeat)
                    )
                 )
              ),
           )
        )

        # Extract the raw PCM data from the response
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        
        # Save the raw data as a playable WAV file
        save_wave_file(output_file, audio_data)

    except Exception as e:
        print(f"Single-speaker generation failed: {e}")

# --- 3. Multi-Speaker TTS Generation Example (Dialogue) ---
def generate_multi_speaker_audio(output_file):
    """Generates multi-speaker dialogue, assigning voices by name."""
    print(f"\n--- Generating Multi-Speaker Audio: {output_file} ---")
    
    # Prompt must clearly define speakers using the names configured below
    prompt = """TTS the following conversation between the scientist, Dr. Anya, and the field assistant, Liam:
             Dr. Anya: Liam, did you confirm the temperature reading of the thermal vent?
             Liam: Yes, Doctor. It's stable, but I detected a faint, rhythmic clicking sound near the perimeter.
             Dr. Anya: Interesting. Investigate that clicking sound immediately, and report your findings with excitement."""
             
    try:
        response = client.models.generate_content(
           model="gemini-2.5-flash-preview-tts",
           contents=prompt,
           config=types.GenerateContentConfig(
              response_modalities=["AUDIO"],
              speech_config=types.SpeechConfig(
                 multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                       types.SpeakerVoiceConfig(
                          speaker='Dr. Anya', # Speaker name must match prompt
                          voice_config=types.VoiceConfig(
                             prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Charon', # Informative voice for the scientist
                             )
                          )
                       ),
                       types.SpeakerVoiceConfig(
                          speaker='Liam', # Speaker name must match prompt
                          voice_config=types.VoiceConfig(
                             prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Fenrir', # Excitable voice for the assistant
                             )
                          )
                       ),
                    ]
                 )
              )
           )
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        save_wave_file(output_file, audio_data)

    except Exception as e:
        print(f"Multi-speaker generation failed: {e}")

# --- 4. Advanced Workflow: LLM Chaining Example (RAG Analogy) ---
def generate_podcast_segment(output_file):
    """
    Generates a text transcript using a standard LLM, then converts it to 
    multi-speaker audio using the TTS model (analogous to RAG chaining).
    """
    print(f"\n--- Generating Chained Podcast Segment: {output_file} ---")

    # Step 1: Generate the transcript using a standard LLM
    print("Step 1: Generating transcript using gemini-2.0-flash...")
    transcript_prompt = """Generate a short, 80-word transcript for a history podcast titled 'The Bronze Age Collapse'. The hosts are Dr. Alara and Professor Ben. The dialogue should discuss the Sea Peoples."""
    
    transcript_response = client.models.generate_content(
       model="gemini-2.0-flash",
       contents=transcript_prompt
    )
    transcript = transcript_response.text
    print(f"Generated Transcript:\n{transcript.strip()}")
    
    # Step 2: Pass the generated transcript to the TTS model
    print("\nStep 2: Converting transcript to multi-speaker audio...")
    
    try:
        response = client.models.generate_content(
           model="gemini-2.5-flash-preview-tts",
           contents=transcript,
           config=types.GenerateContentConfig(
              response_modalities=["AUDIO"],
              speech_config=types.SpeechConfig(
                 multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                       types.SpeakerVoiceConfig(
                          speaker='Dr. Alara',
                          voice_config=types.VoiceConfig(
                             prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Sadaltager', # Knowledgeable voice
                             )
                          )
                       ),
                       types.SpeakerVoiceConfig(
                          speaker='Professor Ben',
                          voice_config=types.VoiceConfig(
                             prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Rasalgethi', # Informative voice
                             )
                          )
                       ),
                    ]
                 )
              )
           )
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        save_wave_file(output_file, audio_data)

    except Exception as e:
        print(f"Chained generation failed: {e}")


if __name__ == "__main__":
    # Execute the examples
    generate_single_speaker_audio(
        text_prompt="The quantum entanglement observation confirmed the theory.",
        output_file="single_speaker_report.wav",
        voice_name='Charon' # Informative
    )
    
    generate_multi_speaker_audio(
        output_file="two_speaker_dialogue.wav"
    )
    
    generate_podcast_segment(
        output_file="chained_podcast_segment.wav"
    )

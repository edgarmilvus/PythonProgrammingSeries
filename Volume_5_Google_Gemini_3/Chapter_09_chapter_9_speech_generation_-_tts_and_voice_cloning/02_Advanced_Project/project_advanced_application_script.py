
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

import os
import wave
from google import genai
from google.genai import types
from typing import Optional, Dict, List

# Ensure your GEMINI_API_KEY is set as an environment variable
if 'GEMINI_API_KEY' not in os.environ:
    raise ValueError("GEMINI_API_KEY environment variable not found. Please set it.")

# --- 1. CORE UTILITY FUNCTION (PCM to WAV Conversion) ---

def save_pcm_to_wav(filename: str, pcm_data: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> None:
    """
    Saves raw Pulse Code Modulation (PCM) audio data received from the Gemini API
    into a standard Waveform Audio File Format (.wav).

    The Gemini TTS model outputs raw PCM data (signed 16-bit, mono, 24kHz), 
    which requires the WAV header structure to be playable by standard media players.
    """
    try:
        with wave.open(filename, "wb") as wf:
            # Set audio parameters for the WAV file header
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            
            # Write the raw PCM data frames
            wf.writeframes(pcm_data)
        print(f"\n[SUCCESS] Audio saved successfully to: {filename}")
    except Exception as e:
        print(f"[ERROR] Could not save WAV file: {e}")


# --- 2. CONFIGURATION MAPPING ---

# Defined voices and their characteristics based on documentation
VOICE_MAP: Dict[str, str] = {
    "Host": "Leda",     # Youthful, good for curious host
    "Expert": "Charon"  # Informative, good for technical expert
}

# --- 3. DYNAMIC AI PODCAST GENERATOR CLASS ---

class DynamicAIPodcastGenerator:
    """
    A class to manage the two-step process of generating a structured podcast 
    transcript using a standard LLM and then converting it to multi-speaker 
    audio using the specialized Gemini TTS model.
    """
    
    # Models used in the pipeline
    TRANSCRIPT_MODEL = "gemini-2.0-flash" 
    TTS_MODEL = "gemini-2.5-flash-preview-tts"

    def __init__(self, topic: str, output_filename: str):
        """Initializes the client and sets up the generation parameters."""
        self.client = genai.Client()
        self.topic = topic
        self.output_filename = output_filename
        print(f"Initializing DAPG for topic: '{self.topic}'")

    def _generate_transcript(self) -> Optional[str]:
        """
        Step 1: Uses a general LLM (Gemini 2.0 Flash) to create a structured 
        transcript, including speaker names and style cues.
        """
        print("\n--- Step 1: Generating Structured Transcript (LLM Chaining) ---")
        
        # The prompt guides the LLM to structure the output for the TTS model
        prompt = f"""
        Generate a short, 150-word podcast segment about the concept of '{self.topic}'.
        The segment must be a conversation between two speakers: 'Host' and 'Expert'.
        
        The Host should sound curious and lead the conversation.
        The Expert should sound authoritative and deliver detailed information.
        
        Format the output strictly using the speaker names followed by a colon, 
        ensuring the tone guidance is incorporated into the dialogue structure.
        
        Example structure:
        Host: Say curiously: What exactly is RAG?
        Expert: Explain authoritatively: RAG stands for Retrieval-Augmented Generation...
        """
        
        try:
            # Generate the text content using the fast LLM
            response = self.client.models.generate_content(
                model=self.TRANSCRIPT_MODEL,
                contents=prompt
            )
            transcript = response.text
            print(f"Transcript Generated:\n{'-'*30}\n{transcript}\n{'-'*30}")
            return transcript
        except Exception as e:
            print(f"[ERROR] Transcript generation failed: {e}")
            return None

    def _generate_audio(self, transcript: str) -> Optional[bytes]:
        """
        Step 2: Uses the specialized TTS model to convert the structured 
        transcript into multi-speaker audio.
        """
        print("\n--- Step 2: Generating Multi-Speaker Audio (TTS Model) ---")

        # Define the configuration for each speaker using the VOICE_MAP
        speaker_configs: List[types.SpeakerVoiceConfig] = [
            types.SpeakerVoiceConfig(
                speaker='Host',
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=VOICE_MAP["Host"],
                    )
                )
            ),
            types.SpeakerVoiceConfig(
                speaker='Expert',
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=VOICE_MAP["Expert"],
                    )
                )
            ),
        ]

        try:
            # Call the TTS model with the transcript and detailed audio config
            response = self.client.models.generate_content(
                model=self.TTS_MODEL,
                contents=transcript,
                config=types.GenerateContentConfig(
                    # CRITICAL: Request the output modality as AUDIO
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        # CRITICAL: Use multi_speaker_voice_config for dialogue
                        multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                            speaker_voice_configs=speaker_configs
                        )
                    ),
                )
            )

            # Retrieve the raw audio data (Base64 decoded bytes)
            # This data is raw PCM and needs to be wrapped in a WAV file
            raw_audio_data = response.candidates[0].content.parts[0].inline_data.data
            print(f"Raw audio data received. Size: {len(raw_audio_data)} bytes.")
            return raw_audio_data

        except Exception as e:
            print(f"[ERROR] Audio generation failed. Ensure model '{self.TTS_MODEL}' is supported and accessible.")
            print(f"Details: {e}")
            return None

    def run(self):
        """Executes the full pipeline."""
        transcript = self._generate_transcript()
        
        if transcript:
            raw_audio = self._generate_audio(transcript)
            
            if raw_audio:
                # Save the raw PCM data to a playable WAV file
                save_pcm_to_wav(self.output_filename, raw_audio)
            else:
                print("[FAILURE] Cannot save audio because raw data was not generated.")
        else:
            print("[FAILURE] Cannot generate audio without a successful transcript.")


# --- 4. EXECUTION BLOCK ---

if __name__ == "__main__":
    # Define the core parameters for the podcast segment
    PODCAST_TOPIC = "Retrieval-Augmented Generation (RAG)"
    OUTPUT_FILE = "rag_podcast_segment.wav"
    
    # Instantiate and run the generator
    generator = DynamicAIPodcastGenerator(
        topic=PODCAST_TOPIC,
        output_filename=OUTPUT_FILE
    )
    
    generator.run()


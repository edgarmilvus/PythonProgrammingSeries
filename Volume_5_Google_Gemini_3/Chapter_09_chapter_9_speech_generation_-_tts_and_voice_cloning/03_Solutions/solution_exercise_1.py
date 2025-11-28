
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

import os
import wave
from google import genai
from google.genai import types

# --- Configuration and Utility Functions ---

# Ensure the API key is available
# Note: For production use, ensure GEMINI_API_KEY is set in your environment.
if 'GEMINI_API_KEY' not in os.environ:
    # This is a placeholder check; in a real environment, this would halt execution.
    print("Warning: GEMINI_API_KEY environment variable not found. Client initialization may fail.")

try:
    # Initialize the Gemini Client
    client = genai.Client()
    TTS_MODEL = "gemini-2.5-flash-preview-tts"
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the google-genai library is installed and GEMINI_API_KEY is set.")
    exit()

# Define the utility function to save raw PCM data to a WAV file
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   """
   Takes raw PCM audio data (Pulse-Code Modulation) from the API response
   and wraps it in a standard WAV file container for playback.
   
   Args:
       filename (str): The name of the output .wav file.
       pcm (bytes): The raw audio data received from the Gemini API.
       channels (int): Number of audio channels (1 for mono).
       rate (int): Sample rate (Hz). Gemini TTS defaults to 24000 Hz.
       sample_width (int): Sample width in bytes (2 for 16-bit audio).
   """
   print(f"-> Saving audio output to: {filename}")
   try:
       with wave.open(filename, "wb") as wf:
          wf.setnchannels(channels)
          wf.setsampwidth(sample_width)
          wf.setframerate(rate)
          wf.writeframes(pcm)
   except Exception as e:
       print(f"Error saving wave file {filename}: {e}")
       
# Helper function to extract and save audio data from a response object
def process_and_save_audio(response, filename):
    """Extracts binary audio data from the Gemini response and saves it."""
    try:
        # The audio data is base64 encoded within the inline_data.data field
        data = response.candidates[0].content.parts[0].inline_data.data
        wave_file(filename, data)
        print(f"Successfully generated {filename}")
    except (AttributeError, IndexError, TypeError) as e:
        print(f"Error processing response for {filename}. API may have returned an error or the structure is unexpected.")
        # Attempt to print error message if available
        if response.candidates[0].finish_reason.name == 'SAFETY':
             print("Generation blocked due to safety settings.")
        elif response.candidates[0].finish_reason.name == 'RECITATION':
             print("Generation blocked due to recitation policy.")
        else:
             print(f"Error details: {e}")
             print(f"Raw response: {response}")


# --- Exercise 1: Single-Speaker Synthesis and Style Adherence ---

def exercise_1_single_speaker():
    print("\n--- Running Exercise 1: Single-Speaker Synthesis (Charon) ---")
    
    prompt = "Read this formal announcement in a clear, informative tone: 'Attention all personnel. The quarterly financial review meeting has been rescheduled to 10:00 AM in Conference Room Alpha. Please ensure all necessary documentation is prepared by that time.'"
    voice_name = 'Charon' # Informative voice

    response = client.models.generate_content(
       model=TTS_MODEL,
       contents=prompt,
       config=types.GenerateContentConfig(
          # CRITICAL: Specify that the desired output modality is AUDIO
          response_modalities=["AUDIO"],
          speech_config=types.SpeechConfig(
             voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                   voice_name=voice_name,
                )
             )
          ),
       )
    )
    process_and_save_audio(response, 'exercise_1_announcement.wav')

# --- Exercise 2: Emotion and Controllable TTS Prompting ---

def exercise_2_controlled_tts():
    print("\n--- Running Exercise 2: Emotion and Controllable TTS Prompting (Enceladus) ---")
    
    # The prompt explicitly instructs the model on tone and emphasis
    prompt = """Speak this line with a dramatic, fearful urgency, emphasizing the word 'suddenly':
             "The lights flickered once, then twice, and suddenly, the door slammed shut behind them."
             """
    voice_name = 'Enceladus' # Breathy voice, suitable for dramatic or soft tones

    response = client.models.generate_content(
       model=TTS_MODEL,
       contents=prompt,
       config=types.GenerateContentConfig(
          response_modalities=["AUDIO"],
          speech_config=types.SpeechConfig(
             voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                   voice_name=voice_name,
                )
             )
          ),
       )
    )
    process_and_save_audio(response, 'exercise_2_fearful_delivery.wav')

# --- Exercise 3: The Multi-Speaker Panel Discussion (3 Speakers) ---

def exercise_3_multi_speaker_challenge():
    print("\n--- Running Exercise 3: Multi-Speaker Panel Discussion (3 Speakers) ---")
    
    # CRITICAL: The prompt must clearly label each speaker using the exact names
    # defined in the MultiSpeakerVoiceConfig.
    prompt = """TTS the following panel discussion between Dr. Aris, Maya, and Ben:
             Dr. Aris: Our latest data confirms the existence of the gravitational anomaly. It's unprecedented.
             Maya: Dr. Aris, with all due respect, the public is skeptical. What tangible evidence can you provide?
             Ben: Wait, Dr. Aris! I just cross-referenced the sensor readings. The anomaly is stabilizing!
             """

    response = client.models.generate_content(
       model=TTS_MODEL,
       contents=prompt,
       config=types.GenerateContentConfig(
          response_modalities=["AUDIO"],
          speech_config=types.SpeechConfig(
             multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                   # Speaker 1: Dr. Aris (Gacrux - Mature)
                   types.SpeakerVoiceConfig(
                      speaker='Dr. Aris',
                      voice_config=types.VoiceConfig(
                         prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Gacrux',
                         )
                      )
                   ),
                   # Speaker 2: Maya (Puck - Upbeat)
                   types.SpeakerVoiceConfig(
                      speaker='Maya',
                      voice_config=types.VoiceConfig(
                         prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Puck',
                         )
                      )
                   ),
                   # Speaker 3: Ben (Leda - Youthful)
                   types.SpeakerVoiceConfig(
                      speaker='Ben',
                      voice_config=types.VoiceConfig(
                         prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Leda',
                         )
                      )
                   ),
                ]
             )
          )
       )
    )
    process_and_save_audio(response, 'exercise_3_three_way_dialogue.wav')

# --- Exercise 4: LLM-Chained Audio Generation (Automated Audiobook) ---

def exercise_4_llm_chained_tts():
    print("\n--- Running Exercise 4: LLM-Chained Audio Generation ---")
    
    # Step 1: Use a general LLM (Gemini 2.0 Flash) to generate the narrative text.
    print("Step 1: Generating narrative transcript using gemini-2.0-flash...")
    transcript_prompt = """Generate a 150-word descriptive passage suitable for an audiobook chapter. The passage should describe the discovery of a lost, hidden jungle temple, focusing on the atmosphere and the sound of the jungle."""
    
    transcript_response = client.models.generate_content(
       model="gemini-2.0-flash",
       contents=transcript_prompt
    )
    transcript = transcript_response.text
    print("--- Generated Transcript ---")
    print(transcript)
    print("--------------------------")

    # Step 2: Pass the generated transcript to the TTS model for audio synthesis.
    print("\nStep 2: Converting transcript to audio using gemini-2.5-flash-preview-tts...")
    voice_name = 'Sadaltager' # Knowledgeable voice for narration

    tts_response = client.models.generate_content(
       model=TTS_MODEL,
       contents=transcript,
       config=types.GenerateContentConfig(
          response_modalities=["AUDIO"],
          speech_config=types.SpeechConfig(
             voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                   voice_name=voice_name,
                )
             )
          ),
       )
    )
    process_and_save_audio(tts_response, 'exercise_4_automated_chapter.wav')

# --- Exercise 5: Multilingual Synthesis (French) ---

def exercise_5_multilingual_tts():
    print("\n--- Running Exercise 5: Multilingual Synthesis (French) ---")
    
    # French text: "Bonjour, le soleil brille aujourd'hui. Nous explorons les capacités de synthèse vocale de Gemini en français."
    prompt = "Bonjour, le soleil brille aujourd'hui. Nous explorons les capacités de synthèse vocale de Gemini en français."
    voice_name = 'Autonoe' # Bright voice

    response = client.models.generate_content(
       model=TTS_MODEL,
       contents=prompt,
       config=types.GenerateContentConfig(
          response_modalities=["AUDIO"],
          speech_config=types.SpeechConfig(
             voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                   voice_name=voice_name,
                )
             )
          ),
       )
    )
    process_and_save_audio(response, 'exercise_5_french_tts.wav')


if __name__ == "__main__":
    if 'GEMINI_API_KEY' in os.environ:
        exercise_1_single_speaker()
        exercise_2_controlled_tts()
        exercise_3_multi_speaker_challenge()
        exercise_4_llm_chained_tts()
        exercise_5_multilingual_tts()
        print("\nAll TTS exercises complete. Check your current directory for WAV files.")
    else:
        print("\nExecution skipped: Please set the GEMINI_API_KEY environment variable to run the exercises.")

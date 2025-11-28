
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
import json
import time
import requests
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- Configuration and Setup ---

# Define the model to use. Flash is fast and capable for transcription/summary.
MODEL_ID = "gemini-2.5-flash"
# Placeholder for a large audio file download (e.g., a 60-minute podcast)
# NOTE: Replace this URL with a link to a publicly accessible MP3 file for testing.
SAMPLE_AUDIO_URL = "https://storage.googleapis.com/generativeai-downloads/data/State_of_the_Union_Address_30_January_1961.mp3"
LOCAL_AUDIO_PATH = "podcast_episode.mp3"
MIME_TYPE = "audio/mp3"

class PodcastInsightExtractor:
    """
    A robust class designed to manage the lifecycle of a large audio file
    for analysis using the Gemini API, including upload, token counting,
    segmented analysis, structured reporting, and cleanup.
    """
    def __init__(self):
        """Initializes the Gemini client and checks for API key."""
        try:
            # The client automatically picks up the GEMINI_API_KEY environment variable.
            self.client = genai.Client()
            print("Gemini Client initialized successfully.")
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            print("Please ensure your GEMINI_API_KEY is set correctly.")
            raise

        self.uploaded_file = None # Stores the File object returned by client.files.upload

    def download_sample_audio(self):
        """Simulates downloading a large podcast file."""
        print(f"Downloading sample audio from: {SAMPLE_AUDIO_URL}...")
        try:
            response = requests.get(SAMPLE_AUDIO_URL, stream=True)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            with open(LOCAL_AUDIO_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Download complete. File saved to {LOCAL_AUDIO_PATH}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error during download: {e}")
            print("Skipping download. Please ensure a file named 'podcast_episode.mp3' exists.")
            return False

    def upload_podcast(self):
        """
        Uploads the local audio file to the Gemini Files API.
        This is mandatory for files larger than 20 MB.
        """
        if not os.path.exists(LOCAL_AUDIO_PATH):
            print(f"Error: Local audio file not found at {LOCAL_AUDIO_PATH}.")
            return

        print(f"Uploading {LOCAL_AUDIO_PATH} to Gemini Files API...")
        try:
            # client.files.upload handles the file streaming and API interaction
            self.uploaded_file = self.client.files.upload(
                file=LOCAL_AUDIO_PATH,
                mime_type=MIME_TYPE
            )
            print(f"File uploaded successfully. URI: {self.uploaded_file.uri}")
            print(f"File Name (ID): {self.uploaded_file.name}")
        except APIError as e:
            print(f"Gemini API Error during upload: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during upload: {e}")

    def count_audio_tokens(self):
        """
        Calculates the token cost of the uploaded audio file.
        Gemini charges based on token usage, making this a critical step.
        """
        if not self.uploaded_file:
            print("Cannot count tokens: File not uploaded.")
            return

        try:
            response = self.client.models.count_tokens(
                model=MODEL_ID,
                contents=[self.uploaded_file]
            )
            print(f"\n--- Token Analysis ---")
            print(f"Total Audio Tokens: {response.total_tokens}")
            # Note: 1 minute (60s) = 1920 tokens (32 tokens/second)
            print(f"Estimated Audio Length (approx): {response.total_tokens / 32 / 60:.2f} minutes")
        except APIError as e:
            print(f"Error counting tokens: {e}")

    def analyze_segment(self, start_time: str, end_time: str, specific_query: str):
        """
        Analyzes a specific segment of the audio using MM:SS timestamps.

        :param start_time: Start timestamp (MM:SS).
        :param end_time: End timestamp (MM:SS).
        :param specific_query: The specific question or task for the segment.
        """
        if not self.uploaded_file:
            print("Cannot analyze segment: File not uploaded.")
            return None

        prompt = (
            f"Analyze the audio content between the timestamps {start_time} and {end_time}. "
            f"Specifically: {specific_query}"
        )

        print(f"\n--- Segment Analysis ({start_time} to {end_time}) ---")
        print(f"Query: {specific_query}")

        try:
            response = self.client.models.generate_content(
                model=MODEL_ID,
                contents=[prompt, self.uploaded_file]
            )
            print("Result:")
            print(response.text)
            return response.text
        except APIError as e:
            print(f"Error analyzing segment: {e}")
            return None

    def generate_structured_report(self):
        """
        Generates a comprehensive, structured report (JSON format) for the entire podcast.
        Uses system instructions to enforce output quality and focus on key concepts
        like diarization and noise handling.
        """
        if not self.uploaded_file:
            print("Cannot generate report: File not uploaded.")
            return None

        # Define the desired output structure using a JSON schema
        schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "podcast_title": types.Schema(type=types.Type.STRING, description="Inferred title of the podcast."),
                "main_speakers": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="List of primary speakers identified (Speaker A, Speaker B, etc.)."),
                "noise_assessment": types.Schema(type=types.Type.STRING, description="Brief assessment of audio quality and background noise (e.g., 'Clear, minimal noise' or 'High background hum')."),
                "key_takeaways": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="The three most important conclusions from the entire episode."),
                "topic_breakdown": types.Schema(type=types.Type.ARRAY, items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "topic": types.Schema(type=types.Type.STRING),
                        "start_time": types.Schema(type=types.Type.STRING, description="MM:SS"),
                        "summary": types.Schema(type=types.Type.STRING)
                    }
                ))
            },
            required=["podcast_title", "main_speakers", "noise_assessment", "key_takeaways", "topic_breakdown"]
        )

        # System instruction to guide the model's behavior
        system_instruction = (
            "You are an expert podcast analyst. Your task is to process the full audio file "
            "and generate a comprehensive JSON report. Focus on identifying and separating "
            "the main speakers (diarization) and noting any significant background noise. "
            "Structure the output strictly according to the provided JSON schema."
        )

        prompt = "Generate the full structured analysis report for this podcast episode."

        print("\n--- Generating Structured JSON Report (Diarization & Summary) ---")
        try:
            response = self.client.models.generate_content(
                model=MODEL_ID,
                contents=[prompt, self.uploaded_file],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=schema
                )
            )

            # Attempt to parse the JSON response
            report_data = json.loads(response.text)
            print("Structured Report Generated Successfully:")
            print(json.dumps(report_data, indent=2))
            return report_data

        except APIError as e:
            print(f"Error generating structured report: {e}")
        except json.JSONDecodeError:
            print("Error: Failed to decode the model's response as valid JSON.")
            print(f"Raw response text: {response.text}")
        return None

    def cleanup(self):
        """
        Deletes the file from the Gemini server.
        Crucial for managing storage and maintaining privacy/security.
        """
        if self.uploaded_file:
            print(f"\n--- Cleaning Up ---")
            print(f"Deleting uploaded file: {self.uploaded_file.name}...")
            try:
                self.client.files.delete(name=self.uploaded_file.name)
                print("File deleted successfully from the server.")
            except APIError as e:
                print(f"Warning: Failed to delete file {self.uploaded_file.name}. Error: {e}")

    def run_analysis(self):
        """Orchestrates the entire analysis workflow."""
        if self.download_sample_audio():
            try:
                self.upload_podcast()
                if self.uploaded_file:
                    self.count_audio_tokens()

                    # 1. Segmented Analysis: Focus on a specific 5-minute window
                    self.analyze_segment(
                        start_time="01:00",
                        end_time="06:00",
                        specific_query="Identify the main argument presented in this segment and list any technical terms mentioned."
                    )

                    # 2. Comprehensive Structured Report (Diarization and Noise Assessment)
                    self.generate_structured_report()

            finally:
                # Ensure cleanup happens even if an error occurs during analysis
                self.cleanup()
                # Clean up the local file as well
                if os.path.exists(LOCAL_AUDIO_PATH):
                    os.remove(LOCAL_AUDIO_PATH)
                    print(f"Local file {LOCAL_AUDIO_PATH} removed.")


# --- Main Execution Block ---

if __name__ == "__main__":
    print("Starting Podcast Insight Extraction Application.")
    analyzer = PodcastInsightExtractor()
    analyzer.run_analysis()


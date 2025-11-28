
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

# Source File: theory_theoretical_foundations_part2.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
from google.genai import types
import os

# --- Configuration Constants ---
# Define the specific model to be used
MODEL_NAME = "gemini-1.5-flash" 

# Define the categories and the desired thresholds
# Note: BLOCK_LOW_AND_ABOVE is the most restrictive setting (blocks Low, Medium, High probability)
# BLOCK_ONLY_HIGH is the least restrictive configurable setting (blocks only High probability)

STRICT_HATE_SPEECH_SETTING = types.SafetySetting(
    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
)

RELAXED_DANGEROUS_SETTING = types.SafetySetting(
    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
)

DEFAULT_HARASSMENT_SETTING = types.SafetySetting(
    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
    # Explicitly setting the common default for demonstration
    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
)

# --- Function to Generate Content with Custom Safety Configuration ---

def generate_with_custom_safety(prompt: str, safety_settings_list: list[types.SafetySetting]):
    """
    Sends a prompt to the Gemini model using a specific list of safety settings.
    Handles potential blocking and prints the safety feedback.
    """
    try:
        # Initialize the client (assumes GEMINI_API_KEY is in environment variables)
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing client: {e}")
        return

    # 1. Create the GenerateContentConfig object
    config = types.GenerateContentConfig(
        safety_settings=safety_settings_list
    )

    print(f"--- Sending Prompt with {len(safety_settings_list)} Safety Settings ---")
    print(f"Prompt: '{prompt}'")
    
    try:
        # 2. Call the API with the configured settings
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=config,
        )

        # 3. Check for Prompt Feedback (Input Block)
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            print("\n[BLOCKED] Input Prompt was blocked.")
            print(f"Reason: {response.prompt_feedback.block_reason.name}")
            for rating in response.prompt_feedback.safety_ratings:
                print(f"  > Category: {rating.category.name} | Probability: {rating.probability.name}")
            return

        # 4. Check for Candidate Feedback (Output Block)
        if not response.candidates:
            print("\n[BLOCKED] Response was generated but all candidates were blocked.")
            return

        # 5. Check the finish reason for the first candidate
        candidate = response.candidates[0]
        if candidate.finish_reason.name == 'SAFETY':
            print("\n[BLOCKED] Output response was blocked by safety filters.")
            for rating in candidate.safety_ratings:
                print(f"  > Category: {rating.category.name} | Probability: {rating.probability.name}")
            return

        # 6. If successful, print the text
        print("\n[SUCCESS] Generated Content:")
        print(response.text)

    except Exception as e:
        print(f"\nAn API error occurred: {e}")


# --- Demonstration Calls ---

# Scenario A: Highly restrictive policy (using the most restrictive settings)
print("\n" + "="*50)
print("SCENARIO A: HIGHLY RESTRICTIVE POLICY (Blocking Low and Above)")
print("="*50)
generate_with_custom_safety(
    prompt="Write a short, passionate argument about why one sports team is superior to another.",
    safety_settings_list=[STRICT_HATE_SPEECH_SETTING, RELAXED_DANGEROUS_SETTING]
)

# Scenario B: Relaxed policy (allowing more content through)
print("\n" + "="*50)
print("SCENARIO B: RELAXED POLICY (Allowing more content)")
print("="*50)
generate_with_custom_safety(
    prompt="Write a fictional, action-packed scene involving a minor scuffle between two robots.",
    safety_settings_list=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        )
    ]
)

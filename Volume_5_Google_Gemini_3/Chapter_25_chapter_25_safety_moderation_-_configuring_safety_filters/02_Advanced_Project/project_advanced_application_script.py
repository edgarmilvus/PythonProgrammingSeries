
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
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import List

# --- 1. CONFIGURATION CONSTANTS ---

# Define the model to use
MODEL_NAME = "gemini-2.5-flash"

# Define a set of prompts to test the moderation thresholds
TEST_PROMPTS = {
    "Neutral Query": "Explain the concept of quantum entanglement in simple terms.",
    "Mildly Dangerous Dialogue": "The knight yelled, 'I will strike down the dragon and tear its heart from its chest!' Write the next line of dialogue.",
    "Hate Speech Attempt": "Write a short, rude phrase criticizing people who enjoy the color purple.",
}

# --- 2. CONFIGURATION FACTORY FUNCTIONS ---

def create_safety_config(category: types.HarmCategory, threshold: types.HarmBlockThreshold) -> types.SafetySetting:
    """
    Helper function to create a single SafetySetting object.
    """
    return types.SafetySetting(
        category=category,
        threshold=threshold,
    )

def get_strict_baseline_config() -> List[types.SafetySetting]:
    """
    Configuration 1: Strict Baseline.
    Blocks content with Medium or higher probability of harm.
    This simulates the default behavior for most use cases (BLOCK_MEDIUM_AND_ABOVE).
    """
    print("\n--- Applying Configuration: Strict Baseline (Medium/High block) ---")
    return [
        create_safety_config(types.HarmCategory.HARM_CATEGORY_HARASSMENT, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    ]

def get_relaxed_rpg_config() -> List[types.SafetySetting]:
    """
    Configuration 2: Relaxed RPG Dialogue.
    Relaxes Dangerous Content to BLOCK_ONLY_HIGH (Block few) to allow fantasy violence.
    Keeps Hate Speech and Harassment strict (BLOCK_MEDIUM_AND_ABOVE).
    """
    print("\n--- Applying Configuration: Relaxed RPG Dialogue (Dangerous Content relaxed) ---")
    return [
        # Allow more dangerous content for narrative realism
        create_safety_config(types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, types.HarmBlockThreshold.BLOCK_ONLY_HIGH),
        # Keep sensitive categories strict
        create_safety_config(types.HarmCategory.HARM_CATEGORY_HARASSMENT, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    ]

def get_hyper_vigilant_config() -> List[types.SafetySetting]:
    """
    Configuration 3: Hyper-Vigilant Monitoring.
    Blocks content with Low, Medium, or High probability of harm (BLOCK_LOW_AND_ABOVE).
    This is useful for highly sensitive environments or specific data filtering tasks.
    """
    print("\n--- Applying Configuration: Hyper-Vigilant (Block Low and Above) ---")
    return [
        create_safety_config(types.HarmCategory.HARM_CATEGORY_HARASSMENT, types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
        create_safety_config(types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
    ]

# --- 3. CORE GENERATION AND FEEDBACK FUNCTION ---

def generate_with_settings(client: genai.Client, prompt: str, settings: List[types.SafetySetting]):
    """
    Sends the prompt to the Gemini API with the specified safety settings and reports feedback.
    """
    print(f"\n[PROMPT]: {prompt[:60]}...")
    
    # Configure the generation request using the provided safety settings list
    config = types.GenerateContentConfig(safety_settings=settings)

    try:
        # Call the API with the custom configuration
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config,
        )

        # --- A. Check for Prompt Blocking ---
        # Prompt feedback indicates if the *input* itself was blocked before generation started.
        prompt_feedback = response.prompt_feedback
        if prompt_feedback and prompt_feedback.block_reason:
            print(f"STATUS: PROMPT BLOCKED! Reason: {prompt_feedback.block_reason.name}")
            if prompt_feedback.safety_ratings:
                print("DETAILS: Prompt Safety Ratings:")
                for rating in prompt_feedback.safety_ratings:
                    print(f"  - {rating.category.name}: Probability {rating.probability.name}")
            return

        # --- B. Check for Candidate (Response) Blocking ---
        # If the prompt passed, check the generated response (candidate).
        if not response.candidates:
            print("STATUS: RESPONSE BLOCKED! No candidates returned.")
            # If candidates are missing, we check the prompt feedback again (though usually empty here)
            return

        candidate = response.candidates[0]
        if candidate.finish_reason == types.FinishReason.SAFETY:
            print("STATUS: RESPONSE BLOCKED! Finish Reason: SAFETY.")
            print("DETAILS: Candidate Safety Ratings:")
            for rating in candidate.safety_ratings:
                # We only print categories that caused the block (usually HIGH or MEDIUM probability)
                if rating.probability != types.HarmProbability.NEGLIGIBLE:
                    print(f"  - {rating.category.name}: Probability {rating.probability.name} (Blocked)")
        else:
            # Content was successfully generated
            print("STATUS: SUCCESS.")
            print("RESPONSE:")
            # Use try/except for response.text as it sometimes fails if the structure is odd
            try:
                print(response.text.strip())
            except ValueError:
                print("[Response text unavailable due to internal filtering or structure error.]")
            
    except APIError as e:
        print(f"API Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- 4. MAIN EXECUTION BLOCK ---

def main():
    """
    Main function to initialize the client and run the tests.
    """
    try:
        # Initialize the client. Assumes GEMINI_API_KEY is set in environment variables.
        client = genai.Client()
    except Exception:
        print("ERROR: Failed to initialize Gemini client. Ensure the GEMINI_API_KEY environment variable is set correctly.")
        return

    # Define the list of configurations to test
    configs_to_test = [
        get_strict_baseline_config(),
        get_relaxed_rpg_config(),
        get_hyper_vigilant_config(),
    ]

    # Iterate through the test prompts and apply all configurations to each
    for prompt_name, prompt_text in TEST_PROMPTS.items():
        print(f"\n{'='*80}")
        print(f"TESTING PROMPT: {prompt_name}")
        print(f"{'='*80}")
        
        # Apply each configuration to the current prompt
        for settings in configs_to_test:
            generate_with_settings(client, prompt_text, settings)
            print("-" * 40)


if __name__ == "__main__":
    main()


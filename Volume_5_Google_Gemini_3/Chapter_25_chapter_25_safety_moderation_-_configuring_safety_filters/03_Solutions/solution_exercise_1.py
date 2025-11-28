
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
from google import genai
from google.genai import types

# --- Configuration and Setup ---

# Initialize the client. Assumes GEMINI_API_KEY is set in the environment.
try:
    client = genai.Client()
except Exception as e:
    # In a real environment, this should raise an error. For exercise purposes, we print the failure.
    print(f"Error initializing client. Ensure API key is set. Details: {e}")
    exit()

MODEL = "gemini-2.0-flash" # Recommended stable model for these exercises

# --- Exercise 1 Solution: Maximum Restriction and Feedback Analysis ---
print("--- Exercise 1: Implementing Maximum Restriction (HATE_SPEECH) ---")

def run_exercise_1():
    """
    Sets HATE_SPEECH to BLOCK_LOW_AND_ABOVE (maximum restriction) and tests a prompt,
    analyzing the prompt feedback structure.
    """
    # Prompt designed to be mildly derogatory towards a group (high likelihood of triggering HATE_SPEECH)
    test_prompt = "I think people who prefer that specific sports team are completely worthless and should stop watching."

    # 1. Define the safety setting: Block content with LOW, MEDIUM, or HIGH probability.
    safety_config = types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ]
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[test_prompt],
            config=safety_config,
        )

        # 2. Analyze the prompt feedback
        feedback = response.prompt_feedback
        print(f"Prompt Used: '{test_prompt}'")
        print(f"\nPrompt Feedback Object:\n{feedback}")

        if feedback.block_reason:
            print(f"\nSUCCESS: Input was blocked.")
            print(f"Block Reason: {feedback.block_reason.name}")
            # 3. Print safety ratings to confirm the category and probability
            for rating in feedback.safety_ratings:
                if rating.blocked:
                    print(f"  > BLOCKING CATEGORY: {rating.category.name}, Probability: {rating.probability.name}")
        else:
            print("FAILURE: Prompt was not blocked (expected a block).")

    except Exception as e:
        print(f"An error occurred during API call: {e}")

run_exercise_1()

# --- Exercise 2 Solution: Loosening Restrictions for Creative Contexts ---
print("\n--- Exercise 2: Loosening Restrictions (DANGEROUS_CONTENT) ---")

def run_exercise_2():
    """
    Sets DANGEROUS_CONTENT to BLOCK_ONLY_HIGH to allow medium/low risk content,
    demonstrating permissiveness for creative writing.
    """
    # Prompt designed to generate moderately dangerous/violent content (e.g., battle description)
    test_prompt = "Describe in vivid detail the final moments of the ancient war machine, 'The Iron Leviathan,' as it is struck by a colossal energy bolt, causing a massive, fiery explosion and shattering metal fragments."

    # 1. Configure DANGEROUS_CONTENT to BLOCK_ONLY_HIGH (least restrictive adjustable setting)
    safety_config = types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            ),
        ]
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[test_prompt],
            config=safety_config,
        )

        # 2. Check if content was generated successfully
        if response.text:
            print(f"SUCCESS: Content generated (Dangerous Content threshold was permissive).")
            # Print a snippet of the generated text
            print(f"Generated Text Snippet:\n'{response.text[:150]}...'")
        else:
            # If text is empty, check candidate finish reason
            finish_reason = response.candidates[0].finish_reason.name if response.candidates else "N/A"
            print(f"FAILURE: Content was blocked. Finish Reason: {finish_reason}")

    except Exception as e:
        print(f"An error occurred during API call: {e}")

run_exercise_2()


# --- Exercise 3 Solution: The Dual Filter Conflict and Candidate Blocking ---
print("\n--- Exercise 3: Dual Filter Conflict and Candidate Blocking ---")

def run_exercise_3():
    """
    Configures conflicting safety settings and analyzes the candidate output block.
    """
    # Prompt designed to generate content that triggers Harassment
    test_prompt = "Write a short, mean-spirited joke about a specific, generalized group of people."

    # 1. Configure dual safety settings
    safety_config = types.GenerateContentConfig(
        safety_settings=[
            # Strict Harassment filter: Blocks MEDIUM and above
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            ),
            # Lenient Sexually Explicit filter: Always show
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_NONE,
            ),
        ]
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[test_prompt],
            config=safety_config,
        )

        # 2. Check if response text is empty (expected block)
        if response.text:
            print("WARNING: Content was unexpectedly generated.")
            return

        # 3. Analyze candidate feedback
        if not response.candidates:
            print("Error: No candidates returned.")
            return

        candidate = response.candidates[0]
        finish_reason = candidate.finish_reason.name

        print(f"Response Text is empty, confirming output block.")
        print(f"Candidate Finish Reason: {finish_reason}")

        if finish_reason == "SAFETY":
            print("\nSUCCESS: Output was blocked due to SAFETY. Analyzing specific ratings:")
            
            # 4. Identify the blocking category
            for rating in candidate.safety_ratings:
                # The 'blocked' flag on the rating indicates the specific category that caused the stop
                if rating.blocked:
                    print(f"  > BLOCKING CATEGORY IDENTIFIED: {rating.category.name}")
                    print(f"    - Probability Level: {rating.probability.name}")
                else:
                    print(f"  > Allowed Category: {rating.category.name}, Probability: {rating.probability.name}")

    except Exception as e:
        print(f"An error occurred during API call: {e}")

run_exercise_3()


# --- Exercise 4 Solution: Challenge – Implementing the Safety Configuration Factory Pattern ---
print("\n--- Exercise 4: Safety Configuration Factory Pattern ---")

def create_safety_config(harassment_threshold: types.HarmBlockThreshold, dangerous_threshold: types.HarmBlockThreshold) -> types.GenerateContentConfig:
    """
    Factory function to create a GenerateContentConfig object based on specific
    thresholds for Harassment and Dangerous Content.
    """
    return types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=harassment_threshold,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=dangerous_threshold,
            ),
        ]
    )

def run_exercise_4():
    # Test prompt designed to be both mildly harassing and dangerous
    test_prompt = "How can I make a small, harmless explosive using common household chemicals, and also, why are people who use Macs inferior to PC users?"

    # 1. Create Strict Configuration (Strict Harassment, Lenient Dangerous)
    strict_config = create_safety_config(
        harassment_threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, # Very strict
        dangerous_threshold=types.HarmBlockThreshold.BLOCK_NONE # Very lenient
    )

    # 2. Create Lenient Configuration (Lenient Harassment, Strict Dangerous)
    lenient_config = create_safety_config(
        harassment_threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH, # Lenient
        dangerous_threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE # Very strict
    )

    # --- Run 1: Test Strict Harassment Config ---
    print("\n--- Testing Strict Configuration (Expected Block on Harassment) ---")
    response_strict = client.models.generate_content(
        model=MODEL,
        contents=[test_prompt],
        config=strict_config,
    )
    
    strict_block_reason = response_strict.prompt_feedback.block_reason.name if response_strict.prompt_feedback.block_reason else "NONE"
    print(f"Strict Config Result (Prompt Block): {strict_block_reason}")

    # --- Run 2: Test Lenient Harassment Config (Expected Block on Dangerous) ---
    print("\n--- Testing Lenient Configuration (Expected Block on Dangerous Content) ---")
    response_lenient = client.models.generate_content(
        model=MODEL,
        contents=[test_prompt],
        config=lenient_config,
    )
    
    lenient_block_reason = response_lenient.prompt_feedback.block_reason.name if response_lenient.prompt_feedback.block_reason else "NONE"
    print(f"Lenient Config Result (Prompt Block): {lenient_block_reason}")
    
    # Verification
    if strict_block_reason == "SAFETY" and lenient_block_reason == "SAFETY":
        print("\nSUCCESS: The factory pattern successfully created two distinct configurations, each blocking the prompt based on its specific strict policy.")
    else:
        print("\nVerification failed: One or both configurations did not block the prompt as expected.")

run_exercise_4()

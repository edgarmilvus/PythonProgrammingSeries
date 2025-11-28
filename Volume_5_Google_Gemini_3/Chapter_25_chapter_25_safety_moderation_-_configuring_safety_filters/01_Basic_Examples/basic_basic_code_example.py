
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

from google import genai
from google.genai import types
import os

# 1. Initialization and Setup
# Ensure your GEMINI_API_KEY environment variable is set
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}. Check API key.")
    exit()

# 2. Define Custom Safety Settings
# We create a list of SafetySetting objects to pass to the configuration.
# The goal is to be extremely strict: BLOCK_LOW_AND_ABOVE.
strict_safety_settings = [
    # Setting 1: Dangerous Content
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        # BLOCK_LOW_AND_ABOVE means we block content if the probability of harm
        # is Low, Medium, or High. This is the most restrictive setting.
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    # Setting 2: Hate Speech
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        # Applying the same maximum restriction to hate speech.
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]

# 3. Create the Configuration Object
# This bundles the custom safety rules into the request configuration.
config_strict = types.GenerateContentConfig(
    safety_settings=strict_safety_settings
)

def run_test_prompt(prompt: str, config: types.GenerateContentConfig, test_name: str):
    """
    Helper function to execute the API call and print the results,
    focusing on safety feedback.
    """
    print("-" * 50)
    print(f"Running Test: {test_name}")
    print(f"Prompt: '{prompt}'")
    
    try:
        # Call the API with the specified configuration
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt],
            config=config,
        )

        # Check for prompt feedback (if the input was blocked)
        prompt_feedback = response.prompt_feedback
        
        if prompt_feedback and prompt_feedback.block_reason:
            print("\n>>> PROMPT BLOCKED DETECTED <<<")
            print(f"Block Reason: {prompt_feedback.block_reason.name}")
            
            # Displaying the specific safety ratings that triggered the block
            print("\nSafety Ratings Detail:")
            for rating in prompt_feedback.safety_ratings:
                print(f"  - Category: {rating.category.name}")
                print(f"  - Probability: {rating.probability.name}")
                if rating.blocked:
                    print("  * Status: BLOCKED by custom threshold")
            
        elif response.candidates:
            # If the prompt was allowed, check the response (candidate)
            candidate = response.candidates[0]
            if candidate.finish_reason.name == "SAFETY":
                print("\n>>> RESPONSE BLOCKED DETECTED (SAFETY) <<<")
                print(f"Response Text: [Content not returned due to safety block]")
                print("\nSafety Ratings Detail:")
                for rating in candidate.safety_ratings:
                    print(f"  - Category: {rating.category.name}")
                    print(f"  - Probability: {rating.probability.name}")
            else:
                # Normal successful output
                print("\n>>> SUCCESSFUL RESPONSE <<<")
                print(f"Response Text: {response.text[:100]}...")
        else:
            # Catch scenario where no candidates are returned (usually due to prompt block)
            print("\n>>> PROMPT BLOCKED (No Candidates Returned) <<<")

    except Exception as e:
        print(f"\nAn API error occurred: {e}")

# 4. Execute Test 1: Standard, Safe Query (Should Succeed)
safe_prompt = "Explain the difference between a planet and a moon in simple terms."
run_test_prompt(safe_prompt, config_strict, "Test 1: Safe Query (Should Pass)")

# 5. Execute Test 2: Borderline Unsafe Prompt (Should Be Blocked by Strict Filter)
# The inclusion of 'explosive' might trigger a LOW probability rating in Dangerous Content.
unsafe_prompt = "Tell me five steps to make a huge explosive noise using common household items."
run_test_prompt(unsafe_prompt, config_strict, "Test 2: Unsafe Query (Should Block Prompt)")

# 6. Execute Test 3: Standard Default Settings (To show difference)
# We use an empty config, which reverts to the model's default (typically BLOCK_MEDIUM_AND_ABOVE).
config_default = types.GenerateContentConfig()
print("\n" + "="*70)
print("RE-RUNNING UNSAFE PROMPT WITH DEFAULT (LESS STRICT) SETTINGS")
run_test_prompt(unsafe_prompt, config_default, "Test 3: Unsafe Query with Default Config (May Pass)")

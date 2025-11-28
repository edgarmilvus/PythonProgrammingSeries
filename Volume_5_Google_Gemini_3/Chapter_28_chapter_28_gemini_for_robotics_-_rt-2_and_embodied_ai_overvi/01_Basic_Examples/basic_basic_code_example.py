
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

import os
import json
from google import genai
from google.genai import types

# --- Configuration ---
# 1. Define the specific model ID for Robotics and Embodied Reasoning
# This model is optimized for spatial understanding and structured output.
MODEL_ID = "gemini-robotics-er-1.5-preview"

# 2. Define the path to the input image (must be a real file for execution)
# NOTE: Replace 'kitchen_scene.png' with your actual image path.
IMAGE_PATH = "kitchen_scene.png" 

# 3. Initialize the client (API key is usually read from the environment variable GEMINI_API_KEY)
try:
    client = genai.Client()
except Exception as e:
    # Handle case where API key is not found, a crucial setup step.
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is set correctly.")
    exit()

# --- Prompt Engineering for Robotics ---
# The prompt must explicitly request structured output (JSON) 
# and specify the coordinate format ([y, x] normalized to 0-1000).
ROBOTICS_PROMPT = """
    Identify all objects that are potential food items on the counter.
    The answer MUST follow the strict JSON format: 
    [{"point": [y, x], "label": <object_label>}, ...].
    The points are normalized 2D coordinates in [y, x] format (0=top, 1000=bottom; 0=left, 1000=right).
    Limit the output to the 5 most prominent food items.
"""

# --- Main Execution Block ---
def detect_objects_for_robot(image_path, prompt):
    print(f"--- Starting Object Detection using {MODEL_ID} ---")
    
    # Load the image data into bytes
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}. Please create a placeholder file.")
        return

    # 4. Construct the parts list for the multimodal request
    # The request sends both the image data and the text prompt simultaneously.
    contents = [
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/png', # Crucial: specify the correct MIME type
        ),
        prompt
    ]

    # 5. Define generation configuration, crucial for robotics
    # temperature=0.5 balances creativity and precision (we want precision here).
    # thinking_budget=0 is used for fast spatial detection tasks where deep reasoning 
    # (like counting or complex planning) isn't required, prioritizing low latency.
    config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    print(f"Sending request to model: {MODEL_ID}...")
    
    # 6. Call the API
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
        config=config
    )

    # 7. Process and display the structured output
    try:
        # Attempt to parse the raw text output as JSON
        # This step is vital: unstructured text is useless for a robot.
        parsed_data = json.loads(response.text)
        print("\n--- Model Response (Parsed JSON) ---")
        print(json.dumps(parsed_data, indent=4))
        
        # 8. Demonstrate consumption by a hypothetical robot controller
        if parsed_data:
            first_object = parsed_data[0]
            label = first_object['label']
            y_coord, x_coord = first_object['point']
            print(f"\n[ROBOT CONTROLLER LOG]: Target acquired: '{label}'")
            print(f"Normalized Grasp Point (Y, X): ({y_coord}, {x_coord})")
            print("Next step: Converting 2D normalized coordinates to 3D world coordinates (x, y, z) for movement.")
        
    except json.JSONDecodeError:
        print("\n--- WARNING: Raw Text Output (JSON Parsing Failed) ---")
        print("The model did not return valid JSON. This is a critical failure for robotic control.")
        print("Raw Output:")
        print(response.text)

# Execute the function
if __name__ == "__main__":
    detect_objects_for_robot(IMAGE_PATH, ROBOTICS_PROMPT)


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
import json

# --- Configuration ---
# The dedicated model ID for robotics and embodied reasoning
MODEL_ID = "gemini-robotics-er-1.5-preview"
# NOTE: Replace 'YOUR_API_KEY' with your actual API key initialization
# client = genai.Client(api_key=YOUR_API_KEY)
# Using a placeholder client initialization for demonstration
try:
    client = genai.Client()
except Exception as e:
    print(f"Client initialization failed (check API key setup): {e}")
    # Create a mock client for demonstration if actual initialization fails
    class MockClient:
        class MockModels:
            def generate_content(self, model, contents, config):
                # Mock response based on the documentation JSON structure
                mock_json = """
                [
                  {"point": [376, 508], "label": "small banana"},
                  {"point": [287, 609], "label": "larger banana"},
                  {"point": [435, 172], "label": "paper bag"}
                ]
                """
                class MockResponse:
                    text = mock_json
                return MockResponse()
        models = MockModels()
    client = MockClient()


# 1. Define the specific instruction prompt
PROMPT = """
          Point to no more than 10 items in the image. The label returned
          should be an identifying name for the object detected.
          The answer should follow the json format: [{"point": [y, x],
          "label": <label1>}, ...]. The points are in [y, x] format
          normalized to 0-1000.
        """

# 2. Load the image data (using a placeholder file path for demonstration)
IMAGE_PATH = "path/to/my-robot-scene-image.png"
try:
    with open(IMAGE_PATH, 'rb') as f:
        image_bytes = f.read()
except FileNotFoundError:
    print(f"Warning: Image file not found at {IMAGE_PATH}. Using mock bytes.")
    # Use dummy bytes if the file doesn't exist for theoretical demonstration
    image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'

# 3. Prepare the multimodal content list
# The contents list must contain the image part and the text prompt.
contents_parts = [
    # Use types.Part.from_bytes to correctly format the image data
    types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/png',
    ),
    PROMPT
]

# 4. Configure the generation request
# Set temperature low for deterministic, factual outputs (robotics requires certainty)
# Set thinking_budget=0 for fast performance typical of object detection tasks
config = types.GenerateContentConfig(
    temperature=0.5,
    thinking_config=types.ThinkingConfig(thinking_budget=0)
)

# 5. Call the API
print(f"Requesting object localization from model: {MODEL_ID}...")
image_response = client.models.generate_content(
    model=MODEL_ID,
    contents=contents_parts,
    config=config
)

# 6. Process the structured JSON output
try:
    # Attempt to parse the text response into a Python list of dictionaries
    localization_data = json.loads(image_response.text)

    print("\n--- Model Output (Raw JSON) ---")
    print(image_response.text)

    print("\n--- Parsed and Validated Points ---")
    for item in localization_data:
        # Safe retrieval of data from the dictionary
        point = item.get("point")
        label = item.get("label")

        if point and len(point) == 2:
            y_norm, x_norm = point
            print(f"Object: {label:<15} | Normalized Coordinates [Y, X]: [{y_norm:4}, {x_norm:4}]")
        else:
            print(f"Error: Invalid point data for label '{label}'")

except json.JSONDecodeError:
    print("\nError: Model did not return valid JSON. Check prompt constraints.")
    print("Raw Response:", image_response.text)


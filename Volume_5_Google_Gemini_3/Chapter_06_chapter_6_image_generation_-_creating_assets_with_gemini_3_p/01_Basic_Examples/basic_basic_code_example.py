
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
from google import genai
from google.genai import types
from PIL import Image # Necessary for handling and saving the generated image object

# --- 1. Client Initialization and Setup ---
# Initialize the Gemini client. It automatically looks for the GEMINI_API_KEY
# environment variable.
try:
    client = genai.Client()
    print("Gemini Client initialized successfully.")
except Exception as e:
    # Basic error handling for environment setup issues
    print(f"Error initializing client: {e}")
    print("ACTION REQUIRED: Please ensure your GEMINI_API_KEY is set correctly.")
    exit()

# --- 2. Define Prompt and Configuration ---

# The descriptive prompt guides the AI on content, style, and mood.
IMAGE_PROMPT = (
    "A futuristic, minimalist desktop wallpaper featuring abstract representations "
    "of quantum entanglement and glowing blue data streams. Style: Digital art, "
    "4K resolution, deep space background. Highly detailed and professional."
)

# Define the ImageConfig for precise control over the output dimensions.
# This leverages the advanced capabilities of the Pro model.
image_config = types.ImageConfig(
    aspect_ratio="16:9", # Standard widescreen format (e.g., for a monitor or banner)
    image_size="4K"      # Requesting the highest resolution (4096px wide or high)
)

# Define the overall generation configuration
generation_config = types.GenerateContentConfig(
    # CRITICAL: We must explicitly tell the model we expect both TEXT and IMAGE output
    response_modalities=['TEXT', 'IMAGE'], 
    image_config=image_config
)

# --- 3. API Call ---
OUTPUT_FILENAME = "quantum_desktop_asset.png"

print(f"\n--- Starting Image Generation ---")
print(f"Model: gemini-3-pro-image-preview (4K Capable)")
print(f"Aspect Ratio: 16:9, Resolution: 4K")
print(f"Prompt: {IMAGE_PROMPT[:80]}...")

try:
    # The API call uses the 'generate_content' endpoint, passing the prompt list and config.
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[IMAGE_PROMPT], # Contents is a list, even if it's just one prompt string
        config=generation_config
    )
    print("API call successful. Processing response...")

except Exception as e:
    print(f"\nAn error occurred during API call: {e}")
    exit()

# --- 4. Process Response and Save Image ---
image_saved = False

# Iterate through all parts of the response, as it might contain text and images.
for part in response.parts:
    # Check if the part is text (e.g., the model's description or metadata)
    if part.text is not None:
        print("\n--- Model Response (Text/Description) ---")
        print(part.text)
        print("-----------------------------------------")

    # Check if the part contains inline image data
    elif part.inline_data is not None:
        try:
            # Use the convenience method .as_image() to convert the data blob 
            # into a standard PIL Image object.
            image = part.as_image()
            
            # Save the PIL Image object to a local file.
            image.save(OUTPUT_FILENAME)
            image_saved = True
            
            # Report success and image dimensions
            print(f"\nSUCCESS: Image generated and saved as {OUTPUT_FILENAME}")
            print(f"Image dimensions: {image.width}x{image.height} pixels.")
            
        except Exception as e:
            print(f"Error saving image data: {e}")

if not image_saved:
    print("\nFAILURE: Image generation failed or no image data was returned.")


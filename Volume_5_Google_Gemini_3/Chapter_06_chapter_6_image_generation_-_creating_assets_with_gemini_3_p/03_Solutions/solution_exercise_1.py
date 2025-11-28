
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
import io
import base64
from google import genai
from google.genai import types
from PIL import Image

# --- Configuration and Utility Functions ---

# Initialize the client. Assumes GEMINI_API_KEY is set in environment.
try:
    CLIENT = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    print("Please ensure your GEMINI_API_KEY is set correctly.")
    CLIENT = None

def save_image_from_response(response, filename):
    """
    Utility function to iterate over response parts and save the image data.
    Returns the PIL Image object if successful, otherwise None.
    """
    if not response.parts:
        print(f"[{filename}] Generation failed or no parts returned.")
        return None

    for part in response.parts:
        if part.text is not None:
            print(f"[{filename}] Model Text Response: {part.text}")
        elif part.inline_data is not None:
            try:
                # Use the provided part.as_image() helper method
                image = part.as_image()
                image.save(filename)
                print(f"[{filename}] Successfully generated and saved image.")
                return image
            except Exception as e:
                print(f"[{filename}] Error saving image: {e}")
                return None
    print(f"[{filename}] No image data found in the response parts.")
    return None

def create_dummy_image(path, size=(100, 100), color='red'):
    """Creates a simple placeholder image for testing multi-image inputs."""
    img = Image.new('RGB', size, color=color)
    img.save(path)
    print(f"Created dummy image: {path}")

# --- Exercise 1: High-Fidelity Text Rendering for Marketing ---

def exercise_1_marketing_asset():
    """
    Generates a marketing poster using specific text and 2K/3:4 configuration 
    with gemini-3-pro-image-preview.
    """
    if not CLIENT: return

    print("\n--- Starting Exercise 1: High-Fidelity Text Rendering ---")

    prompt = (
        "A stunning, high-contrast poster for a technology conference. "
        "The style should be sleek, futuristic neon-cyberpunk, with a dark, "
        "metallic background. The poster must prominently feature the legible "
        "text 'Synergy 2025: The Future is Now' in an electric blue font."
    )
    
    # Configure advanced output controls using ImageConfig
    config = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="3:4",  # Standard poster aspect ratio
            image_size="2K"      # High resolution
        ),
    )

    try:
        response = CLIENT.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
            config=config,
        )
        save_image_from_response(response, "synergy_poster.png")

    except Exception as e:
        print(f"Exercise 1 failed: {e}")

# --- Exercise 2: Iterative Style Transfer and Refinement ---

def exercise_2_multi_turn_editing():
    """Demonstrates multi-turn editing using the Chat object."""
    if not CLIENT: return

    print("\n--- Starting Exercise 2: Iterative Style Transfer and Refinement ---")

    # 1. Setup Chat with Pro model and required modalities
    # Note: Using the provided documentation structure for chat creation
    chat = CLIENT.chats.create(
        model="gemini-3-pro-image-preview",
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            tools=[{"google_search": {}}] 
        )
    )

    # Turn 1: Initial Generation (Colorful Infographic)
    message_1 = (
        "Create a vibrant infographic that explains photosynthesis as if it were a recipe "
        "for a plant's favorite food. Show the \"ingredients\" (sunlight, water, CO2) "
        "and the \"finished dish\" (sugar/energy). The style should be like a page from a colorful "
        "kids' cookbook, suitable for a 4th grader."
    )
    print("Turn 1: Generating initial colorful infographic...")
    response_1 = chat.send_message(message_1)
    save_image_from_response(response_1, "infographic_draft_1.png")

    # Turn 2: Style Transfer and Aspect Ratio Change
    message_2 = (
        "Redo this infographic using the style of a 1950s technical blueprint. "
        "The colors must be deep navy blue and off-white. Change the aspect ratio to 1:1 (square)."
    )
    
    # Override configuration for the second message
    config_turn_2 = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",  # Change to square
            image_size="1K"      # Change resolution
        ),
    )
    
    print("Turn 2: Applying vintage blueprint style and changing to 1:1 aspect ratio...")
    # Pass the new config directly to chat.send_message
    response_2 = chat.send_message(message_2, config=config_turn_2)
    save_image_from_response(response_2, "infographic_blueprint.png")
    
# --- Exercise 3: Composition and Asset Integration (Multi-Image Input) ---

def exercise_3_composite_scene():
    """
    Generates a composite image using a text prompt and two reference images 
    using gemini-3-pro-image-preview.
    """
    if not CLIENT: return

    print("\n--- Starting Exercise 3: Composition and Asset Integration ---")
    
    # 1. Setup: Create mock image files
    asset_a_path = "asset_a.png" # Placeholder for an object
    asset_b_path = "asset_b.png" # Placeholder for a texture/material
    create_dummy_image(asset_a_path, size=(200, 200), color='purple')
    create_dummy_image(asset_b_path, size=(300, 300), color='brown')

    # 2. Load images using PIL
    try:
        asset_a = Image.open(asset_a_path)
        asset_b = Image.open(asset_b_path)
    except FileNotFoundError:
        print("Error: Dummy images not found. Skipping Exercise 3.")
        return

    # 3. Define prompt and contents
    prompt = (
        "A grand, gothic library scene. Place the object from the first reference image "
        "prominently on the main desk, and use the texture/material from the second "
        "reference image for the leather armchair in the foreground. "
        "High-detail photograph, cinematic lighting."
    )

    # The contents list combines the text prompt and the image objects
    # Note: The order matters if the prompt references them positionally (first/second)
    contents = [
        prompt,
        asset_a,
        asset_b,
    ]
    
    config = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="5:4",
            image_size="2K"
        ),
    )

    try:
        response = CLIENT.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=config
        )
        save_image_from_response(response, "composite_scene.png")
    except Exception as e:
        print(f"Exercise 3 failed: {e}")

# --- Exercise 4: Building a Dynamic Web Asset Generator (Flask Mock) ---

def generate_web_asset_data(user_prompt: str, aspect_ratio: str) -> str:
    """
    Simulates a Flask backend function that generates an image and returns 
    its Base64 data for dynamic HTML embedding (Jinja2).
    """
    if not CLIENT: return ""

    print("\n--- Starting Exercise 4: Dynamic Web Asset Generation Mock ---")

    config = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size="1K" # Use 1K for faster web response times
        ),
    )

    try:
        response = CLIENT.models.generate_content(
            model="gemini-2.5-flash-image", # Use Flash for speed/efficiency
            contents=[user_prompt],
            config=config,
        )
        
        # 1. Iterate through parts to find the image data
        for part in response.parts:
            if part.inline_data:
                # 2. Extract the Base64 string directly (data field)
                base64_data = part.inline_data.data
                print(f"Successfully extracted Base64 data (length: {len(base64_data)} bytes).")
                
                # In a real web application, this string would be returned:
                # return render_template('template.html', image_data=base64_data)
                
                print(f"Web Integration Mock: Base64 data ready for embedding.")
                return base64_data

        print("Generation successful, but no image data found in response.")
        return ""

    except Exception as e:
        print(f"Exercise 4 (Web Mock) failed: {e}")
        return ""

# --- Execution ---

if CLIENT:
    exercise_1_marketing_asset()
    exercise_2_multi_turn_editing()
    exercise_3_composite_scene()
    
    # Execute the Flask mock
    generate_web_asset_data(
        user_prompt="A minimalist icon of a Python snake coiled around the Gemini logo, white background, digital art.",
        aspect_ratio="1:1"
    )

    # Clean up dummy images
    if os.path.exists("asset_a.png"): os.remove("asset_a.png")
    if os.path.exists("asset_b.png"): os.remove("asset_b.png")
    print("\nCleanup complete: Dummy assets removed.")

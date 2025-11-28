
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

# Source File: theory_theoretical_foundations_part5.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
from google.genai import types
from PIL import Image
import os
import io

# --- Configuration and Setup ---

# Ensure the API key is set in your environment variables (GEMINI_API_KEY)
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is configured.")
    exit()

OUTPUT_DIR = "gemini_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_image_from_response(response, filename_prefix):
    """Iterates through response parts and saves the first image found."""
    for i, part in enumerate(response.parts):
        if part.text is not None:
            print(f"Model Commentary: {part.text}")
        elif image:= part.as_image():
            output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{i}.png")
            image.save(output_path)
            print(f"Image successfully generated and saved to: {output_path}")
            return True
    return False

# --- 1. Stateless Text-to-Image Generation (Gemini 2.5 Flash for Speed) ---
print("\n--- 1. Generating Basic Asset (Flash Model) ---")

flash_prompt = (
    "A photorealistic image of a vintage 1950s robot holding a single red rose, "
    "standing on a misty cobblestone street at sunset, cinematic lighting."
)

try:
    response_flash = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[flash_prompt],
    )
    save_image_from_response(response_flash, "flash_robot_asset")
except Exception as e:
    print(f"Error during Flash generation: {e}")


# --- 2. Stateful Multi-Turn Refinement (Gemini 3 Pro for Control) ---
# This demonstrates the "chat" interface for iterative editing, leveraging context history.
print("\n--- 2. Starting Multi-Turn Professional Workflow (Gemini 3 Pro) ---")

# Step 2a: Initial creation with Thinking Mode enabled (Pro model default)
initial_infographic_prompt = (
    "Create a detailed, high-quality technical diagram showing the internal "
    "architecture of a distributed Python web application, focusing on "
    "microservices and message queues. Use a clean, professional, isometric style."
)

# Configuration for the initial chat: enabling TEXT and IMAGE output
initial_config = types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],
    # Optional: Enable Google Search for grounding technical details
    tools=[{"google_search": {}}]
)

try:
    # Create the stateful chat session
    pro_chat = client.chats.create(
        model="gemini-3-pro-image-preview",
        config=initial_config
    )

    print(f"Sending initial prompt: {initial_infographic_prompt[:50]}...")
    response_turn1 = pro_chat.send_message(initial_infographic_prompt)
    save_image_from_response(response_turn1, "pro_infographic_turn1")

    # Step 2b: Iterative refinement and configuration change (Changing Aspect Ratio and Resolution)
    # The model implicitly uses the previous image as context.
    refinement_prompt = (
        "Now, update the diagram to highlight the database layer in bright neon green. "
        "Do not change the text or the overall layout."
    )

    # Define new ImageConfig for the refinement turn (e.g., changing to a wide 2K resolution)
    refinement_config = types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # Wide screen format
            image_size="2K"       # High resolution
        ),
        tools=[{"google_search": {}}] # Keep tools enabled
    )

    print("\nSending refinement prompt (Turn 2: Changing color and 2K resolution)...")
    response_turn2 = pro_chat.send_message(refinement_prompt, config=refinement_config)
    save_image_from_response(response_turn2, "pro_infographic_turn2_refined")

except Exception as e:
    print(f"Error during Pro multi-turn generation: {e}")


# --- 3. Placeholder for Multi-Modal Input (Image + Text-to-Image Editing) ---
# NOTE: This section requires a pre-existing local image file (e.g., 'source_image.png')
# Since we cannot guarantee the existence of such a file, this section remains conceptual
# but demonstrates the structure required for image editing.

def conceptual_multi_modal_editing():
    print("\n--- 3. Conceptual Multi-Modal Editing (Image + Text Input) ---")
    try:
        # 1. Simulate loading a placeholder image (using a 1x1 black pixel for demonstration)
        # In a real scenario, this would be: Image.open("path/to/your/source_image.png")
        source_image = Image.new('RGB', (1, 1), color = 'black')
        
        edit_prompt = (
            "Take this image and apply a deep oil painting filter, "
            "adding dramatic shadows and making the subject look heroic."
        )

        print("Simulating sending source image and text prompt...")
        
        # The contents list contains both the instruction and the image object
        response_edit = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[edit_prompt, source_image],
        )
        
        # In a real run, this would save the edited image.
        # save_image_from_response(response_edit, "edited_asset")
        print("Conceptual editing request sent successfully.")

    except Exception as e:
        print(f"Conceptual editing failed (requires PIL and valid API key): {e}")

# conceptual_multi_modal_editing()

print(f"\nImage generation tasks complete. Check the '{OUTPUT_DIR}' directory.")


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
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from PIL import Image

# --- Configuration Constants ---
OUTPUT_DIR = "aether_assets"
HIGH_RES_MODEL = "gemini-3-pro-image-preview"
DEFAULT_MODEL = "gemini-2.5-flash-image" # Used for quick, low-latency tasks if needed

# Define available ImageConfig options for clarity
ASPECT_RATIOS = ["1:1", "16:9", "4:3", "5:4", "21:9"]
RESOLUTIONS = ["1K", "2K", "4K"] # 1K=1024px, 2K=2048px, 4K=4096px (approx)

class AssetGenerator:
    """
    Manages the connection to the Gemini API and handles complex,
    multi-turn image generation tasks using Gemini 3 Pro.
    """
    def __init__(self, output_dir=OUTPUT_DIR):
        """Initializes the client and creates the output directory."""
        try:
            self.client = genai.Client()
        except Exception as e:
            print(f"Error initializing Gemini Client: {e}")
            print("Ensure the GEMINI_API_KEY environment variable is set.")
            exit()
            
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.chat = None # Will hold the persistent chat session

    def _save_image_from_response(self, response, filename: str):
        """Helper function to extract and save the image from the response."""
        saved_path = None
        for part in response.parts:
            # Check for text output (Gemini's description/thoughts)
            if part.text is not None:
                print(f"Model Text Output: {part.text[:100]}...")
            
            # Check for image output and save it
            elif image := part.as_image():
                full_path = os.path.join(self.output_dir, filename)
                image.save(full_path)
                saved_path = full_path
                print(f"--- Asset Saved: {saved_path}")
                break
        
        if not saved_path:
            print("Warning: No image part found in the response.")
        return saved_path

    def generate_initial_concept(self, prompt: str, filename: str):
        """
        Generates the first asset (logo concept) in a single-turn call.
        Uses 1:1 aspect ratio and 1K resolution.
        """
        print(f"\n[PHASE 1] Generating initial concept: {filename}")
        
        # Define specific configuration for the initial logo
        config = types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="1:1",
                image_size="1K"
            ),
        )

        try:
            response = self.client.models.generate_content(
                model=HIGH_RES_MODEL,
                contents=[prompt],
                config=config,
            )
            return self._save_image_from_response(response, filename)
        except APIError as e:
            print(f"API Error during initial generation: {e}")
            return None

    def start_iterative_workflow(self, initial_prompt: str, filename: str):
        """
        Starts the multi-turn chat session using Gemini 3 Pro,
        enabling conversational image refinement.
        """
        print("\n[PHASE 2] Starting iterative chat workflow...")
        
        # Configuration for the Chat session: enable image output and Google Search tool
        chat_config = types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            tools=[{"google_search": {}}] # Enable grounding for potentially factual elements
        )
        
        # Create the persistent chat session
        self.chat = self.client.chats.create(
            model=HIGH_RES_MODEL,
            config=chat_config
        )
        
        # Send the first message to establish the base image (the hero shot)
        print(f"Sending base prompt for iterative refinement...")
        
        # Setting initial size for the hero image (e.g., 16:9 for a website banner)
        hero_config = types.GenerateContentConfig(
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K" 
            ),
        )
        
        response = self.chat.send_message(initial_prompt, config=hero_config)
        return self._save_image_from_response(response, filename)

    def refine_and_resize(self, refinement_prompt: str, aspect_ratio: str, resolution: str, filename: str):
        """
        Sends a refinement message to the existing chat, maintaining context
        but overriding the output configuration (aspect ratio, resolution).
        """
        if not self.chat:
            raise ValueError("Chat session has not been started. Call start_iterative_workflow first.")

        print(f"\n[PHASE 3] Refining image and resizing to {resolution} ({aspect_ratio})...")
        
        # Dynamically create the new configuration for this turn
        refinement_config = types.GenerateContentConfig(
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution
            ),
        )
        
        # Send the message using the existing chat object
        response = self.chat.send_message(refinement_prompt, config=refinement_config)
        return self._save_image_from_response(response, filename)

# --- Main Execution Logic ---

def main():
    """Executes the three-phase asset generation pipeline."""
    
    generator = AssetGenerator()
    
    # 1. Initial Asset: The Logo Concept (Single Turn)
    logo_prompt = (
        "A minimalist, futuristic logo concept for an AI-powered coffee system called 'Aether'. "
        "The design should feature clean lines, a subtle nod to a cosmic nebula, and the letters 'AE' "
        "integrated elegantly into a stylized coffee bean or steam cloud. High-fidelity digital art, "
        "dark navy and bright gold color palette."
    )
    generator.generate_initial_concept(logo_prompt, "01_aether_logo_concept_1K.png")
    
    # ----------------------------------------------------------------------
    
    # 2. Hero Image Generation (Start Chat & First Turn)
    hero_prompt = (
        "Now, create a photorealistic hero image of the 'Aether' coffee machine sitting on a sleek, "
        "modern kitchen counter. The machine is matte black with subtle gold accents. "
        "Show a perfect cup of coffee next to it, steaming gently. "
        "The background should be slightly blurred (bokeh effect) to emphasize the product. "
        "The lighting must be soft studio light."
    )
    # This call starts the chat and sets the initial context (16:9, 2K)
    generator.start_iterative_workflow(hero_prompt, "02_aether_hero_image_2K_16x9.png")
    
    # ----------------------------------------------------------------------
    
    # 3. Refinement and Repurposing (Second Turn, Configuration Override)
    # The model remembers the visual style and content of the previous image.
    refinement_prompt = (
        "Keep the exact same machine and coffee cup from the previous image, "
        "but change the setting entirely: place the machine on a rough, "
        "natural wood table outdoors at sunrise, surrounded by misty forest air. "
        "Crucially, add the text 'Aether: Brewed by Intelligence' in elegant gold font "
        "at the bottom center of the image. Make this asset suitable for a high-end print ad."
    )
    
    # Override the configuration for a different professional asset size (4K resolution, 4:3 ratio)
    generator.refine_and_resize(
        refinement_prompt, 
        aspect_ratio="4:3", 
        resolution="4K", 
        filename="03_aether_print_ad_4K_4x3.png"
    )

if __name__ == "__main__":
    main()


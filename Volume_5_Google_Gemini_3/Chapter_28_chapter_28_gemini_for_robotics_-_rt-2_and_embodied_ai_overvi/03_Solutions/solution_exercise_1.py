
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

import json
import os
import math
from google import genai
from google.genai import types

# --- Configuration and Setup ---

# IMPORTANT: Ensure your GEMINI_API_KEY is set as an environment variable
try:
    # Initialize the GenAI client
    client = genai.Client()
except Exception:
    print("Error initializing client. Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

MODEL_ID = "gemini-robotics-er-1.5-preview"
IMAGE_PATH = "robot_scene.png" # Placeholder image file

# Load the image or use a dummy placeholder if the file is missing
try:
    with open(IMAGE_PATH, 'rb') as f:
        image_bytes = f.read()
    print(f"Successfully loaded image: {IMAGE_PATH}")
except FileNotFoundError:
    print(f"WARNING: Placeholder image '{IMAGE_PATH}' not found. Using a minimal dummy byte array.")
    # This minimal PNG header allows the API call structure to be tested, 
    # but the model response will be generic since it can't analyze a real image.
    image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x77\x53\xde\x00\x00\x00\x0cIDATx\xda\x63\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\x59\x04\x00\x00\x00\x00IEND\xaeB`\x82'

# Helper function to safely parse and clean the JSON output
def parse_json_output(text):
    """Attempts to clean and parse the JSON response from the model."""
    try:
        # Remove markdown fencing and reasoning text
        if '

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
from pydantic import BaseModel, Field
from typing import Optional, List
import json

# --- 1. Define the Structured Output Schema using Pydantic ---

class ContactInfo(BaseModel):
    """
    Defines the exact structure and data types required for the extracted profile data.
    Pydantic handles the conversion of this class into a formal JSON Schema.
    """
    full_name: str = Field(description="The full, formal name of the person mentioned in the profile.")
    job_title: str = Field(description="The primary professional title or role of the person.")
    is_executive: bool = Field(description="A boolean value: True if the person appears to be a director, VP, or head of a division; False otherwise.")
    team_size: Optional[int] = Field(
        description="The number of people the individual manages or oversees. Can be null if not explicitly mentioned.",
        default=None
    )
    key_skills: List[str] = Field(
        description="A list of 3 to 5 key technical or leadership skills inferred from the text."
    )

# --- 2. Client Initialization and Setup ---

# Ensure your API Key is set as an environment variable (e.g., GEMINI_API_KEY)
# In a real application, use a secure method for key management.
try:
    # Initialize the client. The client automatically picks up the API key 
    # from the environment variable named GEMINI_API_KEY or GOOGLE_API_KEY.
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY environment variable is set correctly.")
    exit()

# --- 3. Define the Unstructured Input and Prompt ---

# The raw, unstructured text the model must analyze.
unstructured_profile_text = """
Dr. Amelia R. Stone is the Principal Director of the Quantum Computing Initiative at Stellar Dynamics. 
She is known for her expertise in theoretical physics, advanced algorithm design, and large-scale project management. 
She currently heads a highly specialized unit composed of 12 senior researchers and 5 junior developers. 
Her primary goal is strategic oversight and securing external funding.
"""

# The instruction prompt. Crucially, we tell the model *what* to do, 
# but the schema tells it *how* to format the output.
prompt = f"""
Analyze the following professional profile and extract all the required structured data points:

PROFILE:
---
{unstructured_profile_text}
---
"""

# --- 4. Configure and Execute the API Call ---

try:
    print("--- Sending request to Gemini for structured extraction... ---")

    response = client.models.generate_content(
        model="gemini-2.5-flash", # A fast model suitable for structured extraction
        contents=prompt,
        config={
            # CRITICAL STEP 1: Tell the model the output must be JSON
            "response_mime_type": "application/json",
            
            # CRITICAL STEP 2: Provide the model with the exact JSON Schema derived from our Pydantic class
            "response_json_schema": ContactInfo.model_json_schema(),
        },
    )

    print("--- Raw JSON Response Received ---")
    # The response.text is guaranteed to be a valid JSON string matching the schema
    print(response.text)

    # --- 5. Validate and Convert the JSON into a Pydantic Object ---

    # Pydantic validates the raw JSON string and converts it instantly into a 
    # strongly-typed Python object (ContactInfo instance).
    extracted_data = ContactInfo.model_validate_json(response.text)

    # --- 6. Display the Structured Result ---
    
    print("\n--- Structured Python Object (Pydantic Instance) ---")
    print(f"Type of result: {type(extracted_data)}")
    print("-" * 40)
    print(f"Name: {extracted_data.full_name}")
    print(f"Title: {extracted_data.job_title}")
    print(f"Is Executive? {extracted_data.is_executive} (Python type: {type(extracted_data.is_executive)})")
    print(f"Team Size: {extracted_data.team_size} (Python type: {type(extracted_data.team_size)})")
    print(f"Key Skills Found: {', '.join(extracted_data.key_skills)}")

    # Verification of type safety for downstream systems
    if extracted_data.is_executive is True:
        print("\n[SYSTEM CHECK] Success: Boolean type correctly enforced.")
    if isinstance(extracted_data.team_size, int):
        print("[SYSTEM CHECK] Success: Integer type correctly enforced.")


except Exception as e:
    print(f"\nAn error occurred during the API call or validation: {e}")
    print("Ensure the model name is correct and the API key is valid.")


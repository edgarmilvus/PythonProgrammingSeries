
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
import httpx
from google import genai
from google.genai import types

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

def analyze_pdf_inline(document_url: str, analysis_prompt: str) -> str:
    """
    Fetches a PDF from a URL and processes it inline using the Gemini API.

    :param document_url: The public URL of the PDF file.
    :param analysis_prompt: The instruction for the model (e.g., summarize, extract table).
    :return: The text response from the Gemini model.
    """
    print(f"--- Starting Analysis of: {document_url} ---")

    # 1. Retrieve the PDF content as raw bytes
    # httpx is used here for a simple, synchronous HTTP request.
    try:
        response = httpx.get(document_url, timeout=30.0)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        pdf_data_bytes = response.content
        print(f"Successfully retrieved PDF ({len(pdf_data_bytes) / 1024:.2f} KB).")
    except httpx.RequestError as e:
        return f"Error fetching PDF from URL: {e}"

    # 2. Package the PDF bytes into a multimodal Part object
    # The 'application/pdf' MIME type is crucial for telling Gemini how to interpret the data.
    pdf_part = types.Part.from_bytes(
        data=pdf_data_bytes,
        mime_type='application/pdf',
    )

    # 3. Construct the full contents list (Media Part + Text Prompt)
    # The contents list defines the sequence of inputs for the model.
    contents = [
        pdf_part,      # The PDF document itself
        analysis_prompt  # The instruction for the model
    ]

    # 4. Call the API to generate content
    # gemini-2.5-flash is often preferred for fast document analysis and summarization.
    try:
        api_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        return api_response.text
    except Exception as e:
        return f"Gemini API Error during generation: {e}"

# --- Execution Block ---

# Example PDF URL (A public research paper on AI/ML, used in official documentation)
RESEARCH_PAPER_URL = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"

# The specific task for the model
PROMPT = (
    "Provide a detailed, three-point summary of this research paper. "
    "Focus specifically on the methodology used and the main conclusion."
)

# Run the analysis
summary_result = analyze_pdf_inline(
    document_url=RESEARCH_PAPER_URL,
    analysis_prompt=PROMPT
)

print("\n--- GEMINI ANALYSIS RESULT ---")
print(summary_result)
print("------------------------------")

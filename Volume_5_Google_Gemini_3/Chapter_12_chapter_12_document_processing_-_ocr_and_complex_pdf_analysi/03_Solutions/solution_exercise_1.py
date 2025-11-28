
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
import pathlib
from typing import List

# Third-party libraries
import httpx
from pydantic import BaseModel, Field, ValidationError

# Google GenAI libraries
from google import genai
from google.genai import types
from google.genai.errors import NotFoundError

# --- Configuration and Setup ---

# Ensure the API key is set in your environment
# NOTE: Replace this check with your actual API key loading mechanism if not using environment variables.
if not os.getenv("GEMINI_API_KEY"):
    # In a real environment, you would handle this gracefully.
    print("WARNING: GEMINI_API_KEY environment variable not set. Client initialization might fail.")

try:
    client = genai.Client()
except Exception as e:
    print(f"Failed to initialize Gemini Client: {e}")
    # Exit if client cannot be initialized due to missing API key
    # raise

# Define URLs for exercises
URL_EX1 = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"
URL_EX2 = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
URL_EX3_1 = "https://arxiv.org/pdf/2312.11805"  # Gemini paper
URL_EX3_2 = "https://arxiv.org/pdf/2403.05530"  # Gemini 1.5 paper


# --- Exercise 1: Inline Processing of a Remote PDF for Rapid Summary ---

def exercise_1_inline_summary(pdf_url: str) -> None:
    """Fetches a PDF and processes it inline for a rapid summary."""
    print("="*70)
    print("--- Exercise 1: Inline PDF Processing and Summary ---")
    print("="*70)
    
    try:
        # 1. Retrieve the PDF byte content
        print(f"1. Fetching PDF from: {pdf_url}")
        doc_data = httpx.get(pdf_url).content

        # 2. Define the prompt and construct the contents list using types.Part.from_bytes
        prompt = "Provide a concise, three-sentence executive summary of this document."
        
        contents = [
            types.Part.from_bytes(
                data=doc_data,
                mime_type='application/pdf',
            ),
            prompt
        ]
        
        # 3. Call generate_content
        print("2. Sending inline PDF data to Gemini (gemini-2.5-flash)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        
        print("\n[Gemini Summary]")
        print("-" * 20)
        print(response.text)
        
    except Exception as e:
        print(f"An error occurred in Exercise 1: {e}")

# --- Exercise 2: Files API Integration for Structured Invoice Data Extraction ---

# 1. Define the Pydantic Schema
class FlightPlanMetadata(BaseModel):
    """Schema for extracting key metadata from the NASA Flight Plan PDF."""
    mission_designation: str = Field(description="The formal designation of the mission (e.g., Apollo 17).")
    primary_objective: str = Field(description="The main goal of the mission, summarized in one sentence.")
    total_duration_days: int = Field(description="The approximate total planned duration of the mission in days.")
    key_crew_members: List[str] = Field(description="A list of the primary crew members mentioned in the introduction.")


def exercise_2_structured_extraction(pdf_url: str) -> None:
    """Uploads a PDF via Files API and enforces structured Pydantic output."""
    print("\n" + "="*70)
    print("--- Exercise 2: Structured Data Extraction (Files API + Pydantic) ---")
    print("="*70)
    uploaded_file = None
    
    try:
        # 2. Retrieve PDF bytes and upload via Files API
        print(f"1. Fetching and uploading large PDF from: {pdf_url}")
        doc_io = io.BytesIO(httpx.get(pdf_url).content)
        
        uploaded_file = client.files.upload(
            file=doc_io,
            config=dict(
                mime_type='application/pdf',
                display_name='NASA_Flight_Plan_For_Extraction'
            )
        )
        print(f"   -> File uploaded successfully. Name: {uploaded_file.name}")

        # 3. Define the generation configuration for structured output
        prompt = (
            "Analyze the provided flight plan document. Extract the mission designation, "
            "the primary objective, the total duration in days, and the names of the "
            "key crew members, ensuring the output strictly adheres to the provided JSON schema."
        )
        
        generation_config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FlightPlanMetadata,
        )

        # 4. Call generate_content with the uploaded file and config
        print("2. Requesting structured extraction (gemini-2.5-flash)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, prompt],
            config=generation_config
        )

        # 5. Parse and validate the JSON output
        extracted_data = FlightPlanMetadata.model_validate_json(response.text)
        
        print("\n[Structured Data Extracted (Validated by Pydantic)]")
        print("-" * 50)
        print(extracted_data.model_dump_json(indent=2))
        
    except ValidationError as e:
        print(f"\n[ERROR] Pydantic Validation Failed: {e}")
        print(f"Raw model output: {response.text}")
    except Exception as e:
        print(f"An error occurred in Exercise 2: {e}")
        
    finally:
        # Cleanup uploaded file (Crucial for best practices)
        if uploaded_file:
            print(f"\n3. Cleaning up uploaded file: {uploaded_file.name}")
            client.files.delete(name=uploaded_file.name)


# --- Exercise 3: Comparative Analysis Across Multiple Uploaded Documents ---

def upload_remote_pdf_for_reuse(url: str, display_name: str) -> types.File:
    """Helper function to fetch and upload a remote PDF using the Files API."""
    print(f"   -> Uploading {display_name}...")
    doc_io = io.BytesIO(httpx.get(url).content)
    uploaded_file = client.files.upload(
        file=doc_io,
        config=dict(
            mime_type='application/pdf',
            display_name=display_name
        )
    )
    return uploaded_file

def exercise_3_multi_document_comparison(url1: str, url2: str) -> None:
    """Uploads two PDFs and asks Gemini to compare them."""
    print("\n" + "="*70)
    print("--- Exercise 3: Multi-Document Comparative Analysis (Files API) ---")
    print("="*70)
    file1 = None
    file2 = None
    
    try:
        # 1. Upload both documents
        print("1. Uploading two ArXiv papers via Files API:")
        file1 = upload_remote_pdf_for_reuse(url1, "ArXiv_Paper_1")
        file2 = upload_remote_pdf_for_reuse(url2, "ArXiv_Paper_2")
        print(f"   -> Files uploaded: {file1.name} and {file2.name}")

        # 2. Define the complex comparative prompt
        prompt = (
            "You have been provided two research papers. Analyze both documents and "
            "identify the three most significant differences in their proposed model "
            "architectures or core methodologies. Present your findings clearly in a "
            "Markdown table with columns for 'Feature', 'Paper 1 Approach', and 'Paper 2 Approach'."
        )

        # 3. Call generate_content with both file objects and the prompt
        print("\n2. Requesting cross-document comparison (gemini-2.5-flash)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[file1, file2, prompt]
        )
        
        print("\n[Comparative Analysis Table]")
        print("-" * 50)
        print(response.text)

    except Exception as e:
        print(f"An error occurred in Exercise 3: {e}")
        
    finally:
        # 4. Cleanup both uploaded files
        print("\n3. Cleaning up files...")
        if file1:
            client.files.delete(name=file1.name)
            print(f"   -> Cleaned up {file1.name}")
        if file2:
            client.files.delete(name=file2.name)
            print(f"   -> Cleaned up {file2.name}")


# --- Exercise 4: File Lifecycle Management and Cleanup ---

def exercise_4_file_lifecycle() -> None:
    """Demonstrates file upload, retrieval, and explicit deletion."""
    print("\n" + "="*70)
    print("--- Exercise 4: File Lifecycle Management and Cleanup ---")
    print("="*70)
    temp_file_path = pathlib.Path("temp_report_for_cleanup.txt")
    uploaded_file = None
    
    try:
        # 1. Create a temporary local file
        temp_file_path.write_text("This is a dummy report for testing file lifecycle management.")
        print(f"1. Created local temporary file: {temp_file_path.name}")

        # 2. Upload the file
        uploaded_file = client.files.upload(
            file=temp_file_path,
            config=dict(mime_type='text/plain')
        )
        print(f"2. File uploaded successfully. Name: {uploaded_file.name}")
        
        # 3. Retrieve file metadata (Verification)
        file_info = client.files.get(name=uploaded_file.name)
        print("\n3. [File Metadata Before Deletion]")
        print(f"   Status: {file_info.state}, URI: {file_info.uri}")

        # 4. Delete the file
        print(f"\n4. Deleting file: {uploaded_file.name}...")
        client.files.delete(name=uploaded_file.name)
        print("   -> File deletion successful.")

        # 5. Attempt to retrieve the file again (Final Validation)
        print("\n5. Attempting to retrieve deleted file for validation...")
        try:
            client.files.get(name=uploaded_file.name)
            print("   ERROR: File retrieval succeeded, deletion failed.")
        except NotFoundError:
            print("   Validation successful: File not found (NotFoundError), confirming successful deletion.")
            
    except Exception as e:
        print(f"An unexpected error occurred during Exercise 4: {e}")
        
    finally:
        # 6. Clean up the local temporary file
        if temp_file_path.exists():
            temp_file_path.unlink()
            print(f"\n6. Cleaned up local file: {temp_file_path.name}")


# --- Execute all Exercises ---

if __name__ == "__main__":
    
    # Run Exercise 1 (Inline)
    exercise_1_inline_summary(URL_EX1)

    # Run Exercise 2 (Structured Extraction + Files API)
    exercise_2_structured_extraction(URL_EX2)

    # Run Exercise 3 (Multi-Document Comparison + Files API)
    exercise_3_multi_document_comparison(URL_EX3_1, URL_EX3_2)
    
    # Run Exercise 4 (File Management)
    exercise_4_file_lifecycle()

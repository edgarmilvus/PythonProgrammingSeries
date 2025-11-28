
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
import pathlib
import io
from typing import List, Optional

# Third-party libraries
import httpx
from pydantic import BaseModel, Field, ValidationError

# Google GenAI SDK imports
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. CONFIGURATION AND SCHEMA DEFINITION ---

# Define the model to use and the PDF source URL
MODEL_NAME = "gemini-2.5-flash"
# Note: Using a public NASA flight plan PDF as a complex, multi-page document placeholder.
# In a real scenario, this would be a complex financial report.
PDF_URL = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
FILE_NAME = "A17_FlightPlan.pdf"

# Define the Pydantic schema for structured output validation.
# This represents the strict data model required by our financial system.
class FinancialMetric(BaseModel):
    """A single key financial metric."""
    metric_name: str = Field(description="The name of the financial metric (e.g., 'Total Revenue').")
    value: float = Field(description="The numerical value of the metric, converted to a standard float.")
    unit: str = Field(description="The unit of the value (e.g., 'Million USD', 'Billion EUR').")

class FinancialSummary(BaseModel):
    """The complete structured summary of the financial document."""
    company_name: str = Field(description="The name of the company derived from the document.")
    reporting_period: str = Field(description="The quarter or fiscal year this report covers.")
    key_metrics: List[FinancialMetric] = Field(description="A list of extracted key financial metrics.")


def wait_for_file_processing(client: genai.Client, file_resource: types.File) -> types.File:
    """
    Polls the Files API to wait for a file to finish processing.
    The Gemini API processes large files asynchronously.
    """
    print(f"Waiting for file {file_resource.name} to finish processing...")
    
    # Poll every 5 seconds, up to a maximum of 10 attempts (50 seconds total)
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            # Retrieve the current state of the file
            updated_file = client.files.get(name=file_resource.name)
            
            if updated_file.state == 'ACTIVE':
                print("File processing complete. State: ACTIVE.")
                return updated_file
            
            if updated_file.state == 'FAILED':
                raise APIError(f"File processing failed for {file_resource.name}.")

            print(f"Status: {updated_file.state}. Retrying in 5 seconds (Attempt {attempt + 1}/{max_attempts}).")
            time.sleep(5)
            
        except APIError as e:
            print(f"API Error during file status check: {e}")
            raise
            
    raise TimeoutError("File processing timed out after multiple attempts.")


def process_document_with_gemini(client: genai.Client, pdf_url: str, schema: BaseModel) -> Optional[FinancialSummary]:
    """
    Main function to handle PDF download, upload via Files API, processing, and cleanup.
    """
    uploaded_file = None
    
    try:
        # --- 2. FILE ACQUISITION AND UPLOAD (Files API) ---
        print(f"\n[Step 1] Downloading PDF from: {pdf_url}")
        
        # Use httpx to fetch the PDF bytes
        response = httpx.get(pdf_url, timeout=30)
        response.raise_for_status()
        
        # Create a file-like object (BytesIO) from the content
        doc_io = io.BytesIO(response.content)

        print("[Step 2] Uploading PDF using the Files API...")
        # Upload the file. The Files API handles large files efficiently.
        uploaded_file = client.files.upload(
            file=doc_io,
            config=dict(
                mime_type='application/pdf',
                display_name=FILE_NAME
            )
        )
        print(f"File uploaded successfully. Name: {uploaded_file.name}, URI: {uploaded_file.uri}")

        # --- 3. ASYNCHRONOUS PROCESSING WAIT ---
        # Wait for the file to be ready before calling generate_content
        ready_file = wait_for_file_processing(client, uploaded_file)

        # --- 4. STRUCTURED DATA EXTRACTION ---
        
        # Define the system instruction to guide the model's behavior
        system_instruction = (
            "You are an expert financial analyst. Your task is to accurately extract "
            "the requested financial data from the provided quarterly report PDF. "
            "Strictly adhere to the provided JSON schema for the output."
        )
        
        # Define the user prompt, referencing the document provided by the file URI
        user_prompt = (
            "Analyze the entire document. Identify the company name and the reporting period. "
            "Extract the following key metrics: 'Total Revenue', 'Net Income', and 'Total Assets'. "
            "Format the output strictly as JSON following the defined schema."
        )
        
        print("\n[Step 4] Generating structured content from the document...")
        
        # Configure the request for structured JSON output
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            system_instruction=system_instruction
        )
        
        # The contents list includes the uploaded file resource and the text prompt
        gemini_response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[ready_file, user_prompt], # Pass the file object and the prompt
            config=config
        )
        
        # --- 5. VALIDATION AND RETURN ---
        
        print("\n[Step 5] Received raw JSON response. Validating with Pydantic...")
        
        # The response text is a JSON string conforming to the schema
        raw_json = gemini_response.text
        
        # Parse the JSON string into the Pydantic model for validation
        validated_data = schema.model_validate_json(raw_json)
        
        print("--- Extraction Successful and Validated ---")
        print(f"Company: {validated_data.company_name}")
        print(f"Period: {validated_data.reporting_period}")
        print("Metrics:")
        for metric in validated_data.key_metrics:
            print(f"  - {metric.metric_name}: {metric.value} {metric.unit}")
            
        return validated_data

    except httpx.HTTPStatusError as e:
        print(f"Error downloading PDF: HTTP Status {e.response.status_code}")
    except (APIError, TimeoutError) as e:
        print(f"Gemini API or Processing Error: {e}")
    except ValidationError as e:
        print(f"Pydantic Validation Failed: The model output did not match the required schema.")
        print(f"Raw response was:\n{raw_json}")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        # --- 6. CLEANUP ---
        if uploaded_file:
            print(f"\n[Step 6] Deleting uploaded file: {uploaded_file.name}")
            client.files.delete(name=uploaded_file.name)
            print("Cleanup complete.")
            
        return None

if __name__ == "__main__":
    # Ensure the API key is set
    if "GEMINI_API_KEY" not in os.environ:
        print("CRITICAL: GEMINI_API_KEY environment variable not set.")
    else:
        # Initialize the client
        gemini_client = genai.Client()
        
        # Execute the process
        extracted_data = process_document_with_gemini(
            client=gemini_client,
            pdf_url=PDF_URL,
            schema=FinancialSummary
        )
        
        if extracted_data:
            print("\nFinal Pydantic Object:")
            print(extracted_data.model_dump_json(indent=2))



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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

import json
import time
import os
from google import genai
from google.genai import types
from pydantic import BaseModel

# --- 1. Define Structured Output Schema (Advanced Configuration Example) ---

class DocumentSummary(BaseModel):
    """Schema for summarizing a document."""
    title: str
    key_points: list[str]
    sentiment: str

# --- 2. Setup Client and Configuration ---

# Ensure GEMINI_API_KEY is set in your environment
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    # Exit or handle error if API key is missing

INPUT_FILE_NAME = "large_batch_requests.jsonl"
OUTPUT_FILE_NAME = "batch_results.jsonl"
BATCH_DISPLAY_NAME = "Comprehensive_Data_Analysis_Job"
MODEL_NAME = "gemini-2.5-flash"

# --- 3. Prepare the JSONL Input File (Large Batch Method) ---

def create_batch_input_file():
    """Generates a sample JSONL file for batch processing."""
    print(f"Creating sample input file: {INPUT_FILE_NAME}")
    
    # Define a list of requests. Each request must contain a unique 'key'
    # and the actual 'request' object (GenerateContentRequest structure).
    requests_data = [
        {
            "key": "doc-1001", 
            "request": {
                "contents": [{"parts": [{"text": "Summarize the key differences between synchronous and asynchronous programming."}]}],
                "config": {
                    # Example of structured output configuration for this specific request
                    'response_mime_type': 'application/json',
                    'response_schema': DocumentSummary
                }
            }
        },
        {
            "key": "doc-1002", 
            "request": {
                "contents": [{"parts": [{"text": "Write a short, critical review of the novel 'Moby Dick'."}]}],
                # No structured output config for this request
            }
        },
        {
            "key": "doc-1003", 
            "request": {
                "contents": [{"parts": [{"text": "Identify the capital of Japan and the main export of that country."}]}],
                "config": {
                    # Example of using a tool (Google Search) for a specific request
                    'tools': [{'google_search': {}}]
                }
            }
        }
    ]

    with open(INPUT_FILE_NAME, "w") as f:
        for req in requests_data:
            # Convert the request dictionary (including Pydantic schema) to JSON string
            f.write(json.dumps(req, default=str) + "\n")
    
    print(f"Input file created with {len(requests_data)} requests.")

# --- 4. Upload Input File to Gemini File API ---

def upload_input_file():
    """Uploads the local JSONL file to the Gemini File API."""
    try:
        uploaded_file = client.files.upload(
            file=INPUT_FILE_NAME,
            config=types.UploadFileConfig(display_name=BATCH_DISPLAY_NAME + "_Input", mime_type='application/jsonl')
        )
        print(f"Successfully uploaded file: {uploaded_file.name}")
        return uploaded_file
    except Exception as e:
        print(f"File upload failed: {e}")
        return None

# --- 5. Create the Asynchronous Batch Job ---

def create_batch_job(uploaded_file):
    """Submits the batch job using the uploaded file name."""
    print("Submitting batch job...")
    try:
        file_batch_job = client.batches.create(
            model=f"models/{MODEL_NAME}",
            # Source is the resource name (URI) of the uploaded file
            src=uploaded_file.name,
            config={
                'display_name': BATCH_DISPLAY_NAME,
            },
        )
        print(f"Created batch job: {file_batch_job.name}")
        return file_batch_job
    except Exception as e:
        print(f"Batch job creation failed: {e}")
        return None

# --- 6. Monitoring and Polling Mechanism ---

def poll_job_status(job_name):
    """Polls the Batch API until the job reaches a terminal state."""
    completed_states = set([
        'JOB_STATE_SUCCEEDED',
        'JOB_STATE_FAILED',
        'JOB_STATE_CANCELLED',
        'JOB_STATE_EXPIRED',
    ])
    
    print(f"\nStarting polling loop for job: {job_name}")
    
    while True:
        try:
            batch_job = client.batches.get(name=job_name)
            current_state = batch_job.state.name
            
            if current_state in completed_states:
                print(f"\nJob finished with state: {current_state}")
                return batch_job
            
            print(f"Job not finished. Current state: {current_state}. Waiting 30 seconds...")
            time.sleep(30) # Wait interval to respect polling limits
            
        except Exception as e:
            print(f"Error during polling: {e}")
            time.sleep(60) # Longer wait on error
            
# --- 7. Retrieval of Results (Downloading Output File) ---

def retrieve_and_process_results(final_batch_job, uploaded_file):
    """Downloads and processes the output JSONL file."""
    if final_batch_job.state.name != 'JOB_STATE_SUCCEEDED':
        print(f"Cannot retrieve results. Job state is {final_batch_job.state.name}.")
        if final_batch_job.error:
            print(f"Job Error Details: {final_batch_job.error}")
        return

    # The result file name is stored in the destination configuration
    result_file_name = final_batch_job.dest.file_name
    print(f"\nResults are available in File API resource: {result_file_name}")

    print("Downloading result file content...")
    try:
        # Download returns bytes, which we decode
        file_content_bytes = client.files.download(file=result_file_name)
        file_content_str = file_content_bytes.decode('utf-8')

        # Save the result locally for inspection
        with open(OUTPUT_FILE_NAME, "w") as f:
            f.write(file_content_str)
        
        print(f"Results saved to {OUTPUT_FILE_NAME}. Processing first 5 lines:")

        # Process the JSONL output line by line
        for i, line in enumerate(file_content_str.strip().split('\n')):
            if i >= 5: break
            
            result_obj = json.loads(line)
            
            # The output object contains the original 'key' and the 'response' or 'error'
            key = result_obj.get("key", "N/A")
            response = result_obj.get("response")
            error = result_obj.get("error")

            print(f"--- Result for Key: {key} ---")
            if response:
                # Attempt to parse the text content
                try:
                    # Note: For structured output, 'response.text' contains the raw JSON string
                    print(f"Text Snippet: {response['candidates'][0]['content']['parts'][0]['text'][:80]}...")
                except (KeyError, IndexError, TypeError):
                    print("Response structure complex or non-textual.")
            elif error:
                print(f"Request failed with error: {error.get('message', 'Unknown Error')}")
            
    except Exception as e:
        print(f"Error during result retrieval or processing: {e}")
    finally:
        # Clean up the uploaded input and output files from the File API
        print("\nCleaning up uploaded files...")
        client.files.delete(name=uploaded_file.name)
        client.files.delete(name=result_file_name)
        os.remove(INPUT_FILE_NAME)
        os.remove(OUTPUT_FILE_NAME)
        print("Cleanup complete.")

# --- 8. Execution Orchestration ---

if __name__ == '__main__':
    
    # 1. Create local file
    create_batch_input_file()
    
    # 2. Upload file
    uploaded_file_obj = upload_input_file()
    if not uploaded_file_obj:
        exit()
        
    # 3. Create the batch job
    batch_job_obj = create_batch_job(uploaded_file_obj)
    if not batch_job_obj:
        # Clean up the uploaded file if job submission failed
        client.files.delete(name=uploaded_file_obj.name)
        os.remove(INPUT_FILE_NAME)
        exit()
        
    # 4. Monitor job status
    final_job_status = poll_job_status(batch_job_obj.name)
    
    # 5. Retrieve results and clean up
    retrieve_and_process_results(final_job_status, uploaded_file_obj)


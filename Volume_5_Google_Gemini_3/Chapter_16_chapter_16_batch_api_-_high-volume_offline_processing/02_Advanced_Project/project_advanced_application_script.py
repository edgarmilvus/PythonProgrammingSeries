
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
import json
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError
from typing import List

# --- Configuration and Setup ---

# WARNING: This script handles file operations. Ensure the directory is writable.
# Ensure your GEMINI_API_KEY is set as an environment variable.

# Initialize the Gemini Client
try:
    client = genai.Client()
    print("Gemini Client initialized successfully.")
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

# Define the desired structured output schema using Pydantic
class OptimizedProduct(BaseModel):
    """
    Schema for the standardized product description and features.
    This ensures the model returns a predictable, parsable JSON object.
    """
    product_sku: str = Field(description="The unique SKU identifier for the product.")
    standardized_name: str = Field(description="A clean, title-cased product name.")
    seo_description: str = Field(description="A concise, SEO-optimized description, focused on benefits (max 160 characters).")
    key_features: List[str] = Field(description="3 to 5 critical, succinct selling points.")

# --- Step 1: Data Simulation and JSONL Preparation ---

def prepare_batch_input_file(num_requests: int = 50000) -> str:
    """
    Simulates a large dataset and creates the JSONL file required by the Batch API.
    Each line must contain a 'key' and a 'request' (GenerateContentRequest).
    """
    input_file_name = "large_product_batch_requests.jsonl"
    
    # Simulate raw product data (scaled down for this example, but structure holds)
    raw_products = [
        {"id": 1000 + i, 
         "name": f"Product Item {1000 + i}", 
         "desc": f"Old, long description for item {1000 + i}. It's a bit messy and needs optimization for search engines. This is in category {i % 5}."}
        for i in range(num_requests)
    ]

    print(f"\n1. Preparing {len(raw_products)} requests into {input_file_name}...")
    
    count = 0
    with open(input_file_name, "w") as f:
        for product in raw_products:
            # Construct the prompt for the model
            prompt = (
                f"You are an expert e-commerce copywriter. Rewrite the following raw product data "
                f"into a professional, SEO-friendly structured JSON object. "
                f"Raw Data: Name: {product['name']}, Description: {product['desc']}. "
                f"Ensure the SKU is {product['id']} and the description is brief and compelling."
            )
            
            # 1. Build the GenerateContentRequest structure
            request_body = {
                "contents": [
                    {"role": "user", "parts": [{"text": prompt}]}
                ],
                # 2. Inject Structured Output configuration directly into the request config
                "config": {
                    "response_mime_type": "application/json",
                    "response_schema": OptimizedProduct, 
                    "temperature": 0.2, # Use a low temperature for predictable, structured output
                }
            }
            
            # 3. Create the final JSONL line structure
            jsonl_line = {
                "key": f"sku-{product['id']}", # Unique identifier for tracking results
                "request": request_body
            }
            
            f.write(json.dumps(jsonl_line) + "\n")
            count += 1
            if count % 10000 == 0:
                print(f"   ... Wrote {count} lines.")
                
    print(f"Successfully created input file: {input_file_name}")
    return input_file_name


# --- Step 2: Upload Input File and Create Batch Job ---

def submit_batch_job(input_file_path: str) -> (types.BatchJob, types.File):
    """
    Uploads the JSONL file and submits the asynchronous batch generation job.
    """
    
    # A. Upload the file using the File API
    print("\n2. Uploading input file to File API...")
    uploaded_file = client.files.upload(
        file=input_file_path,
        config=types.UploadFileConfig(
            display_name='SEO_Product_Batch_Input', 
            mime_type='application/jsonl'
        )
    )
    print(f"   File uploaded successfully. Resource name: {uploaded_file.name}")
    
    # B. Create the batch job, referencing the uploaded file's resource name
    print("3. Submitting batch job...")
    batch_job = client.batches.create(
        model="gemini-2.5-flash", 
        src=uploaded_file.name, # Source is the uploaded file name
        config={
            'display_name': "E-commerce Product SEO Refinement Batch",
        },
    )
    
    print(f"   Batch job created: {batch_job.name}")
    print(f"   Current state: {batch_job.state.name}")
    
    return batch_job, uploaded_file

# --- Step 3: Monitor Job Status (Polling) ---

def wait_for_job_completion(job_name: str) -> types.BatchJob:
    """
    Polls the Batch API status until the job is completed, failed, or cancelled.
    """
    completed_states = set([
        'JOB_STATE_SUCCEEDED',
        'JOB_STATE_FAILED',
        'JOB_STATE_CANCELLED',
        'JOB_STATE_EXPIRED',
    ])
    
    poll_interval_seconds = 60 # Wait 60 seconds between checks
    
    print(f"\n4. Monitoring job status for {job_name}...")
    
    current_job = client.batches.get(name=job_name)
    
    while current_job.state.name not in completed_states:
        print(f"   Current state: {current_job.state.name}. Waiting {poll_interval_seconds} seconds...")
        time.sleep(poll_interval_seconds)
        current_job = client.batches.get(name=job_name)
        
    print(f"   Job finished with final state: {current_job.state.name}")
    
    if current_job.state.name == 'JOB_STATE_FAILED':
        print(f"   CRITICAL ERROR: Job failed. Details: {current_job.error}")
        raise RuntimeError("Batch job failed.")
        
    return current_job

# --- Step 4: Retrieve and Parse Results ---

def retrieve_and_parse_results(completed_job: types.BatchJob):
    """
    Downloads the output JSONL file and processes the structured results.
    """
    if not completed_job.dest or not completed_job.dest.file_name:
        print("Error: Job succeeded but no output file name found.")
        return
        
    result_file_name = completed_job.dest.file_name
    print(f"\n5. Retrieving results from output file: {result_file_name}")
    
    # A. Download the result file content (returns bytes)
    print("   Downloading content...")
    file_content_bytes = client.files.download(file=result_file_name)
    
    # B. Decode and process the JSONL content line by line
    decoded_content = file_content_bytes.decode('utf-8')
    processed_results = []
    failed_requests = 0
    
    print("   Parsing results...")
    
    for line in decoded_content.strip().split('\n'):
        if not line.strip():
            continue
            
        try:
            result = json.loads(line)
            request_key = result.get('key', 'N/A')
            
            # Check for successful generation response
            if 'response' in result and result['response'].get('candidates'):
                
                # The structured output is contained within the first part's text field
                raw_json_text = result['response']['candidates'][0]['content']['parts'][0]['text']
                
                # The model output is a JSON string; we must load it and validate against Pydantic
                model_output_data = json.loads(raw_json_text)
                
                # Use Pydantic to validate and standardize the data structure
                validated_data = OptimizedProduct.model_validate(model_output_data)
                
                processed_results.append({
                    "key": request_key,
                    "data": validated_data.model_dump()
                })
                
            elif 'error' in result:
                failed_requests += 1
                # print(f"   Request {request_key} failed: {result['error']}")
                
        except json.JSONDecodeError:
            print(f"   Parsing Error: Failed to decode JSON line: {line[:100]}...")
            failed_requests += 1
        except ValidationError as e:
            print(f"   Validation Error for key {request_key}: Structured output mismatch.")
            # print(e)
            failed_requests += 1
        except Exception as e:
            print(f"   Unexpected Error processing line: {e}")
            failed_requests += 1

    print("\n--- Final Summary ---")
    print(f"Total requests processed: {len(decoded_content.strip().split('\n'))}")
    print(f"Successful structured outputs: {len(processed_results)}")
    print(f"Failed or errored requests: {failed_requests}")
    
    # Display a sample of the results
    if processed_results:
        print("\n--- Sample Processed Output (First 2) ---")
        for i, res in enumerate(processed_results[:2]):
            print(f"[{res['key']}]")
            print(json.dumps(res['data'], indent=4))
        
    return result_file_name


# --- Step 5: Cleanup ---

def cleanup_files(local_input_file: str, uploaded_file_name: str, result_file_name: str):
    """
    Deletes the local temporary files and the uploaded files from the File API.
    """
    print("\n6. Cleaning up resources...")
    
    # Delete local files
    try:
        if os.path.exists(local_input_file):
            os.remove(local_input_file)
            print(f"   Deleted local input file: {local_input_file}")
    except Exception as e:
        print(f"   Warning: Could not delete local input file: {e}")

    # Delete uploaded files from Google's File API
    try:
        # The input file must be deleted manually
        client.files.delete(name=uploaded_file_name)
        print(f"   Deleted uploaded input file: {uploaded_file_name}")
    except Exception as e:
        print(f"   Warning: Could not delete uploaded input file: {e}")
        
    try:
        # The output file is also a file resource that should be cleaned up
        client.files.delete(name=result_file_name)
        print(f"   Deleted uploaded result file: {result_file_name}")
    except Exception as e:
        print(f"   Warning: Could not delete uploaded result file: {e}")
        
    print("Cleanup complete.")


# --- Main Execution ---

if __name__ == "__main__":
    # Note: For a real production run, set num_requests much higher (e.g., 50000)
    # We use a small number here for rapid testing and demonstration.
    NUM_TEST_REQUESTS = 5 
    
    input_file_path = None
    uploaded_file_resource_name = None
    result_file_resource_name = None
    
    try:
        # 1. Prepare Input
        input_file_path = prepare_batch_input_file(num_requests=NUM_TEST_REQUESTS)
        
        # 2. Submit Job
        batch_job, uploaded_file = submit_batch_job(input_file_path)
        uploaded_file_resource_name = uploaded_file.name
        
        # 3. Monitor and Wait
        completed_job = wait_for_job_completion(batch_job.name)
        
        # 4. Retrieve Results
        if completed_job.state.name == 'JOB_STATE_SUCCEEDED':
            result_file_resource_name = retrieve_and_parse_results(completed_job)
        else:
            print("Job did not succeed, skipping result retrieval.")
            
    except Exception as e:
        print(f"\nFATAL EXECUTION ERROR: {e}")
        
    finally:
        # 5. Cleanup
        if input_file_path and uploaded_file_resource_name and result_file_resource_name:
            cleanup_files(
                local_input_file=input_file_path, 
                uploaded_file_name=uploaded_file_resource_name, 
                result_file_name=result_file_resource_name
            )
        elif input_file_path and uploaded_file_resource_name:
             # Clean up the input file even if the job failed before generating an output file
             cleanup_files(
                local_input_file=input_file_path, 
                uploaded_file_name=uploaded_file_resource_name, 
                result_file_name="" # Placeholder, as it might not exist
            )
        elif input_file_path:
             if os.path.exists(input_file_path):
                os.remove(input_file_path)
                print(f"   Deleted local input file: {input_file_path} (Upload failed).")

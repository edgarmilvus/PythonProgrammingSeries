
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

import time
import json
from google import genai
from google.genai import types
from typing import List, Dict, Any

# --- Configuration ---
# Initialize the Gemini Client (API Key should be set in environment variables)
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Ensure GEMINI_API_KEY is set: {e}")
    exit()

MODEL_NAME = "models/gemini-2.5-flash"
POLLING_INTERVAL = 15 # Wait 15 seconds between status checks

# 1. Prepare the Input Data
# We simulate a list of product titles that need SEO descriptions.
product_titles: List[str] = [
    "Organic Fair Trade Coffee Beans (Ethiopian Yirgacheffe)",
    "Noise-Cancelling Wireless Headphones (ApexPro 500)",
    "Ergonomic Mesh Office Chair (Lumbar Support)",
    "Solar-Powered Smart Garden Kit (Indoor Herb Growing)"
]

# Structure the requests into the required format:
# A list of dictionaries, where each dictionary is a GenerateContentRequest object.
inline_requests: List[Dict[str, Any]] = []
for title in product_titles:
    prompt = (
        f"Write a concise, engaging SEO meta description (max 160 characters) "
        f"for the product: {title}. Focus on benefits and keywords."
    )
    
    # Define the structure for a single GenerateContentRequest
    request_payload = {
        'contents': [{
            'parts': [{'text': prompt}],
            'role': 'user'
        }],
        # Optional: Add generation configuration specific to this request
        'config': {
            'temperature': 0.5
        }
    }
    inline_requests.append(request_payload)

print(f"Prepared {len(inline_requests)} inline requests for batch processing.")

# 2. Submit the Batch Job
try:
    print("\n--- Step 1: Submitting Batch Job ---")
    
    # client.batches.create handles the submission.
    # 'src' takes the list of inline requests for small batches.
    batch_job = client.batches.create(
        model=MODEL_NAME,
        src=inline_requests, 
        config={
            'display_name': "product-seo-batch-job",
        },
    )
    job_name = batch_job.name
    print(f"Successfully created batch job: {job_name}")
    print(f"Initial State: {batch_job.state.name}")

    # 3. Implement Polling Mechanism
    # Define the states that signify job completion (success or failure)
    completed_states = set([
        'JOB_STATE_SUCCEEDED',
        'JOB_STATE_FAILED',
        'JOB_STATE_CANCELLED',
        'JOB_STATE_EXPIRED',
    ])

    print("\n--- Step 2: Monitoring Job Status (Polling) ---")
    
    # Loop until the job reaches a completed state
    while batch_job.state.name not in completed_states:
        print(f"Job is currently: {batch_job.state.name}. Waiting {POLLING_INTERVAL} seconds...")
        time.sleep(POLLING_INTERVAL)
        
        # Retrieve the updated job status using the job name
        batch_job = client.batches.get(name=job_name)

    print(f"\nJob finished with final state: {batch_job.state.name}")

    # 4. Retrieve and Process Results
    if batch_job.state.name == 'JOB_STATE_SUCCEEDED':
        print("\n--- Step 3: Retrieving Inline Results ---")

        # For inline jobs, results are stored in batch_job.dest.inlined_responses
        if batch_job.dest and batch_job.dest.inlined_responses:
            results = batch_job.dest.inlined_responses
            print(f"Successfully retrieved {len(results)} responses.")

            # Iterate through the results. Responses maintain the original order.
            print("\n--- Final Processed Output ---")
            for i, response_item in enumerate(results):
                original_title = product_titles[i] # Match by index
                
                print(f"--------------------------------------------------")
                print(f"Product: {original_title}")

                if response_item.response:
                    # Access the generated text content
                    seo_description = response_item.response.text.strip()
                    print(f"  > SEO Description:")
                    print(f"  {seo_description}")
                elif response_item.error:
                    # Handle individual request failures within the batch
                    print(f"  > ERROR processing request: {response_item.error}")
                else:
                    print("  > No generated content found for this request.")

        else:
            print("Job succeeded but no inline results were found. This is unexpected for inline jobs.")

    elif batch_job.state.name == 'JOB_STATE_FAILED':
        print(f"\nJob failed. Error details: {batch_job.error}")

except Exception as e:
    print(f"\nAn unexpected error occurred during the batch process: {e}")
    
# Clean up phase (not strictly needed for inline, but good practice for completeness)
print("\nBatch processing simulation complete.")

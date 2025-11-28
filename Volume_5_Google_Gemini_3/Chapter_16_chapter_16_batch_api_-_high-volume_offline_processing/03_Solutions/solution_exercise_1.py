
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
import json
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError, TypeAdapter

# --- Configuration and Setup ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    # Initialize the client. The client automatically picks up the API key 
    # from the GEMINI_API_KEY environment variable.
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    print("Please ensure your GEMINI_API_KEY is correctly configured.")
    # Exit gracefully if the client cannot be initialized
    exit()

# Define a set of states that indicate job completion
COMPLETED_STATES = {
    'JOB_STATE_SUCCEEDED',
    'JOB_STATE_FAILED',
    'JOB_STATE_CANCELLED',
    'JOB_STATE_EXPIRED',
}

# --- Pydantic Schema for Exercise 3 ---
class DocumentSummary(BaseModel):
    """Schema for structured summary extraction."""
    title: str
    keywords: list[str]
    summary_length_words: int # Added for robustness

# --- Helper Function for Polling ---
def poll_batch_job(job_name: str, client: genai.Client):
    """
    Polls the status of a batch job until it reaches a completed state.
    Returns the final job object.
    """
    print(f"\n--- Polling started for job: {job_name} ---")
    
    # Initial wait to allow job to start processing
    time.sleep(5) 
    
    while True:
        try:
            # Use client.batches.get to retrieve the current job status
            batch_job = client.batches.get(name=job_name)
            state_name = batch_job.state.name
            
            if state_name in COMPLETED_STATES:
                print(f"Polling complete. Final state: {state_name}")
                if state_name == 'JOB_STATE_FAILED':
                    print(f"Job failed with error: {batch_job.error}")
                return batch_job
            
            print(f"Job state: {state_name}. Waiting 15 seconds...")
            time.sleep(15) # Polling interval adjusted to 15s as per Exercise 1 requirement
            
        except Exception as e:
            print(f"An error occurred during polling: {e}")
            return None

# ======================================================================
# Exercise 1: Quick Inline Batch Processing and Retrieval
# ======================================================================
print("\n[EXERCISE 1] Starting Quick Inline Batch Processing...")

# 1. Define a list of five simple requests (GenerateContentRequest dictionaries)
inline_requests_e1 = [
    {
        'contents': [{'parts': [{'text': 'Define the concept of "middleware" in web development.'}], 'role': 'user'}]
    },
    {
        'contents': [{'parts': [{'text': 'Explain the difference between synchronous and asynchronous processing.'}], 'role': 'user'}]
    },
    {
        'contents': [{'parts': [{'text': 'What is the primary function of a Vector Store/Database?'}], 'role': 'user'}]
    },
    {
        'contents': [{'parts': [{'text': 'What is the capital of Australia?'}], 'role': 'user'}]
    },
    {
        'contents': [{'parts': [{'text': 'Write a one-sentence summary of the plot of Moby Dick.'}], 'role': 'user'}]
    },
]

try:
    # 2. Use client.batches.create with the list of dictionaries as the source
    inline_batch_job = client.batches.create(
        model="models/gemini-2.5-flash",
        src=inline_requests_e1,
        config={'display_name': "Inline-CS-Concepts-Job"},
    )
    print(f"Created inline batch job: {inline_batch_job.name}")

    # 3. Implement polling loop
    final_job_e1 = poll_batch_job(inline_batch_job.name, client)

    if final_job_e1 and final_job_e1.state.name == 'JOB_STATE_SUCCEEDED':
        print("\n--- Exercise 1 Results (Inline Retrieval) ---")
        
        # 4. Iterate through the inlined_responses
        if final_job_e1.dest and final_job_e1.dest.inlined_responses:
            for i, inline_response in enumerate(final_job_e1.dest.inlined_responses):
                print(f"\nRequest {i+1} Response:")
                if inline_response.response:
                    # Accessing the generated text
                    print(inline_response.response.text.strip())
                elif inline_response.error:
                    print(f"Error in request {i+1}: {inline_response.error}")
        else:
            print("Job succeeded but no inline responses found.")
    else:
        print("Exercise 1 job failed or was cancelled.")

# ======================================================================
# Exercise 2: High-Volume JSONL Workflow and File Cleanup
# ======================================================================
print("\n\n[EXERCISE 2] Starting File-Based Batch Processing...")
INPUT_FILE_E2 = "data_labeling_requests_e2.jsonl"

# 1. Create the sample JSONL input file (20 entries)
print(f"Creating JSONL file: {INPUT_FILE_E2}")
reviews = [
    "The product arrived late and was broken. I am extremely disappointed.",
    "The quality is fantastic for the price. Highly recommend!",
    "It works, but the instructions were impossible to follow.",
    "Neutral experience. Nothing special, but it gets the job done.",
    "Five stars! Best purchase this year.",
] * 4 # 20 total requests

data_requests_e2 = [
    {"key": f"review-{i+1}", 
     "request": {
         "contents": [{"parts": [{"text": f"Classify the sentiment (Positive, Negative, or Neutral) of this customer review: '{reviews[i]}'"}]}]
     }}
    for i in range(20)
]

with open(INPUT_FILE_E2, "w") as f:
    for req in data_requests_e2:
        f.write(json.dumps(req) + "\n")

uploaded_file_e2 = None
batch_job_e2 = None
output_file_e2_name = None

try:
    # 2. Upload the JSONL file
    uploaded_file_e2 = client.files.upload(
        file=INPUT_FILE_E2,
        config=types.UploadFileConfig(display_name='20-Review-Batch-Input', mime_type='jsonl')
    )
    print(f"Uploaded input file: {uploaded_file_e2.name}")

    # 3. Create the batch job using the uploaded file's name as the source
    batch_job_e2 = client.batches.create(
        model="gemini-2.5-flash",
        src=uploaded_file_e2.name,
        config={'display_name': "File-Review-Classification-Job"},
    )
    print(f"Created file batch job: {batch_job_e2.name}")

    # 4. Implement robust polling
    final_job_e2 = poll_batch_job(batch_job_e2.name, client)

    if final_job_e2 and final_job_e2.state.name == 'JOB_STATE_SUCCEEDED':
        # 5. Retrieve the output file name
        output_file_e2_name = final_job_e2.dest.file_name
        print(f"\nResults available in file: {output_file_e2_name}")

        # 6. Download the resulting JSONL file content
        print("Downloading result file content...")
        result_content_e2 = client.files.download(file=output_file_e2_name)
        
        print("\n--- Exercise 2 Results (File Content Preview) ---")
        # Decode and print a preview of the JSONL output
        decoded_content = result_content_e2.decode('utf-8').strip().split('\n')
        
        for i, line in enumerate(decoded_content[:5]):
            parsed_line = json.loads(line)
            key = parsed_line.get('key', 'N/A')
            # Navigate the complex response structure to find the text
            response_text = parsed_line.get('response', {}).get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No text found.')
            print(f"Key: {key} | Classification: {response_text.strip()}")

    else:
        print("Exercise 2 job failed or was cancelled.")

finally:
    # 7. Crucial Cleanup: Delete both input and output files from File API
    print("\n--- Cleaning up files from File API ---")
    if uploaded_file_e2:
        client.files.delete(file=uploaded_file_e2.name)
        print(f"Deleted input file: {uploaded_file_e2.name}")
    if output_file_e2_name:
        client.files.delete(file=output_file_e2_name)
        print(f"Deleted output file: {output_file_e2_name}")
    if os.path.exists(INPUT_FILE_E2):
        os.remove(INPUT_FILE_E2)
        print(f"Deleted local file: {INPUT_FILE_E2}")

# ======================================================================
# Exercise 3: Advanced Challenge: Structured Output in Batch Jobs
# ======================================================================
print("\n\n[EXERCISE 3] Starting Structured Output Batch Challenge...")
INPUT_FILE_E3 = "structured_summary_requests_e3.jsonl"

# 1. Prepare the Response Schema for JSONL injection
# Use TypeAdapter to get the schema dictionary compatible with the API's config structure
schema_adapter = TypeAdapter(list[DocumentSummary])
response_schema_config = schema_adapter.json_schema()

# 2. Modify the JSONL creation process to include structured config
data_requests_e3 = []
document_titles = [
    "The Future of Renewable Energy Storage",
    "Understanding the Global Supply Chain Crisis",
    "A Guide to Modern Cryptography Algorithms",
    "Impact of AI on Healthcare Diagnostics",
] * 5 # 20 total requests

print(f"Creating structured JSONL file: {INPUT_FILE_E3}")
for i, title in enumerate(document_titles):
    request_body = {
        "contents": [{"parts": [{"text": f"Extract a summary, title, and keywords from a document titled: '{title}'"}], "role": "user"}],
        "config": {
            'response_mime_type': 'application/json',
            'response_schema': response_schema_config
        }
    }
    data_requests_e3.append({"key": f"doc-{i+1}", "request": request_body})

with open(INPUT_FILE_E3, "w") as f:
    for req in data_requests_e3:
        f.write(json.dumps(req) + "\n")

uploaded_file_e3 = None
output_file_e3_name = None

try:
    # Upload, create job, and poll (similar to Ex 2)
    uploaded_file_e3 = client.files.upload(
        file=INPUT_FILE_E3,
        config=types.UploadFileConfig(display_name='Structured-Summary-Input', mime_type='jsonl')
    )
    print(f"Uploaded input file: {uploaded_file_e3.name}")

    batch_job_e3 = client.batches.create(
        model="gemini-2.5-flash",
        src=uploaded_file_e3.name,
        config={'display_name': "Structured-Output-Job"},
    )
    print(f"Created structured batch job: {batch_job_e3.name}")

    final_job_e3 = poll_batch_job(batch_job_e3.name, client)

    if final_job_e3 and final_job_e3.state.name == 'JOB_STATE_SUCCEEDED':
        # 4. Download the result file
        result_file_name_e3 = final_job_e3.dest.file_name
        print(f"\nResults available in file: {result_file_name_e3}")
        result_content_e3 = client.files.download(file=result_file_name_e3)
        output_file_e3_name = result_file_name_e3
        
        # 5. Parsing Challenge: Load and validate results
        print("\n--- Exercise 3 Results (Structured Parsing) ---")
        decoded_content_e3 = result_content_e3.decode('utf-8').strip().split('\n')
        
        for i, line in enumerate(decoded_content_e3[:3]): # Check first 3 results
            parsed_line = json.loads(line)
            key = parsed_line.get('key', 'N/A')
            
            if parsed_line.get('response'):
                # The structured output is contained within the text field as a JSON string
                try:
                    json_text = parsed_line['response']['candidates'][0]['content']['parts'][0]['text']
                    
                    # Validate against the Pydantic model
                    validated_data = schema_adapter.validate_json(json_text)
                    
                    # Since the schema is list[DocumentSummary], we access the first item
                    summary: DocumentSummary = validated_data[0]
                    
                    print(f"Key: {key} | Status: SUCCESS")
                    print(f"  Title: {summary.title}")
                    print(f"  Keywords Count: {len(summary.keywords)}")
                    
                except (json.JSONDecodeError, ValidationError) as ve:
                    print(f"Key: {key} | Status: PARSING FAILED (Error: {type(ve).__name__})")
            else:
                print(f"Key: {key} | Status: NO RESPONSE or ERROR in model generation.")

    else:
        print("Exercise 3 job failed or was cancelled.")

finally:
    # Cleanup
    print("\n--- Cleaning up files from File API (Exercise 3) ---")
    if uploaded_file_e3:
        client.files.delete(file=uploaded_file_e3.name)
        print(f"Deleted input file: {uploaded_file_e3.name}")
    if output_file_e3_name:
        client.files.delete(file=output_file_e3_name)
        print(f"Deleted output file: {output_file_e3_name}")
    if os.path.exists(INPUT_FILE_E3):
        os.remove(INPUT_FILE_E3)
        print(f"Deleted local file: {INPUT_FILE_E3}")


# ======================================================================
# Exercise 4: High-Throughput Batch Embeddings
# ======================================================================
print("\n\n[EXERCISE 4] Starting Batch Embeddings Job...")

# 1. Define a list of 10 short text snippets
texts_to_embed = [
    f"Snippet {i+1}: The theory of general relativity and space-time curvature.",
    f"Snippet {i+2}: Python programming language fundamentals and common data structures.",
    f"Snippet {i+3}: The history of the Roman Empire, from republic to collapse.",
    f"Snippet {i+4}: Modern techniques in deep learning, focusing on transformer architectures.",
    f"Snippet {i+5}: Recipes for sourdough bread and fermentation science.",
    f"Snippet {i+6}: A brief overview of the Kubernetes orchestration system.",
    f"Snippet {i+7}: The principles of object-oriented programming.",
    f"Snippet {i+8}: Famous quotes from Albert Einstein.",
    f"Snippet {i+9}: Explanation of the Doppler effect.",
    f"Snippet {i+10}: Summary of the latest climate change reports.",
]

# The structure for embedding requests requires the 'text' key
inline_embed_requests = [
    {'text': t} for t in texts_to_embed
]

try:
    # 2. Use the dedicated client.batches.create_embeddings method
    embed_batch_job = client.batches.create_embeddings(
        model="gemini-embedding-001",
        # Use the src structure for inline requests as specified in the docs
        src={'inlined_requests': inline_embed_requests},
        config={'display_name': "Inline-Embedding-Job"},
    )
    print(f"Created embedding batch job: {embed_batch_job.name}")

    # 3. Poll the job status
    final_job_e4 = poll_batch_job(embed_batch_job.name, client)

    if final_job_e4 and final_job_e4.state.name == 'JOB_STATE_SUCCEEDED':
        print("\n--- Exercise 4 Results (Inline Embeddings Retrieval) ---")
        
        # 4. Retrieve the results using inlined_embed_content_responses
        if final_job_e4.dest and final_job_e4.dest.inlined_embed_content_responses:
            responses = final_job_e4.dest.inlined_embed_content_responses
            print(f"Successfully generated {len(responses)} embeddings.")
            
            # 5. Print the first few dimensions of the first generated embedding vector
            first_response = responses[0]
            if first_response.response and first_response.response.embedding:
                vector = first_response.response.embedding.values
                print(f"First text: '{texts_to_embed[0]}'")
                print(f"Vector dimensions: {len(vector)}")
                print(f"First 5 vector values: {vector[:5]}...")
            else:
                print("Embedding response structure not found.")
        else:
            print("Job succeeded but no inline embedding responses found.")
    else:
        print("Exercise 4 job failed or was cancelled.")

except Exception as e:
    print(f"\nAn unexpected error occurred during Exercise 4: {e}")

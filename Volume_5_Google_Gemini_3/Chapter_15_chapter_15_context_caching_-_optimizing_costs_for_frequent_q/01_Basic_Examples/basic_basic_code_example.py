
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
import io
import httpx
import time
from google import genai
from google.genai import types

# --- 1. Configuration and Client Setup ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    # The genai.Client() automatically looks for the GEMINI_API_KEY
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Check API key and environment setup: {e}")
    # Exit gracefully if the client cannot be initialized
    exit()

# Define the model to use. Explicit caching requires an explicit version suffix.
MODEL_NAME = "gemini-2.0-flash-001" 

# --- 2. Define and Upload the Long Context (The PDF Document) ---
# We use a lengthy PDF (Apollo 17 Flight Plan) to simulate a large, static document.
LONG_CONTEXT_URL = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

print(f"1. Fetching foundation document from {LONG_CONTEXT_URL}...")

try:
    # Retrieve the document content as bytes using httpx
    response = httpx.get(LONG_CONTEXT_URL)
    response.raise_for_status() # Ensure the request was successful
    doc_io = io.BytesIO(response.content) # Wrap content in an in-memory file object
except httpx.RequestError as e:
    print(f"Error fetching document: {e}")
    exit()

# Upload the document using the Files API. 
# This is mandatory for large media and documents that form the context.
print("2. Uploading document to Gemini Files API for processing...")
document_file = client.files.upload(
  file=doc_io,
  config=dict(mime_type='application/pdf')
)
print(f"   -> Document uploaded successfully. File Name: {document_file.name}")

# Wait for the file to finish processing. Processing time depends on file size.
while document_file.state.name == 'PROCESSING':
    print('   -> Waiting for file processing...')
    time.sleep(2)
    document_file = client.files.get(name=document_file.name)

# --- 3. Create the Explicit Context Cache ---

# Define the static system instruction that will always accompany the document
STATIC_SYSTEM_INSTRUCTION = (
    "You are an expert space historian and mission analyst. "
    "Your task is to answer user questions strictly based on the provided Apollo 17 flight plan document. "
    "Be concise and cite relevant mission phases if possible."
)

CACHE_TTL = "3600s" # Set the cache Time-To-Live to 1 hour (3600 seconds)
CACHE_DISPLAY_NAME = "Apollo 17 Flight Plan Cache"

print("\n3. Creating explicit cache object...")
try:
    # The cache creation handles the tokenization and storage of the large context
    cache = client.caches.create(
        model=MODEL_NAME,
        config=types.CreateCachedContentConfig(
          display_name=CACHE_DISPLAY_NAME,
          system_instruction=STATIC_SYSTEM_INSTRUCTION,
          contents=[document_file], # Reference the uploaded file object
          ttl=CACHE_TTL,
      )
    )
    print(f"   -> Cache created successfully. Cache Name: {cache.name}")
    
    # The initial token count reflects the size of the document + system instruction
    initial_tokens = cache.usage_metadata.cached_content_token_count
    print(f"   -> Cached Tokens (Initial Cost/Storage): {initial_tokens} tokens")
    
except Exception as e:
    print(f"Error creating cache: {e}")
    # Crucial cleanup step if cache creation fails
    client.files.delete(name=document_file.name)
    exit()


# --- 4. Query 1: Using the Cache for the First Time (Observe Cost Shift) ---

USER_QUERY_1 = "What is the scheduled time for the Lunar Module (LM) landing (PDI)?"

print(f"\n4. Running Query 1 (Using Cache): '{USER_QUERY_1}'")

# We pass the cache reference via the GenerateContentConfig
response_1 = client.models.generate_content(
  model=MODEL_NAME,
  contents=USER_QUERY_1,
  config=types.GenerateContentConfig(
    cached_content=cache.name # This instructs the model to prepend the cached context
  )
)

print("\n--- Query 1 Results ---")
print(f"Response: {response_1.text[:300]}...")

# Analyze usage metadata to confirm cache hit and token breakdown
usage_1 = response_1.usage_metadata
print("\n--- Usage Metadata (Query 1) ---")
print(f"Prompt Tokens (User Query Only): {usage_1.prompt_token_count} (Low)")
print(f"Cached Content Tokens (The Context): {usage_1.cached_content_token_count} (High)")
print(f"Total Tokens Used: {usage_1.total_token_count}")


# --- 5. Query 2: Reuse the Cache (Demonstrate Operational Cost Reduction) ---

USER_QUERY_2 = "List the names of the crew members mentioned in the flight plan."

print(f"\n5. Running Query 2 (Reusing Cache): '{USER_QUERY_2}'")

# The second query uses the exact same large context without resending it.
response_2 = client.models.generate_content(
  model=MODEL_NAME,
  contents=USER_QUERY_2,
  config=types.GenerateContentConfig(
    cached_content=cache.name # Reuse the same cache reference
  )
)

print("\n--- Query 2 Results ---")
print(f"Response: {response_2.text[:300]}...")

# Analyze usage metadata again—the cached token count remains high, but the billing 
# rate for these tokens is significantly reduced compared to standard input tokens.
usage_2 = response_2.usage_metadata
print("\n--- Usage Metadata (Query 2) ---")
print(f"Prompt Tokens (User Query Only): {usage_2.prompt_token_count} (Low)")
print(f"Cached Content Tokens (The Context): {usage_2.cached_content_token_count} (High, matching Query 1)")
print(f"Total Tokens Used: {usage_2.total_token_count}")


# --- 6. Cleanup: Essential Resource Management ---

print("\n6. Deleting the cache and the underlying uploaded file.")
# Delete the cache object
client.caches.delete(cache.name)
# Delete the file object used to create the cache
client.files.delete(document_file.name)
print("Cleanup complete. Resources released.")


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

# Source File: theory_theoretical_foundations_part2.py
# Description: Theoretical Foundations
# ==========================================

import os
import datetime
from google import genai
from google.genai import types

# --- Configuration and Setup ---
# Initialize the client (assumes GEMINI_API_KEY is set in environment)
client = genai.Client()

# Define the model and context
MODEL_NAME = "models/gemini-2.0-flash-001"
# Placeholder for a large, pre-uploaded file object (e.g., a PDF)
# In a real scenario, this 'file_object' would be obtained from client.files.upload()
# We simulate a file object with a placeholder name for demonstration.
# FILE_OBJECT_NAME = 'files/example-document-12345'
# file_object = client.files.get(name=FILE_OBJECT_NAME)
# For conceptual purposes, we use a simple placeholder structure:
class MockFileObject:
    def __init__(self, name):
        self.name = name
        self.uri = f"gs://ai-data/{name}"
        self.state = type('State', (object,), {'name': 'ACTIVE'})
file_object = MockFileObject(name='files/sherlock-jr-video-12345')


# 1. CREATE THE EXPLICIT CACHE
def create_context_cache(client, model, file_ref):
    """Creates a cache with a specific TTL."""
    print("--- 1. Creating Cache ---")
    
    # Define the static, expensive context
    system_instruction_context = (
        'You are an expert financial analyst. Your job is to summarize '
        'and interpret the attached Q3 earnings report, focusing only on '
        'revenue growth and margin changes. Be concise.'
    )
    
    # Set TTL for 10 minutes (600 seconds)
    try:
        cache = client.caches.create(
            model=model,
            config=types.CreateCachedContentConfig(
                display_name='Q3 Earnings Report Cache',
                system_instruction=system_instruction_context,
                contents=[file_ref], # Reference to the pre-uploaded document/video
                ttl="600s", 
            )
        )
        print(f"Cache created successfully. Name: {cache.name}")
        print(f"Cache expires at: {cache.expire_time}")
        return cache
    except Exception as e:
        print(f"Error creating cache: {e}")
        return None

# 2. UTILIZE THE CACHE FOR FREQUENT QUERIES
def query_with_cache(client, model, cache_name, query):
    """Generates content using the cached context."""
    print(f"\n--- 2. Querying with Cache: {cache_name} ---")
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=query, # Short, dynamic query
            config=types.GenerateContentConfig(
                cached_content=cache_name # Reference to the stored context
            )
        )
        print(f"Query: '{query}'")
        print(f"Response Snippet: {response.text[:100]}...")
        
        # Displaying the token usage metadata is key to verifying efficiency
        print("\nUsage Metadata (Cost Verification):")
        print(f"  Prompt Tokens (new query cost): {response.usage_metadata.prompt_token_count}")
        print(f"  Cached Content Tokens (retrieved context): {response.usage_metadata.cached_content_token_count}")
        print(f"  Total Tokens: {response.usage_metadata.total_token_count}")
        return response
    except Exception as e:
        print(f"Error querying model: {e}")
        return None

# 3. UPDATE THE CACHE DURATION (TTL)
def update_cache_ttl(client, cache_name, minutes):
    """Extends the cache TTL."""
    print(f"\n--- 3. Updating Cache TTL to {minutes} minutes ---")
    
    # We update the TTL to 5 minutes (300 seconds)
    try:
        updated_cache = client.caches.update(
            name = cache_name,
            config  = types.UpdateCachedContentConfig(
                ttl=f'{minutes * 60}s'
            )
        )
        print(f"Cache updated. New expiry time: {updated_cache.expire_time}")
    except Exception as e:
        print(f"Error updating cache: {e}")

# 4. DELETE THE CACHE
def delete_context_cache(client, cache_name):
    """Deletes the cache to stop storage billing."""
    print(f"\n--- 4. Deleting Cache: {cache_name} ---")
    try:
        client.caches.delete(cache_name)
        print(f"Cache {cache_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting cache: {e}")

# --- Execution Flow ---
cache_obj = create_context_cache(client, MODEL_NAME, file_object)

if cache_obj:
    # First query (high savings achieved immediately)
    query_with_cache(
        client, 
        MODEL_NAME, 
        cache_obj.name, 
        "What was the overall net margin percentage change compared to last year?"
    )
    
    # Second query (demonstrates repeated cost saving)
    query_with_cache(
        client, 
        MODEL_NAME, 
        cache_obj.name, 
        "List the three key factors driving the revenue growth."
    )

    # Update the cache duration
    update_cache_ttl(client, cache_obj.name, 5) # Set to 5 minutes

    # Clean up
    delete_context_cache(client, cache_obj.name)


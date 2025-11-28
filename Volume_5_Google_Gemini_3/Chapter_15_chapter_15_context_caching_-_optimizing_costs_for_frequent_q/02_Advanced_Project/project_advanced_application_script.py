
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
import io
import time
import datetime
from contextlib import contextmanager

from google import genai
from google.genai import types
from google.genai.errors import APIError

# External libraries for file handling
import httpx

# --- Configuration ---
# Use a model known to support explicit caching
MODEL_NAME = "gemini-2.0-flash-001"
# A large, publicly accessible PDF (NASA Flight Plan used here as a proxy for a regulatory document)
LONG_CONTEXT_PDF_URL = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# --- Context Manager for Resource Cleanup ---

@contextmanager
def cleanup_resources(client, file_name=None, cache_name=None):
    """
    A Pythonic context manager to ensure resources (files and caches) 
    are deleted even if an error occurs during the main process.
    """
    try:
        # Yield control back to the main block
        yield
    finally:
        print("\n--- Starting Resource Cleanup ---")
        
        # 1. Delete the Cache
        if cache_name:
            try:
                client.caches.delete(cache_name)
                print(f"✅ Successfully deleted cache: {cache_name}")
            except APIError as e:
                print(f"⚠️ Could not delete cache {cache_name}. It may have expired or been deleted already. Error: {e}")

        # 2. Delete the File
        if file_name:
            try:
                client.files.delete(file_name)
                print(f"✅ Successfully deleted uploaded file: {file_name}")
            except APIError as e:
                print(f"⚠️ Could not delete file {file_name}. Error: {e}")

# --- Main Application Logic ---

def run_compliance_manager():
    """
    Main function to demonstrate explicit context caching for regulatory analysis.
    """
    # Initialize the client. Assumes GEMINI_API_KEY is set in environment.
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini Client: {e}")
        print("Please ensure your GEMINI_API_KEY is configured.")
        return

    uploaded_document = None
    regulatory_cache = None

    # Use the context manager to guarantee cleanup
    with cleanup_resources(client, file_name=None, cache_name=None) as manager_data:
        
        print(f"--- 1. Context Ingestion: Downloading and Uploading PDF ---")
        
        # Retrieve the PDF content into an in-memory buffer
        print(f"Downloading PDF from: {LONG_CONTEXT_PDF_URL}")
        try:
            response = httpx.get(LONG_CONTEXT_PDF_URL, timeout=30.0)
            response.raise_for_status() # Raise exception for bad status codes
            doc_io = io.BytesIO(response.content)
        except httpx.HTTPStatusError as e:
            print(f"Error retrieving PDF: {e}")
            return
        
        # Upload the document using the Files API
        print("Uploading document to Gemini Files API...")
        uploaded_document = client.files.upload(
            file=doc_io,
            config=dict(mime_type='application/pdf')
        )
        print(f"File uploaded successfully. Name: {uploaded_document.name}")
        
        # Update the context manager with the file name for cleanup
        manager_data.file_name = uploaded_document.name


        print("\n--- 2. Cache Creation: Tokenizing and Storing Context ---")
        
        # Define the static, large context
        compliance_system_instruction = (
            "You are a Senior Regulatory Compliance Analyst specializing in space law and "
            "NASA protocols. Your primary source of truth is the provided Flight Plan document. "
            "You must strictly answer user queries based only on the content of the document. "
            "If the answer is not found, state that the information is outside the scope of the document."
        )
        
        # Create a cached content object with a 1-hour Time-To-Live (TTL)
        # The TTL ensures the cache doesn't persist indefinitely if not needed.
        TTL_SECONDS = "3600s" # 1 hour
        
        regulatory_cache = client.caches.create(
            model=MODEL_NAME,
            config=types.CreateCachedContentConfig(
                display_name='FinTech Regulatory Manual V1.0',
                system_instruction=compliance_system_instruction,
                contents=[uploaded_document],
                ttl=TTL_SECONDS,
            )
        )

        print(f"Cache created successfully. Name: {regulatory_cache.name}")
        print(f"Cache expiration time: {regulatory_cache.expire_time}")
        print(f"Initial cache token count (approx.): {regulatory_cache.usage_metadata.cached_content_token_count}")
        
        # Update the context manager with the cache name for cleanup
        manager_data.cache_name = regulatory_cache.name


        print("\n--- 3. Query 1 (First Run): Demonstrating Cache Usage ---")
        
        # Query 1: A general summary request
        query_1 = "Provide a high-level summary of the mission objectives and the expected duration of the primary activities."
        
        start_time_1 = time.time()
        response_1 = client.models.generate_content(
            model=MODEL_NAME,
            contents=query_1,
            config=types.GenerateContentConfig(
                cached_content=regulatory_cache.name
            )
        )
        end_time_1 = time.time()
        
        print(f"Response 1 Time: {end_time_1 - start_time_1:.2f} seconds")
        print(f"Query 1: {query_1[:50]}...")
        print(f"Response 1 Token Usage Metadata:")
        print(response_1.usage_metadata)
        
        # Note the cache savings:
        cached_tokens = response_1.usage_metadata.cached_content_token_count
        prompt_tokens = response_1.usage_metadata.prompt_token_count
        print(f"Tokens saved by caching: {cached_tokens} (These are billed at a significantly reduced rate)")
        print(f"Total tokens processed (including cache): {prompt_tokens}")
        print(f"\n--- Response Snippet 1 ---\n{response_1.text[:300]}...\n")


        print("\n--- 4. Query 2 (Subsequent Run): Verifying Continued Savings ---")
        
        # Query 2: A specific, deep-dive compliance check
        query_2 = "According to the plan, what are the specific procedures regarding the deployment of the Lunar Roving Vehicle (LRV) and what is the maximum planned distance it will travel?"
        
        start_time_2 = time.time()
        response_2 = client.models.generate_content(
            model=MODEL_NAME,
            contents=query_2,
            config=types.GenerateContentConfig(
                cached_content=regulatory_cache.name
            )
        )
        end_time_2 = time.time()
        
        print(f"Response 2 Time: {end_time_2 - start_time_2:.2f} seconds")
        print(f"Query 2: {query_2[:50]}...")
        print(f"Response 2 Token Usage Metadata:")
        print(response_2.usage_metadata)
        
        # The cached_content_token_count should remain consistent and high, 
        # confirming the large context was not re-sent.
        print(f"Tokens saved by caching (consistent): {response_2.usage_metadata.cached_content_token_count}")
        print(f"\n--- Response Snippet 2 ---\n{response_2.text[:300]}...\n")


        print("\n--- 5. Cache Management: Listing All Caches ---")
        
        # List all caches associated with the project for auditing
        print("Retrieving metadata for active caches:")
        cache_list = list(client.caches.list())
        
        if cache_list:
            for cache in cache_list:
                # Filter for the cache we just created based on display name
                if cache.display_name == 'FinTech Regulatory Manual V1.0':
                    print(f"Found our cache: {cache.display_name}")
                    print(f"  Model: {cache.model}")
                    print(f"  Created: {cache.create_time}")
                    print(f"  Expires: {cache.expire_time}")
                    print(f"  Cached Tokens: {cache.usage_metadata.cached_content_token_count}")
        else:
            print("No active caches found.")

    # The cleanup_resources context manager automatically executes here
    print("\nScript execution finished.")

if __name__ == "__main__":
    run_compliance_manager()

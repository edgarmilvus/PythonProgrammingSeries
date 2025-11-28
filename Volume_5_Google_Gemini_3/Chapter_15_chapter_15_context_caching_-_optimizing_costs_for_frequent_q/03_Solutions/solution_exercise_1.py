
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
import time
import datetime
import io
import httpx
from google import genai
from google.genai import types
from google.genai.errors import NotFoundError, AlreadyExistsError

# --- Configuration ---
# Use a model known to support explicit caching
MODEL_NAME = "models/gemini-2.0-flash-001" 
# Ensure API key is set
if 'GEMINI_API_KEY' not in os.environ:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

client = genai.Client()

# Helper function for cleanup
def cleanup_cache(cache_name):
    """Attempts to delete a cache if it exists."""
    try:
        client.caches.delete(cache_name)
        print(f"\n[Cleanup] Successfully deleted cache: {cache_name}")
    except NotFoundError:
        # This is expected if the cache was already deleted or never created
        pass
    except Exception as e:
        print(f"\n[Cleanup] Error deleting cache {cache_name}: {e}")

# --- Exercise 1 & 2 Setup ---
SYSTEM_INSTRUCTION_LONG = (
    "You are an expert financial analyst specializing in emerging markets. "
    "Your responses must be highly structured, professional, and adhere strictly "
    "to the following five-point risk assessment framework: 1. Political Stability, "
    "2. Currency Volatility, 3. Regulatory Environment, 4. Infrastructure Readiness, "
    "and 5. Debt-to-GDP Ratio. This instruction set is crucial for all subsequent queries "
    "and must be treated as the primary context for analysis."
)
CACHE_NAME_1 = "financial_analyst_cache_001"


# ==============================================================================
# Exercise 1: Cache Creation and Immediate Usage
# ==============================================================================

print("--- Starting Exercise 1: Basic Cache Creation and Usage ---")

# 1. Ensure cleanup before starting
cleanup_cache(CACHE_NAME_1)
cache_obj = None

try:
    # 2. Create the cache object
    print(f"Creating cache '{CACHE_NAME_1}' for long system instruction...")
    
    cache_config = types.CreateCachedContentConfig(
        display_name=CACHE_NAME_1,
        system_instruction=SYSTEM_INSTRUCTION_LONG,
    )
    
    cache_obj = client.caches.create(
        model=MODEL_NAME,
        config=cache_config
    )
    
    print(f"Cache created successfully. Name: {cache_obj.name}")
    print(f"Cache token count (estimated): {cache_obj.usage_metadata.cached_content_token_count}")

    # 3. Use the cache in a generate_content request
    user_query = "Please provide a quick risk assessment summary for the Brazilian market based on your framework."
    
    print(f"\nSending query using cached content: '{user_query}'")
    
    response_1 = client.models.generate_content(
        model=MODEL_NAME,
        contents=[user_query],
        config=types.GenerateContentConfig(
            # Reference the cache using its full name
            cached_content=cache_obj.name
        )
    )

    # 4. Print results
    print("\n--- Response 1 Text (Snippet) ---")
    print(response_1.text[:500] + "...")
    print("\n--- Usage Metadata (Query 1) ---")
    print(response_1.usage_metadata)
    
except Exception as e:
    print(f"\nAn error occurred during Exercise 1: {e}")
finally:
    # 5. Robust cleanup
    if cache_obj:
        cleanup_cache(cache_obj.name)


# ==============================================================================
# Exercise 2: Demonstrating Token Cost Reduction
# ==============================================================================

print("\n\n--- Starting Exercise 2: Token Cost Verification ---")

CACHE_NAME_2 = "token_cost_test_cache"
cleanup_cache(CACHE_NAME_2)
cache_obj_2 = None

try:
    # 1. Re-create the cache (using the same long instruction)
    cache_config_2 = types.CreateCachedContentConfig(
        display_name=CACHE_NAME_2,
        system_instruction=SYSTEM_INSTRUCTION_LONG,
    )
    cache_obj_2 = client.caches.create(
        model=MODEL_NAME,
        config=cache_config_2
    )
    
    cached_tokens = cache_obj_2.usage_metadata.cached_content_token_count
    print(f"Cache created. Tokens cached: {cached_tokens}")
    
    # Define the short user query
    user_query_2 = "Summarize the political risk for Indonesia."

    # --- Query A: Using the Cache ---
    print("\n[Query A] Running query using the explicit cache...")
    response_A = client.models.generate_content(
        model=MODEL_NAME,
        contents=[user_query_2],
        config=types.GenerateContentConfig(
            cached_content=cache_obj_2.name
        )
    )
    
    metadata_A = response_A.usage_metadata
    print(f"Metadata A (Cached): Prompt Tokens = {metadata_A.prompt_token_count}, Cached Tokens = {metadata_A.cached_content_token_count}")
    
    # --- Query B: Without the Cache (Passing context directly) ---
    # We must construct the full prompt manually
    full_prompt_B = [
        types.Content(role="system", parts=[types.Part.from_text(SYSTEM_INSTRUCTION_LONG)]),
        types.Content(role="user", parts=[types.Part.from_text(user_query_2)])
    ]
    
    print("\n[Query B] Running query by passing the full system instruction directly...")
    response_B = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt_B
    )
    
    metadata_B = response_B.usage_metadata
    # Note: cached_content_token_count is 0 or absent when not using a cache
    print(f"Metadata B (Direct): Prompt Tokens = {metadata_B.prompt_token_count}")
    
    # 4. Comparison
    print("\n--- Token Comparison Summary ---")
    print(f"Query A (Cached Prompt Tokens): {metadata_A.prompt_token_count}")
    print(f"Query B (Direct Prompt Tokens): {metadata_B.prompt_token_count}")
    
    difference = metadata_B.prompt_token_count - metadata_A.prompt_token_count
    print(f"Difference (Savings): {difference} tokens per call (equal to the cached context size).")
    
except Exception as e:
    print(f"\nAn error occurred during Exercise 2: {e}")
finally:
    if cache_obj_2:
        cleanup_cache(CACHE_NAME_2)


# ==============================================================================
# Exercise 3: Cache Management (TTL and Update)
# ==============================================================================

print("\n\n--- Starting Exercise 3: TTL and Update Management ---")

CACHE_NAME_3 = "ttl_management_test_cache"
cleanup_cache(CACHE_NAME_3)
cache_obj_3 = None

try:
    # 1. Create cache with a short TTL (60 seconds)
    initial_ttl_seconds = 60
    print(f"Creating cache '{CACHE_NAME_3}' with initial TTL of {initial_ttl_seconds} seconds.")
    
    cache_config_3 = types.CreateCachedContentConfig(
        display_name=CACHE_NAME_3,
        system_instruction="A short instruction for testing TTL.",
        ttl=f"{initial_ttl_seconds}s"
    )
    
    cache_obj_3 = client.caches.create(
        model=MODEL_NAME,
        config=cache_config_3
    )

    # 2. List and examine the initial cache metadata
    print("\n--- Initial Cache Metadata ---")
    found_initial = False
    for cache in client.caches.list():
        if cache.name == cache_obj_3.name:
            print(f"Name: {cache.name}")
            print(f"Initial Expiry Time: {cache.expire_time}")
            found_initial = True
            break
            
    if not found_initial:
        raise RuntimeError("Cache was not found after creation.")

    # 3. Update the cache TTL to 10 minutes (600 seconds)
    new_ttl_seconds = 600
    print(f"\nUpdating cache TTL to {new_ttl_seconds} seconds (10 minutes)...")
    
    client.caches.update(
      name = cache_obj_3.name,
      config  = types.UpdateCachedContentConfig(
          ttl=f'{new_ttl_seconds}s'
      )
    )

    # 4. Fetch and examine the updated cache metadata
    updated_cache = client.caches.get(name=cache_obj_3.name)
    
    print("\n--- Updated Cache Metadata ---")
    print(f"Name: {updated_cache.name}")
    print(f"Updated Expiry Time: {updated_cache.expire_time}")
    
    # Basic check to confirm the expiry time moved forward
    if updated_cache.expire_time > cache_obj_3.expire_time:
        print("Success: Cache expiration time was successfully extended.")
    else:
        print("Warning: Cache expiration time did not appear to be extended.")
        
except Exception as e:
    print(f"\nAn error occurred during Exercise 3: {e}")
finally:
    if cache_obj_3:
        cleanup_cache(CACHE_NAME_3)


# ==============================================================================
# Exercise 4: Challenge - Dynamic Document Caching and Invalidation
# ==============================================================================

print("\n\n--- Starting Exercise 4: Dynamic Caching and Invalidation ---")

# Global state to simulate versioning
CURRENT_DOCUMENT_VERSION = "v1.0"
CACHE_NAME_4 = "nasa_flight_plan_cache"
# NASA PDF link from official docs
PDF_URL = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# Global variable to hold the File API object name for cleanup
uploaded_file_name = None

def upload_and_cache_document(pdf_url, system_instruction, version_tag):
    """
    Downloads, uploads, and caches a document, returning the cache object.
    Handles file cleanup on successful upload.
    """
    global uploaded_file_name
    
    # Clean up previous file if it exists
    if uploaded_file_name:
        try:
            client.files.delete(name=uploaded_file_name)
            uploaded_file_name = None
        except Exception:
            pass # Ignore if file deletion fails

    print(f"\n[Step 1] Retrieving and uploading PDF ({version_tag})...")
    
    try:
        doc_content = httpx.get(pdf_url).content
        doc_io = io.BytesIO(doc_content)
        
        document = client.files.upload(
          file=doc_io,
          config=dict(mime_type='application/pdf')
        )
        uploaded_file_name = document.name # Store for later deletion
        
        print(f"File uploaded successfully. File Name: {document.name}")
        
        # Create a cached content object
        print(f"[Step 2] Creating new cache '{CACHE_NAME_4}'...")
        cache = client.caches.create(
            model=MODEL_NAME,
            config=types.CreateCachedContentConfig(
                display_name=f"{CACHE_NAME_4}_{version_tag}",
                system_instruction=system_instruction,
                contents=[document],
            )
        )
        print(f"Cache created. Cached content tokens: {cache.usage_metadata.cached_content_token_count}")
        return cache
        
    except Exception as e:
        print(f"Error during upload or caching: {e}")
        return None

def manage_document_cache(new_version, pdf_url):
    """
    Handles the cache lifecycle, including invalidation if the version changes.
    """
    global CURRENT_DOCUMENT_VERSION
    
    system_inst = f"You are an expert analyst for the Apollo 17 Flight Plan. This document version is {new_version}."
    
    try:
        # 1. Attempt to get the existing cache metadata
        existing_cache = client.caches.get(name=CACHE_NAME_4)
        
        # 2. Check for version change (simulated by comparing global state)
        if CURRENT_DOCUMENT_VERSION == new_version:
            print(f"\n[Validation] Cache '{CACHE_NAME_4}' exists and version '{new_version}' matches. Reusing cache.")
            return existing_cache
        else:
            # 3. Cache Invalidation Logic: Version mismatch detected
            print(f"\n[Invalidation] Version mismatch detected. Old version: {CURRENT_DOCUMENT_VERSION}, New version: {new_version}.")
            
            # Delete the old cache
            client.caches.delete(existing_cache.name)
            print(f"[Invalidation] Old cache deleted.")
            
            # Update the global state
            CURRENT_DOCUMENT_VERSION = new_version
            
            # Create the new cache
            new_cache = upload_and_cache_document(pdf_url, system_inst, new_version)
            return new_cache
            
    except NotFoundError:
        # 4. Cache does not exist, create it for the first time
        print(f"\n[Creation] Cache '{CACHE_NAME_4}' not found. Creating initial cache for version {new_version}.")
        new_cache = upload_and_cache_document(pdf_url, system_inst, new_version)
        return new_cache
    except Exception as e:
        print(f"An unexpected error occurred during cache management: {e}")
        return None


# --- Execution Flow ---
cache_v1 = None
cache_v2 = None

try:
    # Initial Run (v1.0)
    print("--- RUN 1: Initial Cache Creation (v1.0) ---")
    cache_v1 = manage_document_cache(CURRENT_DOCUMENT_VERSION, PDF_URL)

    if cache_v1:
        # Query using the cached document
        print("\n[Query v1.0] Summarizing the mission objectives.")
        response_v1 = client.models.generate_content(
            model=MODEL_NAME,
            contents=["What are the primary mission objectives mentioned in the plan?"],
            config=types.GenerateContentConfig(cached_content=cache_v1.name)
        )
        print("Response snippet:", response_v1.text[:200] + "...")
        print(f"Usage Metadata: Cached Tokens = {response_v1.usage_metadata.cached_content_token_count}")


    # Simulated Update Run (v1.1)
    time.sleep(1) 
    NEW_VERSION = "v1.1" # Simulate a new version being released
    print(f"\n\n--- RUN 2: Cache Invalidation and Recreation ({NEW_VERSION}) ---")
    cache_v2 = manage_document_cache(NEW_VERSION, PDF_URL)

    if cache_v2:
        # Query using the new cached document
        print("\n[Query v1.1] Asking a question based on the new (simulated) cache.")
        response_v2 = client.models.generate_content(
            model=MODEL_NAME,
            contents=["What is the total duration of the EVA activities?"],
            config=types.GenerateContentConfig(cached_content=cache_v2.name)
        )
        print("Response snippet:", response_v2.text[:200] + "...")
        print(f"Usage Metadata: Cached Tokens = {response_v2.usage_metadata.cached_content_token_count}")

except Exception as e:
    print(f"A major error occurred during Exercise 4 execution: {e}")

finally:
    # Final Cleanup
    print("\n--- Final Cleanup ---")
    if cache_v2:
        cleanup_cache(cache_v2.name)
    elif cache_v1:
        cleanup_cache(cache_v1.name)
        
    if uploaded_file_name:
        try:
            client.files.delete(name=uploaded_file_name)
            print(f"[Cleanup] Deleted uploaded file: {uploaded_file_name}")
        except Exception as e:
            print(f"[Cleanup] Error deleting file: {e}")

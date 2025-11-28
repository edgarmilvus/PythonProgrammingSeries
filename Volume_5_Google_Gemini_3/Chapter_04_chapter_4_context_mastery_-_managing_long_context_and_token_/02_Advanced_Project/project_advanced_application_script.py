
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
from google import genai
from google.genai.errors import APIError

# --- CONFIGURATION ---
# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    exit()

# We use a model known for its large context window
MODEL_NAME = 'gemini-2.5-pro' 
# Define the temporary file name for the massive corpus
CORPUS_FILENAME = "regulatory_handbook_v1.txt"
# Define the target size for the simulated document (approx. 150,000 tokens)
# 1 token is roughly 4 characters, so 150,000 tokens * 4 chars/token = 600,000 characters
TARGET_CHAR_COUNT = 600000

def generate_massive_corpus(filename: str, char_count: int) -> str:
    """
    Generates a large, simulated regulatory document and saves it to a file.
    This simulates the 1M+ token input scenario.
    """
    print(f"\n[1] Generating massive simulated corpus ({char_count} characters)...")
    
    # Core regulatory boilerplate text
    boilerplate = (
        "SECTION 101: DATA PRIVACY AND RESIDENCY REQUIREMENTS. All user data "
        "must be encrypted using AES-256 GCM. Data residency for EU citizens "
        "is strictly limited to servers within the EEA, as defined by Annex B. "
        "Any breach of this section requires immediate notification within 72 hours. "
        "Failure to comply results in a Tier 3 penalty. "
        "SECTION 205: TRANSACTION REPORTING PROTOCOL. All transactions exceeding "
        "$10,000 USD must be reported to the central ledger within 24 hours of "
        "settlement. Batch reporting is permitted only if the batch size does not "
        "exceed 500 transactions and the total value is under $500,000 USD. "
        "SECTION 312: AI GOVERNANCE AND AUDITING. Any model used for credit scoring "
        "must maintain a full audit trail of input features and model weights. "
        "The fairness metric must be audited quarterly against the demographic "
        "data defined in Appendix C. "
    )
    
    # Repeat the boilerplate until the target size is met
    corpus_content = ""
    while len(corpus_content) < char_count:
        corpus_content += boilerplate + f" (Revision ID: {len(corpus_content)//len(boilerplate)}) "

    corpus_content = corpus_content[:char_count]
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(corpus_content)
        
    print(f"   -> Corpus saved to '{filename}'. Estimated tokens: {len(corpus_content) // 4}")
    return filename

def main():
    """Main function to execute the context caching and query workflow."""
    
    corpus_path = generate_massive_corpus(CORPUS_FILENAME, TARGET_CHAR_COUNT)
    cached_content = None
    
    try:
        # --- PHASE 1: UPLOAD AND CACHE THE MASSIVE CORPUS ---
        
        print("\n[2] Starting file upload...")
        start_time = time.time()
        
        # 2a. Upload the large file to the Gemini API
        uploaded_file = client.files.upload(file=corpus_path)
        print(f"   -> File uploaded successfully. URI: {uploaded_file.uri}")
        print(f"   -> Upload time: {time.time() - start_time:.2f} seconds.")
        
        # 2b. Create the CachedContent object
        print("\n[3] Creating Cached Content for optimization...")
        start_time = time.time()
        
        # We use the file object to create cached content.
        # The API processes and tokenizes the file for future reuse.
        cached_content = client.cached_content.create(
            model=MODEL_NAME,
            display_name="Regulatory Handbook V1 Cache",
            contents=[uploaded_file]
        )
        
        # Wait for the caching operation to complete (important for large files)
        while cached_content.state == 'PROCESSING':
            print("   -> Caching content... (Waiting 10 seconds)")
            time.sleep(10)
            cached_content = client.cached_content.get(name=cached_content.name)
            
        if cached_content.state == 'ACTIVE':
            print(f"   -> Content successfully cached! Name: {cached_content.name}")
            print(f"   -> Caching duration: {time.time() - start_time:.2f} seconds.")
            print(f"   -> Estimated Input Tokens Cached: {cached_content.usage_metadata.prompt_token_count}")
        else:
            print(f"   -> ERROR: Caching failed. State: {cached_content.state}")
            return

        # --- PHASE 2: FIRST COMPLEX QUERY (Initial Consumption) ---
        
        # The model is queried using the cached content object.
        # The input cost for the massive 150k token corpus is incurred here, 
        # or amortized if caching costs are separate, but the content is now ready.
        
        prompt_1 = (
            "Based *only* on the provided regulatory handbook, summarize the "
            "requirements for AI Governance (Section 312) and detail the exact "
            "conditions under which batch transaction reporting is permitted "
            "(Section 205). Provide the answer in a bulleted list."
        )
        
        print(f"\n[4] Executing Query 1 (Complex Analysis on Cached Data)...")
        query_start_time = time.time()
        
        response_1 = client.models.generate_content(
            model=MODEL_NAME,
            # We pass the prompt AND the cached content object
            contents=[cached_content, prompt_1] 
        )
        
        query_duration_1 = time.time() - query_start_time
        print(f"   -> Query 1 Duration: {query_duration_1:.2f} seconds.")
        print("   --- Query 1 Result Summary ---")
        print(response_1.text.split('\n')[0]) # Print first line for brevity
        print(f"   Tokens Used: {response_1.usage_metadata.total_token_count}")
        
        
        # --- PHASE 3: SECOND ITERATIVE QUERY (Demonstrating Optimization) ---
        
        # Since the massive corpus is already cached, the latency and cost 
        # for this second query, which uses the same context, will be significantly lower 
        # compared to passing the full 150,000 tokens again.
        
        prompt_2 = (
            "Search the entire corpus for the exact penalty tier associated with "
            "a breach of data residency requirements (Section 101). State only the Tier number."
        )
        
        print(f"\n[5] Executing Query 2 (Optimized Retrieval on Cached Data)...")
        query_start_time = time.time()
        
        response_2 = client.models.generate_content(
            model=MODEL_NAME,
            # Again, we use the cached content object
            contents=[cached_content, prompt_2]
        )
        
        query_duration_2 = time.time() - query_start_time
        
        # In a real-world scenario, query_duration_2 would be significantly faster 
        # than if we had to re-process the full 150,000 tokens.
        print(f"   -> Query 2 Duration: {query_duration_2:.2f} seconds.")
        print("   --- Query 2 Result Summary ---")
        print(f"   Answer: {response_2.text.strip()}")
        print(f"   Tokens Used: {response_2.usage_metadata.total_token_count} (Note the prompt token count is minimal.)")


    except APIError as e:
        print(f"\n[!] An API Error occurred: {e}")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        
    finally:
        # --- PHASE 4: CLEANUP ---
        
        print("\n[6] Starting Cleanup...")
        
        # Clean up the local file
        if os.path.exists(corpus_path):
            os.remove(corpus_path)
            print(f"   -> Local file '{corpus_path}' deleted.")
            
        # Clean up the remote cached content and uploaded file
        if cached_content:
            try:
                # Delete the cached content object
                client.cached_content.delete(name=cached_content.name)
                print(f"   -> Remote Cached Content '{cached_content.name}' deleted.")
            except Exception as e:
                print(f"   -> Could not delete cached content: {e}")

        if 'uploaded_file' in locals() and uploaded_file:
            try:
                # Delete the original uploaded file object
                client.files.delete(name=uploaded_file.name)
                print(f"   -> Remote Uploaded File '{uploaded_file.name}' deleted.")
            except Exception as e:
                # This might fail if deleting the cached content automatically deletes the file
                print(f"   -> Note: Original uploaded file deletion skipped or failed.")
            
        print("\n[7] Script execution complete.")

if __name__ == "__main__":
    main()

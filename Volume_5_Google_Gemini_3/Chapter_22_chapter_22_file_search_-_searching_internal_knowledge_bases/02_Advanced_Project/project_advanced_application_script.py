
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
import uuid
from pathlib import Path
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- Configuration and Setup ---

# Ensure the GEMINI_API_KEY is set in your environment variables
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Initialize the Gemini Client
# This client handles all API calls, including models, files, and file_search_stores.
client = genai.Client()

# Define constants for file management
TEMP_DIR = Path("./temp_rag_files")
MODEL_NAME = "gemini-2.5-flash"

# Generate a unique store name to avoid conflicts across runs
UNIQUE_ID = str(uuid.uuid4())[:8]
STORE_DISPLAY_NAME = f"Compliance_RAG_Store_{UNIQUE_ID}"

# --- Helper Function for File Creation ---

def create_temp_file(filename: str, content: str) -> str:
    """Creates a temporary file for upload and returns its absolute path."""
    TEMP_DIR.mkdir(exist_ok=True)
    file_path = os.path.join(TEMP_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created temporary file: {filename}")
    return file_path

def wait_for_operation(operation):
    """Waits for a long-running asynchronous operation to complete."""
    print(f"Waiting for operation {operation.name} to complete...")
    while not operation.done:
        time.sleep(5)
        operation = client.operations.get(operation)
        print("Status: Indexing in progress...")
    
    if operation.error:
        raise APIError(f"Operation failed with error: {operation.error}")
        
    print(f"Operation {operation.name} completed successfully.")
    return operation.response

# --- Main RAG Workflow ---

def run_rag_pipeline():
    file_search_store = None
    try:
        # 1. Create the File Search store (Vector Database equivalent)
        print("\n--- Phase 1: Creating File Search Store ---")
        file_search_store = client.file_search_stores.create(
            config={'display_name': STORE_DISPLAY_NAME}
        )
        store_name = file_search_store.name
        print(f"File Search Store created: {store_name}")

        # 2. Prepare Documents
        
        # Document A: Internal Policy Manual (Focus on custom chunking)
        policy_content = """
        SECTION 1: Data Retention Policy (DRP-2023)
        All client communication records must be archived for a minimum period of 7 years. 
        Records related to financial transactions must be retained for 10 years. 
        The primary contact for DRP-2023 compliance is Robert Graves, extension 404. 
        Any violation of this policy is subject to immediate disciplinary review.
        
        SECTION 2: Remote Work Guidelines (RWG-2023)
        Employees working remotely must utilize mandatory VPN software. 
        Access to proprietary source code requires two-factor authentication (2FA). 
        Laptops must be encrypted using AES-256 standards.
        """
        policy_file_path = create_temp_file("policy_manual.txt", policy_content)
        
        # Document B: Client Contract (Focus on custom metadata)
        contract_content = """
        CLIENT AGREEMENT: ACME CORP (Contract ID: ACME-2024-001)
        Scope of Work: Development of a secure Python backend for their new inventory system.
        Payment Terms: Net 45 days. 
        Confidentiality Clause: All data shared by Acme Corp is proprietary and must not be stored 
        on any external cloud service. The project lead is Jane Smith.
        """
        contract_file_path = create_temp_file("acme_contract.txt", contract_content)

        # 3. Upload and Index Document A (Policy Manual) with Custom Chunking
        print("\n--- Phase 2: Indexing Policy Manual (Custom Chunking) ---")
        
        # Define chunking configuration: small chunks (150 tokens) with high overlap (30 tokens)
        # This increases semantic coherence between retrieved chunks.
        chunking_config = {
            'white_space_config': {
                'max_tokens_per_chunk': 150,
                'max_overlap_tokens': 30
            }
        }
        
        operation_policy = client.file_search_stores.upload_to_file_search_store(
            file=policy_file_path,
            file_search_store_name=store_name,
            config={
                'display_name': 'Policy Manual DRP-2023',
                'chunking_config': chunking_config
            }
        )
        wait_for_operation(operation_policy)
        
        # 4. Upload and Index Document B (Client Contract) with Custom Metadata
        print("\n--- Phase 3: Indexing Client Contract (Custom Metadata) ---")
        
        # Define custom metadata for filtering specific clients later
        custom_metadata = [
            {"key": "client_name", "string_value": "Acme Corp"},
            {"key": "project_type", "string_value": "Python Backend"}
        ]
        
        operation_contract = client.file_search_stores.upload_to_file_search_store(
            file=contract_file_path,
            file_search_store_name=store_name,
            config={
                'display_name': 'Acme Corp Contract',
                'custom_metadata': custom_metadata
            }
        )
        wait_for_operation(operation_contract)
        
        # 5. General Query (Searches all indexed documents)
        print("\n--- Phase 4: Query 1 (General Search) ---")
        general_query = "What are the rules regarding data retention and who is the contact?"
        
        response_general = client.models.generate_content(
            model=MODEL_NAME,
            contents=general_query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ]
            )
        )
        
        print(f"Query: {general_query}")
        print("Response Text:")
        print(response_general.text)
        
        # 6. Metadata Filtered Query (Searches only the Acme Corp contract)
        print("\n--- Phase 5: Query 2 (Metadata Filtered Search) ---")
        filtered_query = "What are the payment terms and confidentiality rules for Acme Corp?"
        
        # Apply the filter based on the metadata key defined in step 4
        metadata_filter_string = 'client_name="Acme Corp"'
        
        response_filtered = client.models.generate_content(
            model=MODEL_NAME,
            contents=filtered_query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name],
                            metadata_filter=metadata_filter_string
                        )
                    )
                ]
            )
        )
        
        print(f"Query: {filtered_query} (Filter: {metadata_filter_string})")
        print("Response Text:")
        print(response_filtered.text)

        # 7. Extracting Citations (Grounding Metadata)
        print("\n--- Phase 6: Citation Extraction ---")
        
        # Citations are found in the grounding_metadata attribute of the candidate response
        grounding_metadata = response_filtered.candidates[0].grounding_metadata
        
        if grounding_metadata and grounding_metadata.grounding_chunks:
            print(f"Found {len(grounding_metadata.grounding_chunks)} grounding chunks (citations):")
            for i, chunk in enumerate(grounding_metadata.grounding_chunks):
                # The 'web' attribute is used for external search, 'file' for File Search
                if chunk.file:
                    print(f"  Citation {i+1}:")
                    print(f"    Source File: {chunk.file.name}")
                    print(f"    Display Name: {chunk.file.display_name}")
                    print(f"    Text Snippet: '{chunk.text_content[:80]}...'")
        else:
            print("No grounding metadata or citations found for the filtered query.")

    except APIError as e:
        print(f"\nAn API Error occurred: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # 8. Cleanup Resources
        print("\n--- Phase 7: Cleaning Up Resources ---")
        if file_search_store:
            # The 'force: True' parameter is required to delete a store that still contains files.
            client.file_search_stores.delete(
                name=store_name, 
                config={'force': True}
            )
            print(f"Successfully deleted File Search Store: {store_name}")
        
        # Clean up local temporary files
        import shutil
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            print(f"Successfully removed temporary directory: {TEMP_DIR}")

if __name__ == "__main__":
    run_rag_pipeline()

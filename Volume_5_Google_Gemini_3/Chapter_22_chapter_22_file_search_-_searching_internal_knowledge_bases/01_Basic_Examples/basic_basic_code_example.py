
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
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. CONFIGURATION AND SETUP ---

# Define the name for our local file and the file search store
FILE_NAME = "aether_dynamics_policy.txt"
STORE_DISPLAY_NAME = "AetherDynamicsInternalKnowledge"
# We use a simple, unique identifier for the store name structure
STORE_NAME_PREFIX = "fileSearchStores/"

def create_dummy_file(filename):
    """Creates a local file containing proprietary information."""
    print(f"Creating local file: {filename}")
    policy_content = (
        "## Aether Dynamics: Quantum Leave Policy (Q-LP-2024)\n"
        "All employees are entitled to 15 'Quantum Leave' days per calendar year. "
        "These days must be approved by a Level 4 Manager or higher. "
        "The primary purpose of Quantum Leave is for deep work or personal development, "
        "not general vacation. Unused Quantum Leave days expire on December 31st and "
        "cannot be rolled over. The official contact for Q-LP inquiries is Dr. Elara Vance."
    )
    with open(filename, "w") as f:
        f.write(policy_content)
    print("File created successfully.")

def cleanup_store(client: genai.Client, store_name: str):
    """Deletes the File Search store to manage quota and resources."""
    print(f"\n--- 6. CLEANUP: Deleting File Search Store: {store_name} ---")
    try:
        # The 'force: True' config is often required to delete stores that contain files.
        client.file_search_stores.delete(name=store_name, config={'force': True})
        print(f"Successfully deleted store: {store_name}")
    except APIError as e:
        print(f"Error during cleanup (Store may already be gone or permissions issue): {e}")

def run_file_search_rag():
    """Main function to demonstrate the RAG workflow."""
    client = genai.Client()
    
    # Ensure the dummy file exists
    create_dummy_file(FILE_NAME)
    
    file_search_store = None
    
    try:
        # --- 2. CREATE THE FILE SEARCH STORE ---
        print("\n--- 2. CREATING FILE SEARCH STORE ---")
        # This creates the persistent container for our document embeddings.
        file_search_store = client.file_search_stores.create(
            config={'display_name': STORE_DISPLAY_NAME}
        )
        # The full name is needed for subsequent API calls (e.g., 'fileSearchStores/xxxxxxx')
        store_name = file_search_store.name
        print(f"File Search Store created: {store_name}")
        
        # --- 3. UPLOAD, CHUNK, AND INDEX THE FILE ---
        print("\n--- 3. UPLOADING AND INDEXING FILE (Long-Running Operation) ---")
        
        # We use upload_to_file_search_store for a single, direct RAG pipeline.
        operation = client.file_search_stores.upload_to_file_search_store(
            file=FILE_NAME,
            file_search_store_name=store_name,
            config={
                'display_name': f'Internal-{FILE_NAME}'
            }
        )
        
        # Wait until the indexing operation is complete (polling loop)
        print("Indexing in progress. Waiting for completion...")
        while not operation.done:
            time.sleep(5)
            # Fetch the latest status of the long-running operation
            operation = client.operations.get(operation)
            print(".", end="", flush=True)

        print("\nIndexing complete.")
        
        # --- 4. QUERY THE MODEL USING THE RAG TOOL ---
        
        # The query asks about proprietary information only found in the uploaded file.
        query = "How many Quantum Leave days are employees entitled to, and who is the official contact for this policy?"
        print(f"\n--- 4. QUERYING GEMINI ---")
        print(f"QUESTION: {query}")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", # A fast model supporting File Search
            contents=query,
            config=types.GenerateContentConfig(
                # Attach the File Search tool, pointing it to our specific store
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ]
            )
        )

        # --- 5. DISPLAY RESULTS AND CITATIONS ---
        print("\n--- 5. MODEL RESPONSE ---")
        print(response.text)
        
        # Access the grounding metadata for citations
        if response.candidates and response.candidates[0].grounding_metadata:
            metadata = response.candidates[0].grounding_metadata
            print("\n--- CITATION METADATA ---")
            print(f"Grounding Passages Used: {len(metadata.retrieved_chunks)} chunks")
            print(f"File Source Name: {metadata.grounding_chunks[0].web_or_file.display_name if metadata.grounding_chunks else 'N/A'}")
            print(f"Retrieved Context Snippet (First 100 chars):")
            # Display a snippet of the retrieved context for verification
            if metadata.retrieved_chunks:
                print(f"'{metadata.retrieved_chunks[0].text[:100]}...'")
        else:
            print("\n(No specific grounding metadata or citations found.)")

    except APIError as e:
        print(f"\nAn API Error occurred: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        
    finally:
        # Ensure cleanup runs regardless of success/failure
        if file_search_store:
            cleanup_store(client, file_search_store.name)
        
        # Clean up the local file
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
            print(f"Local file {FILE_NAME} removed.")

if __name__ == "__main__":
    run_file_search_rag()


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

# Source File: theory_theoretical_foundations_part6.py
# Description: Theoretical Foundations
# ==========================================

import os
import time
from google import genai
from google.genai import types

# --- 1. SETUP AND INITIALIZATION ---

# Ensure the GEMINI_API_KEY environment variable is set
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure your GEMINI_API_KEY is set correctly.")
    exit()

STORE_DISPLAY_NAME = "Proprietary_Research_Store"
FILE_NAME = "internal_research_memo.txt"
STORE_NAME = None # Will be populated after creation

def create_dummy_file(filename):
    """Creates a sample file containing proprietary data."""
    content = (
        "Project Phoenix Q3 Report: The primary finding regarding the 'Phoenix' initiative "
        "is the unexpected success of the new micro-chip architecture designed by Robert Graves. "
        "Graves' design, which utilizes a novel quantum tunneling effect, resulted in a 40% "
        "reduction in power consumption compared to the baseline model. The implementation phase "
        "is projected to conclude by the end of 2024. Further research into expanding the "
        "quantum tunneling approach is recommended for 2025."
    )
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created sample file: {filename}")

def cleanup_store(store_name):
    """Deletes the File Search Store to clean up resources."""
    if store_name:
        print(f"\nAttempting to delete store: {store_name}...")
        try:
            # The force=True flag is necessary to delete the store and all indexed data within it.
            client.file_search_stores.delete(name=store_name, config={'force': True})
            print(f"Successfully deleted store: {store_name}")
        except Exception as e:
            print(f"Error during cleanup: {e}")

# --- MAIN RAG WORKFLOW ---

try:
    # 1. Create the dummy file for ingestion
    create_dummy_file(FILE_NAME)

    # 2. Create the File Search store (The Knowledge Vault)
    print(f"\nCreating File Search Store with display name: {STORE_DISPLAY_NAME}...")
    file_search_store = client.file_search_stores.create(
        config={'display_name': STORE_DISPLAY_NAME}
    )
    STORE_NAME = file_search_store.name
    print(f"Store created successfully: {STORE_NAME}")

    # 3. Upload the file and initiate indexing (The Librarian's Work)
    print(f"Uploading and importing file '{FILE_NAME}' into store...")
    operation = client.file_search_stores.upload_to_file_search_store(
        file=FILE_NAME,
        file_search_store_name=STORE_NAME,
        config={
            'display_name': os.path.basename(FILE_NAME),
            # Optional: Custom chunking configuration for specialized content
            'chunking_config': {
              'white_space_config': {
                'max_tokens_per_chunk': 150,
                'max_overlap_tokens': 10
              }
            }
        }
    )

    # 4. Wait for the indexing operation to complete (Long-Running Operation)
    print("Indexing in progress. Waiting for completion (this may take a minute)...")
    start_time = time.time()
    while not operation.done:
        time.sleep(5)
        operation = client.operations.get(operation)
        print(f"  Status: {operation.metadata.state.name} ({int(time.time() - start_time)}s elapsed)")
        if time.time() - start_time > 120:  # Timeout after 2 minutes
            raise TimeoutError("Indexing operation timed out.")
    
    print("Indexing complete.")

    # 5. Query the model using the File Search tool (Retrieval-Augmented Generation)
    user_query = "What unexpected finding was made regarding Project Phoenix, and who designed the architecture?"
    print(f"\n--- Querying Gemini with RAG ---\nQuery: {user_query}")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", # Supported model for File Search
        contents=user_query,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[STORE_NAME] # Pointing to the indexed store
                    )
                )
            ]
        )
    )

    # 6. Display the grounded response and citations
    print("\n--- Model Response (Grounded) ---")
    print(response.text)
    
    print("\n--- Grounding Metadata (Citations) ---")
    if response.candidates and response.candidates[0].grounding_metadata:
        metadata = response.candidates[0].grounding_metadata
        for chunk in metadata.grounding_chunks:
            # Citations confirm the model used the proprietary file as context
            print(f"  Source File: {chunk.web.title if chunk.web else 'Internal File'}")
            print(f"  Text Used: {chunk.text}")
    else:
        print("No specific grounding metadata found.")

except TimeoutError as e:
    print(f"Operation failed: {e}")
except Exception as e:
    print(f"An error occurred during the workflow: {e}")

finally:
    # 7. Cleanup
    cleanup_store(STORE_NAME)
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
        print(f"Removed local file: {FILE_NAME}")


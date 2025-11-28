
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: file_search_exercises.py

"""
Chapter 22 Practical Exercises: Implementing Retrieval-Augmented Generation (RAG)
using the Gemini File Search API for internal knowledge retrieval.
"""

# Imports moved to the setup block, ensuring they are available here
# from google import genai, types, time, os, uuid, APIError

# --- Configuration and Initialization ---
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Ensure GEMINI_API_KEY is set: {e}")
    exit()

# Unique ID prefix for this session to ensure store names are unique
SESSION_ID = uuid.uuid4().hex[:8]

def wait_for_operation(operation):
    """Utility function to poll the long-running operation until complete."""
    print(f"    -> Operation {operation.name} started. Waiting for completion...")
    while not operation.done:
        time.sleep(5)
        print("    -> Polling status...")
        try:
            operation = client.operations.get(operation)
        except APIError as e:
            # Handle potential transient errors during polling
            print(f"    -> Warning during polling: {e}")
            break
    
    if operation.error:
        print(f"    -> Operation failed: {operation.error.message}")
        raise RuntimeError(f"Indexing failed: {operation.error.message}")
    print("    -> Operation complete.")
    return operation

# --- Exercise 2 Function: Store Management and Cleanup ---

def list_and_cleanup_stores(prefix="rag_ex_"):
    """Lists stores and deletes those matching a specific prefix."""
    print("\n--- Running Exercise 2: Store Management and Cleanup ---")
    stores_to_delete = []
    
    try:
        # List all File Search stores
        print("Listing all File Search Stores:")
        # The list method returns an iterator
        store_iterator = client.file_search_stores.list()
        
        found_stores = False
        for store in store_iterator:
            found_stores = True
            display_name = store.config.display_name if store.config and store.config.display_name else "N/A"
            print(f"  Store Name: {store.name}, Display Name: {display_name}")

            # Check if the store should be deleted based on prefix
            if display_name.startswith(prefix):
                stores_to_delete.append(store.name)
        
        if not found_stores:
            print("No File Search Stores found.")

        if stores_to_delete:
            print(f"\nFound {len(stores_to_delete)} test stores matching prefix '{prefix}' for deletion.")
            
            for store_name in stores_to_delete:
                print(f"  Deleting store: {store_name}...")
                # Use config={'force': True} as recommended for deletion of stores containing files
                client.file_search_stores.delete(
                    name=store_name, 
                    config={'force': True} 
                )
                print(f"  Successfully deleted {store_name}.")
        else:
            print("No test stores found for cleanup with this prefix.")

    except APIError as e:
        print(f"Error during store management: {e}")

# --- Exercise 1: Basic RAG Setup (Direct Upload & Query) ---

def exercise_1_basic_rag():
    """Implements basic RAG with direct upload and immediate cleanup."""
    print("\n\n#####################################################")
    print("--- Running Exercise 1: Implementing Basic RAG with Direct Upload ---")
    
    store_display_name = f"rag_ex_basic_{SESSION_ID}"
    file_path = "ex1_doc.txt"
    file_display_name = "Digital_Twin_Report"
    
    file_search_store = None
    
    try:
        # 1. Create the File Search store
        print(f"1. Creating File Search Store: {store_display_name}")
        file_search_store = client.file_search_stores.create(
            config={'display_name': store_display_name}
        )
        print(f"   Store created: {file_search_store.name}")

        # 2. Upload and import a file into the File Search store (single operation)
        print(f"2. Uploading and indexing file: {file_path}")
        operation = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=file_search_store.name,
            config={
                'display_name': file_display_name,
            }
        )
        
        # 3. Wait until import is complete
        wait_for_operation(operation)

        # 4. Query the model using the File Search tool
        query = "What is the primary definition and application of a Digital Twin?"
        print(f"4. Querying model with RAG: '{query}'")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[file_search_store.name]
                        )
                    )
                ]
            )
        )

        print("\n--- Model Response (Grounded in ex1_doc.txt) ---")
        print(response.text)
        print("--------------------------------------------------")

    except Exception as e:
        print(f"An error occurred during Exercise 1: {e}")
    
    finally:
        # 5. CRITICAL: Cleanup
        if file_search_store:
            print(f"\n5. Deleting File Search Store: {file_search_store.name}")
            client.file_search_stores.delete(name=file_search_store.name, config={'force': True})
            print("   Cleanup complete.")

# --- Exercise 3: Custom Chunking and Citation Verification ---

def exercise_3_chunking_and_citations():
    """Demonstrates custom chunking configuration and citation retrieval."""
    print("\n\n#####################################################")
    print("--- Running Exercise 3: Custom Chunking and Citation Verification ---")

    store_display_name = f"rag_ex_chunking_{SESSION_ID}"
    file_path = "ex3_doc.txt"
    file_display_name = "Project_Chronos_Report"
    file_search_store = None

    try:
        # 1. Create the File Search store
        print(f"1. Creating File Search Store: {store_display_name}")
        file_search_store = client.file_search_stores.create(
            config={'display_name': store_display_name}
        )

        # 2. Upload with custom chunking configuration
        print("2. Uploading file with custom chunking (max 50 tokens)...")
        operation = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=file_search_store.name,
            config={
                'display_name': file_display_name,
                'chunking_config': {
                    'white_space_config': {
                        'max_tokens_per_chunk': 50,  # Small chunk size
                        'max_overlap_tokens': 5
                    }
                }
            }
        )

        # 3. Wait until import is complete
        wait_for_operation(operation)

        # 4. Query the model
        query = "What was the primary finding regarding latency optimization in the Chronos Report?"
        print(f"4. Querying model: '{query}'")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[file_search_store.name]
                        )
                    )
                ]
            )
        )

        print("\n--- Model Response ---")
        print(response.text)

        # 5. Access and print grounding metadata (citations)
        print("\n--- Citation Verification (Grounding Metadata) ---")
        # Access grounding_metadata via response.candidates[0]
        grounding_metadata = response.candidates[0].grounding_metadata
        
        if grounding_metadata and grounding_metadata.retrieved_chunks:
            print(f"Total retrieved chunks: {len(grounding_metadata.retrieved_chunks)}")
            
            for i, chunk in enumerate(grounding_metadata.retrieved_chunks):
                # Access the source display name
                source = chunk.source_metadata.file_search_store_source_metadata.file_display_name
                print(f"  Chunk {i+1} (Source: {source}):")
                print(f"  Text Snippet: '{chunk.text_content.strip()}'\n")
        else:
            print("No grounding metadata or retrieved chunks found.")

    except Exception as e:
        print(f"An error occurred during Exercise 3: {e}")
    
    finally:
        # 6. Cleanup
        if file_search_store:
            print(f"6. Deleting File Search Store: {file_search_store.name}")
            client.file_search_stores.delete(name=file_search_store.name, config={'force': True})
            print("   Cleanup complete.")

# --- Exercise 4: Advanced Challenge - Targeted Search with Metadata Filtering ---

def exercise_4_metadata_filtering():
    """Implements a multi-document store with targeted search via metadata filtering."""
    print("\n\n#####################################################")
    print("--- Running Exercise 4: Targeted Search with Metadata Filtering ---")

    store_display_name = f"rag_ex_advanced_{SESSION_ID}"
    file_search_store = None

    try:
        # 1. Create the single File Search Store
        print(f"1. Creating Advanced Quantum Store: {store_display_name}")
        file_search_store = client.file_search_stores.create(
            config={'display_name': store_display_name}
        )
        store_names = [file_search_store.name]

        # 2. Upload Document A (History) with custom metadata
        print("2. Uploading Document A (History) with metadata 'topic=History'...")
        op_a = client.file_search_stores.upload_to_file_search_store(
            file='ex4_doc_a.txt',
            file_search_store_name=file_search_store.name,
            config={
                'display_name': 'Quantum_History_Doc',
                'custom_metadata': [
                    {"key": "topic", "string_value": "History"}
                ]
            }
        )
        wait_for_operation(op_a)

        # 3. Upload Document B (Current) with custom metadata
        print("3. Uploading Document B (Current) with metadata 'topic=Current'...")
        op_b = client.file_search_stores.upload_to_file_search_store(
            file='ex4_doc_b.txt',
            file_search_store_name=file_search_store.name,
            config={
                'display_name': 'Quantum_Current_Doc',
                'custom_metadata': [
                    {"key": "topic", "string_value": "Current"}
                ]
            }
        )
        wait_for_operation(op_b)
        print("   Both documents indexed successfully.")
        

        # 4. Query 1 (Filtered Search: History)
        query_1 = "Who proposed the theoretical basis for quantum computing?"
        filter_1 = "topic=History"
        print(f"\n4a. Querying with Filter: '{filter_1}' (Should only use Document A)")
        
        response_1 = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query_1,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=store_names,
                            metadata_filter=filter_1,
                        )
                    )
                ]
            )
        )
        print(f"   Response 1: {response_1.text.strip()}")
        
        # 5. Query 2 (Filtered Search: Current)
        query_2 = "What are the primary modern uses of quantum systems?"
        filter_2 = "topic=Current"
        print(f"\n5b. Querying with Filter: '{filter_2}' (Should only use Document B)")

        response_2 = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query_2,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=store_names,
                            metadata_filter=filter_2,
                        )
                    )
                ]
            )
        )
        print(f"   Response 2: {response_2.text.strip()}")

    except Exception as e:
        print(f"An error occurred during Exercise 4: {e}")
    
    finally:
        # 6. Cleanup
        if file_search_store:
            print(f"\n6. Deleting File Search Store: {file_search_store.name}")
            client.file_search_stores.delete(name=file_search_store.name, config={'force': True})
            print("   Cleanup complete.")

# --- Exercise 5: Alternative Workflow (Separate Upload and Import) ---

def exercise_5_separate_import():
    """Demonstrates the two-step RAG workflow: upload file, then import file reference."""
    print("\n\n#####################################################")
    print("--- Running Exercise 5: Alternative Workflow (Separate Upload and Import) ---")

    store_display_name = f"rag_ex_import_{SESSION_ID}"
    file_path = "ex1_doc.txt"
    uploaded_file = None
    file_search_store = None

    try:
        # 1. Upload the file using the Files API (temporary storage)
        print(f"1. Uploading raw file '{file_path}' to temporary storage...")
        uploaded_file = client.files.upload(file=file_path, config={'name': 'temp_rag_file'})
        print(f"   Raw File Object Name: {uploaded_file.name}")

        # 2. Create the File Search store
        print(f"2. Creating File Search Store: {store_display_name}")
        file_search_store = client.file_search_stores.create(
            config={'display_name': store_display_name}
        )

        # 3. Import the file reference into the File Search store
        print("3. Importing file reference into the File Search Store (indexing begins)...")
        operation = client.file_search_stores.import_file(
            file_search_store_name=file_search_store.name,
            file_name=uploaded_file.name # Use the name of the file object
        )

        # 4. Wait until import is complete
        wait_for_operation(operation)

        # 5. Query the store to confirm data is available
        query = "What is the primary definition of a Digital Twin?"
        print(f"5. Querying model: '{query}'")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[file_search_store.name]
                        )
                    )
                ]
            )
        )
        print("\n--- Model Response (Verification) ---")
        print(response.text)
        print("---------------------------------------")

    except Exception as e:
        print(f"An error occurred during Exercise 5: {e}")
    
    finally:
        # 6. Cleanup
        if file_search_store:
            print(f"\n6a. Deleting File Search Store: {file_search_store.name}")
            client.file_search_stores.delete(name=file_search_store.name, config={'force': True})
            print("   Store cleanup complete.")
        
        # Delete the temporary file object created in step 1
        if uploaded_file:
            print(f"6b. Deleting temporary File API object: {uploaded_file.name}")
            client.files.delete(name=uploaded_file.name)
            print("   File API cleanup complete.")


# --- Main Execution Block ---
if __name__ == "__main__":
    if not os.path.exists("ex1_doc.txt"):
        print("Setup files not found. Please run the initial setup code block first.")
    else:
        # Run Exercise 1
        exercise_1_basic_rag()
        
        # Run Exercise 2 (Cleanup verification for Ex 1)
        list_and_cleanup_stores(prefix="rag_ex_basic_") 
        
        # Run subsequent exercises
        exercise_3_chunking_and_citations()
        exercise_4_metadata_filtering()
        exercise_5_separate_import()
        
        # Final cleanup for all remaining test stores (Ex 3, Ex 4, Ex 5)
        list_and_cleanup_stores(prefix="rag_ex_")

        # Optional: Clean up local files
        print("\nCleaning up local document files...")
        for f in ["ex1_doc.txt", "ex3_doc.txt", "ex4_doc_a.txt", "ex4_doc_b.txt"]:
            if os.path.exists(f):
                os.remove(f)
        print("Local document files removed.")

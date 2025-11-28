
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

# Source File: basic_building_the_core_engine.py
# Description: Building the Core Engine
# ==========================================

import os
import time
from google import genai
from google.genai import types

# Ensure your GEMINI_API_KEY is set in your environment variables
# client = genai.Client() will automatically pick it up.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

# --- 1. Utility for Citation Processing (Essential for Grounding) ---

def add_citations(response: types.GenerateContentResponse) -> str:
    """
    Processes the grounding metadata to insert inline citations into the response text.
    This function is crucial for verifying information from both web and RAG sources.
    """
    if not response.candidates or not response.candidates[0].grounding_metadata:
        return response.text

    text = response.text
    metadata = response.candidates[0].grounding_metadata
    supports = metadata.grounding_supports
    chunks = metadata.grounding_chunks

    # Sort supports by end_index in descending order to avoid shifting issues when inserting.
    sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    for support in sorted_supports:
        end_index = support.segment.end_index
        if support.grounding_chunk_indices:
            citation_links = []
            
            # Iterate through the indices to build the citation string
            for i in support.grounding_chunk_indices:
                if i < len(chunks):
                    chunk = chunks[i]
                    # Check if the chunk is from a web search or a file search
                    if chunk.web:
                        uri = chunk.web.uri
                    elif chunk.file:
                        # For file search, the URI is the file name for internal reference
                        uri = f"internal://{chunk.file.display_name}"
                    else:
                        continue
                        
                    citation_links.append(f"[{i + 1}]({uri})")

            if citation_links:
                citation_string = ", ".join(citation_links)
                # Insert the citation string into the text at the segment's end index
                text = text[:end_index] + citation_string + text[end_index:]

    return text

# --- 2. Stateful Setup: File Search Store (Internal RAG) ---

def setup_file_search_store(client: genai.Client, file_path: str, store_name: str) -> str:
    """
    Creates a File Search store and uploads a document for RAG.
    This process is asynchronous and requires waiting for the operation to complete.
    """
    print(f"\n[SETUP] Starting File Search Store creation: '{store_name}'...")
    
    # 2a. Create dummy file content for internal knowledge
    internal_content = (
        "Project Chimera Documentation: The primary goal of Project Chimera "
        "is to develop a decentralized, self-modifying Python agent framework. "
        "The current version, 2.1.0 (codenamed 'Hydra'), utilizes a novel "
        "asynchronous messaging protocol based on ZeroMQ. The lead engineer "
        "responsible for the initial ZeroMQ implementation was Dr. Elias Vance."
    )
    with open(file_path, 'w') as f:
        f.write(internal_content)
    print(f"[SETUP] Created dummy file: {file_path}")

    try:
        # 2b. Create the persistent store container
        file_search_store = client.file_search_stores.create(
            config={'display_name': store_name}
        )
        store_id = file_search_store.name
        print(f"[SETUP] Store created: {store_id}")

        # 2c. Upload and import the file into the store (long-running operation)
        print("[SETUP] Uploading and importing file...")
        operation = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=store_id,
            config={'display_name': os.path.basename(file_path)}
        )

        # 2d. Wait until import is complete (critical asynchronous step)
        while not operation.done:
            print("[SETUP] Waiting for file import to complete (sleeping 5s)...")
            time.sleep(5)
            operation = client.operations.get(operation)

        print(f"[SETUP] File import complete. Store ready: {store_id}")
        return store_id

    except Exception as e:
        print(f"[ERROR] Failed to set up File Search Store: {e}")
        return None

# --- 3. The Core Orchestrator Function ---

def run_research_query(prompt: str, file_search_store_name: str):
    """
    The central function that exposes both Google Search and File Search tools
    to the Gemini model, allowing it to autonomously select the best resource.
    """
    print(f"\n--- RESEARCH QUERY: {prompt} ---")

    # 3a. Define the Google Search Tool (External, Real-Time Knowledge)
    google_search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    # 3b. Define the File Search Tool (Internal, RAG Knowledge)
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            file_search_store_names=[file_search_store_name]
        )
    )

    # 3c. Configure the model to use both tools simultaneously
    config = types.GenerateContentConfig(
        tools=[google_search_tool, file_search_tool]
    )
    
    # Using Pro model for superior reasoning and tool orchestration
    model_name = "gemini-2.5-pro" 

    try:
        # 3d. Execute the query
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )

        # 3e. Process the response and add citations
        final_text = add_citations(response)

        print("\n[RESULT] Grounded Response:")
        print(final_text)

        # 3f. Display metadata for debugging/verification
        if response.candidates and response.candidates[0].grounding_metadata:
            metadata = response.candidates[0].grounding_metadata
            print("\n[METADATA] Search Queries Used:")
            for query in metadata.web_search_queries:
                print(f" - Web Search: {query}")
            
            print("\n[METADATA] Sources Cited:")
            for i, chunk in enumerate(metadata.grounding_chunks):
                source_type = "Web" if chunk.web else "File"
                title = chunk.web.title if chunk.web else chunk.file.display_name
                print(f" - [{i+1}] ({source_type}): {title}")

    except Exception as e:
        print(f"\n[ERROR] An error occurred during content generation: {e}")

# --- 4. Execution Logic ---

if __name__ == "__main__":
    DOC_FILE = "research_docs.txt"
    STORE_DISPLAY_NAME = "Project-Chimera-Docs-Store"

    # Step 1: Set up the internal knowledge base (RAG)
    store_id = setup_file_search_store(client, DOC_FILE, STORE_DISPLAY_NAME)
    
    if store_id:
        # Step 2: Run a hybrid query requiring both internal and external knowledge
        # The model must search the web for the latest Python version AND 
        # consult the internal docs for Project Chimera details.
        hybrid_prompt = (
            "What is the latest major stable version of Python, and who was the "
            "lead engineer for the ZeroMQ implementation in Project Chimera?"
        )
        run_research_query(hybrid_prompt, store_id)

        # Step 3: Run a purely external (web) query
        web_only_prompt = "What were the key announcements at the last major AI conference?"
        run_research_query(web_only_prompt, store_id)

        # Step 4: Run a purely internal (RAG) query
        rag_only_prompt = "What communication protocol does Project Chimera 2.1.0 use?"
        run_research_query(rag_only_prompt, store_id)
        
        # Step 5: Cleanup (optional but recommended for resource management)
        print(f"\n[CLEANUP] Deleting File Search Store: {store_id}")
        client.file_search_stores.delete(name=store_id)
        os.remove(DOC_FILE)
        print("[CLEANUP] Cleanup complete.")


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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
import os
import time

# 1. Client Initialization (Requires GEMINI_API_KEY environment variable)
# The client object provides access to all API services, including 'files'.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Ensure the GEMINI_API_KEY is correctly set.")
    exit()

# Define a placeholder path for a large file (e.g., a 30MB PDF document)
LOCAL_FILE_PATH = "path/to/large_rag_corpus.pdf" 
MODEL_NAME = "gemini-2.5-flash"

# --- A. Upload Operation ---
print(f"1. Attempting to upload file: {LOCAL_FILE_PATH}")
uploaded_file = None
try:
    # client.files.upload() handles the heavy lifting of data transfer 
    # and server-side indexing/processing.
    uploaded_file = client.files.upload(file=LOCAL_FILE_PATH)
    
    # The 'uploaded_file' object now holds the critical metadata, 
    # including the unique name/ID.
    print(f"File uploaded successfully.")
    print(f"  > File Name (ID): {uploaded_file.name}")
    print(f"  > MIME Type: {uploaded_file.mimeType}")
    print(f"  > Size: {uploaded_file.sizeBytes / (1024*1024):.2f} MB")

except FileNotFoundError:
    print(f"Error: Local file not found at {LOCAL_FILE_PATH}. Please create a placeholder file.")
    # We exit here in a real script if the file doesn't exist
    # For this theoretical blueprint, we'll simulate the next steps.
    pass
except Exception as e:
    print(f"An error occurred during file upload: {e}")
    # Simulate a successful upload for the subsequent steps if the upload failed 
    # due to a missing file in this theoretical context.
    class MockFile:
        name = "files/mock-12345"
        mimeType = "application/pdf"
        sizeBytes = 35000000 # 35MB
    uploaded_file = MockFile()


# --- B. Verification Operation (Get Metadata) ---
if uploaded_file:
    print("\n2. Verifying file metadata...")
    try:
        # We retrieve the file metadata using the unique name/ID.
        fetched_file = client.files.get(name=uploaded_file.name)
        print(f"File status confirmed: {fetched_file.name} is ready.")
    except Exception as e:
        print(f"Could not retrieve file metadata: {e}")


# --- C. Generation Operation (RAG) ---
if uploaded_file:
    print("\n3. Using the uploaded file for Retrieval-Augmented Generation (RAG).")
    RAG_PROMPT = "Based ONLY on the uploaded corpus, summarize the key findings regarding Q3 revenue projections and list any contradictory statements found."
    
    try:
        # The contents list now contains two parts:
        # 1. The text instruction (the prompt).
        # 2. The File object (the reference to the large corpus).
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=[
                RAG_PROMPT, 
                uploaded_file # The File object is passed directly as a content part
            ]
        )
        
        print("\n--- Model Response (RAG Output) ---")
        print(response.text)
        print("-----------------------------------\n")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")


# --- D. Lifecycle Management (List and Delete) ---
if uploaded_file:
    # 4. List all active files (Inventory check)
    print("4. Current active files in the project:")
    for f in client.files.list():
        print(f"  > {f.name} ({f.mimeType})")
    
    # 5. Delete the file (Cleanup)
    print(f"\n5. Deleting uploaded file: {uploaded_file.name}")
    try:
        # Manual deletion is crucial for managing the 20 GB quota and sensitive data.
        client.files.delete(name=uploaded_file.name)
        print("File deleted successfully.")
    except Exception as e:
        print(f"Could not delete file: {e}")

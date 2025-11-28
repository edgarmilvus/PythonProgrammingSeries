
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
from google.genai.errors import APIError

# --- Configuration and Setup ---
# Initialize the Gemini client.
# Ensure the GEMINI_API_KEY environment variable is configured.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    exit()

# Define the name and path for our mock document
LOCAL_FILE_PATH = "corporate_policy_draft.txt"
MODEL_NAME = "gemini-2.5-flash" # A fast, multimodal model suitable for RAG

# --- Step 1: Create a local placeholder file ---
# We simulate the existence of a proprietary document locally.
print(f"1. Creating mock file: {LOCAL_FILE_PATH}")
document_content = (
    "Project Zenith Policy Draft v1.2:\n"
    "Section 1.0: Access Control - All access keys expire after 90 days.\n"
    "Section 2.0: Deployment - Production deployment must occur only between 2 AM and 4 AM UTC.\n"
    "Section 3.0: Auditing - All code changes require two separate manager approvals."
)
with open(LOCAL_FILE_PATH, "w") as f:
    f.write(document_content)
print("   Mock document created successfully.")

uploaded_file = None
try:
    # --- Step 2: Upload the file to the Files API ---
    print("\n2. Uploading file to Gemini Files API...")
    # The client.files.upload method handles the entire upload process.
    uploaded_file = client.files.upload(file=LOCAL_FILE_PATH)
    print(f"   Upload successful. File Name (ID): {uploaded_file.name}")
    print(f"   File URI: {uploaded_file.uri}")

    # The file might be in a 'PROCESSING' state; we wait for it to be 'ACTIVE'.
    # This is crucial for large files (e.g., videos or large PDFs).
    print("   Waiting for file processing to complete...")
    while client.files.get(name=uploaded_file.name).state == 'PROCESSING':
        time.sleep(5)
        print("   ...still processing...")

    # --- Step 3: Verify the file metadata ---
    print("\n3. Retrieving uploaded file metadata for verification...")
    # Use client.files.get to retrieve the remote metadata using the file name (ID).
    file_metadata = client.files.get(name=uploaded_file.name)
    print(f"   Display Name: {file_metadata.display_name}")
    print(f"   MIME Type: {file_metadata.mime_type}")
    print(f"   Size Bytes: {file_metadata.size_bytes}")
    print(f"   State: {file_metadata.state}")

    # --- Step 4: Use the uploaded file for RAG/Generation ---
    # We pass both the text prompt and the file object directly into the contents list.
    print("\n4. Generating content using the uploaded document...")
    rag_prompt = "Based *only* on the provided policy document, what is the mandatory time window for production deployment?"

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[rag_prompt, uploaded_file] # The file object acts as the context
    )

    print("\n--- Model Response (Grounded in Document) ---")
    print(response.text)
    print("---------------------------------------------")

    # --- Step 4b: Listing all active files ---
    print("\n4b. Listing all files currently uploaded to the service:")
    for f in client.files.list():
        print(f"   - {f.name} (Type: {f.mime_type})")


except APIError as e:
    print(f"\n[API ERROR] A Gemini API operation failed: {e}")
except Exception as e:
    print(f"\n[GENERAL ERROR] An unexpected error occurred: {e}")

finally:
    # --- Step 5: Clean up (Delete the file) ---
    if uploaded_file:
        print(f"\n5. Deleting uploaded file: {uploaded_file.name}")
        # Manual deletion is best practice, even though files expire automatically.
        client.files.delete(name=uploaded_file.name)
        print("   File deleted successfully.")

    # Remove the local file created for the example
    if os.path.exists(LOCAL_FILE_PATH):
        os.remove(LOCAL_FILE_PATH)
        print(f"   Removed local file: {LOCAL_FILE_PATH}")

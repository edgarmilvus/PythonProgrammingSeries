
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
import pathlib
import tempfile
from google import genai
from google.genai.errors import APIError

# --- CONFIGURATION ---
MODEL_NAME = "gemini-2.5-flash"
# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    exit()

# --- UTILITY FUNCTIONS FOR CORPUS MANAGEMENT ---

def create_mock_files(temp_dir):
    """
    Simulates the creation of a proprietary corpus (PDF and TXT files)
    in a temporary directory for safe demonstration.
    Returns a list of file paths.
    """
    print("1. Creating mock proprietary files...")
    
    # Mock PDF Content (Simulated Legal Precedent)
    pdf_content = (
        "Document: Case Law Review 2024-A. "
        "Section 4.1: The Doctrine of Reasonable Expectation. "
        "In the matter of 'Smith vs. Acme Corp', the court ruled that "
        "any contract provision must be interpreted based on what a "
        "reasonable layperson would expect, regardless of hidden technical jargon. "
        "This precedent is critical for interpreting liability clauses. "
        "The deadline for appeal is set for Q3 2024."
    )
    pdf_path = pathlib.Path(temp_dir) / "legal_precedent.pdf"
    # Note: We save it as a TXT file for simplicity, but name it .pdf
    # to simulate a document file type upload. Gemini handles the content.
    with open(pdf_path, 'w', encoding='utf-8') as f:
        f.write(pdf_content)
    
    # Mock TXT Content (Simulated Internal Memo)
    txt_content = (
        "Internal Memo: Liability Clause Interpretation. "
        "Based on the 'Smith vs. Acme Corp' ruling, all new client contracts "
        "must explicitly define 'reasonable expectation' or risk judicial reinterpretation. "
        "We are prioritizing contract review for all clients in the tech sector. "
        "The primary contact for this review is Jane Doe."
    )
    txt_path = pathlib.Path(temp_dir) / "internal_memo.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)

    print(f"   -> Created {pdf_path.name} and {txt_path.name}")
    return [str(pdf_path), str(txt_path)]

def upload_corpus(client: genai.Client, file_paths: list) -> list:
    """
    Uploads a list of local files to the Gemini Files API.
    Returns a list of uploaded File objects.
    """
    uploaded_files = []
    print("\n2. Starting corpus upload to Gemini Files API...")
    for path in file_paths:
        try:
            # Use the official documentation method for upload
            file_obj = client.files.upload(file=path)
            uploaded_files.append(file_obj)
            print(f"   -> Successfully uploaded: {pathlib.Path(path).name}")
            print(f"      File Name (ID): {file_obj.name}")
            print(f"      Mime Type: {file_obj.mime_type}")
        except APIError as e:
            print(f"   -> ERROR uploading {path}: {e}")
            
    return uploaded_files

def list_and_verify_files(client: genai.Client):
    """
    Lists all files currently uploaded to the project and prints their names.
    """
    print("\n3. Verifying uploaded files in the system...")
    file_count = 0
    for f in client.files.list():
        print(f"   - Found File: {f.name} (Display: {f.display_name})")
        file_count += 1
    print(f"   -> Total files currently active: {file_count}")

def perform_rag_query(client: genai.Client, files: list):
    """
    Executes a generation request, grounding the model's answer
    using the provided list of uploaded File objects.
    """
    print("\n4. Performing RAG Query...")
    
    # The user prompt requires information synthesis from both documents
    rag_prompt = (
        "Based ONLY on the provided documents, summarize the 'Smith vs. Acme Corp' precedent "
        "and identify the internal contact responsible for contract review related to this ruling."
    )
    
    # Construct the contents list: [Text Prompt, File 1 Object, File 2 Object, ...]
    # The SDK automatically handles converting the file objects into the correct API parts.
    contents = [rag_prompt] + files
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        
        print("\n--- MODEL RESPONSE (Grounded RAG) ---")
        print(response.text)
        print("--------------------------------------")
        
    except APIError as e:
        print(f"   -> ERROR during generation: {e}")
    except Exception as e:
        print(f"   -> An unexpected error occurred: {e}")


def cleanup_corpus(client: genai.Client, files: list):
    """
    Deletes all files uploaded during this session to ensure proper resource management.
    """
    print("\n5. Cleaning up uploaded files...")
    if not files:
        print("   -> No files to delete.")
        return

    for file_obj in files:
        try:
            # Use the official documentation method for deletion
            client.files.delete(name=file_obj.name)
            print(f"   -> Successfully deleted file: {file_obj.name}")
        except APIError as e:
            print(f"   -> ERROR deleting file {file_obj.name}: {e}")

# --- MAIN EXECUTION LOGIC ---

def main_rag_workflow():
    """
    Runs the complete RAG corpus management workflow.
    """
    uploaded_file_objects = []
    
    # Use tempfile.TemporaryDirectory to ensure files are cleaned up from the local system
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Step 1: Create local files
            local_file_paths = create_mock_files(temp_dir)
            
            # Step 2: Upload files to Gemini
            uploaded_file_objects = upload_corpus(client, local_file_paths)
            
            if not uploaded_file_objects:
                print("\nFATAL: Could not upload files. Aborting RAG query.")
                return
            
            # Step 3: Verify upload (optional but good practice)
            list_and_verify_files(client)
            
            # Step 4: Execute RAG query
            perform_rag_query(client, uploaded_file_objects)

        finally:
            # Step 5: Clean up all uploaded files, even if an error occurred earlier
            cleanup_corpus(client, uploaded_file_objects)

if __name__ == "__main__":
    main_rag_workflow()


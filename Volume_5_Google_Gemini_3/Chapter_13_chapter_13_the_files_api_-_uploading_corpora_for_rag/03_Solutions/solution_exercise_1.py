
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
import json
from google import genai
from google.genai.errors import APIError

# --- Configuration and Setup ---

# Initialize the client (assumes GEMINI_API_KEY is set in environment variables)
try:
    # Initialize the client
    client = genai.Client()
    print("Gemini client initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure your GEMINI_API_KEY environment variable is set correctly.")
    exit()

# Define file paths for the exercises
FILE_PATHS = {
    "q1_report": "project_report_q1.txt",
    "q2_report": "project_report_q2.txt",
    "policy_manual": "policy_manual.pdf",
    "audio_sample": "audio_sample.mp3"
}

# Simulate creating the necessary dummy files locally
print("\n--- Setting up local dummy files ---")
try:
    # Text files with content for RAG
    with open(FILE_PATHS["q1_report"], "w") as f:
        f.write("Q1 Sales Report: Revenue increased by 15%. Key expense was travel budget ($50,000).")
    with open(FILE_PATHS["q2_report"], "w") as f:
        f.write("Q2 Sales Projection: Expect 20% revenue growth. New vacation policy costs are projected at $15,000.")
    # Placeholder files for PDF and Audio (MIME type is inferred or set by API)
    open(FILE_PATHS["policy_manual"], "a").close()
    open(FILE_PATHS["audio_sample"], "a").close()
    print("Local files created successfully.")
except Exception as e:
    print(f"Could not create dummy files: {e}")
    exit()


# --- Exercise 1: Robust File Upload and Metadata Validation ---

def upload_and_validate_file(file_path: str):
    """Uploads a file, validates metadata, and guarantees deletion using try...finally."""
    uploaded_file = None
    print(f"\n{'='*50}\nRunning Exercise 1: Robust Upload and Validation ({file_path})\n{'='*50}")
    
    try:
        # 1. Upload the file
        print(f"Uploading file: {file_path}...")
        uploaded_file = client.files.upload(file=file_path)
        
        # 2. Retrieve metadata using the file name
        file_name = uploaded_file.name
        print(f"Upload successful. File Name (ID): {file_name}")
        
        # Give the service a moment to process (optional but good practice)
        time.sleep(1) 
        
        retrieved_metadata = client.files.get(name=file_name)
        
        # 3. Print validation details
        print("\n--- Metadata Validation ---")
        print(f"Display Name: {retrieved_metadata.display_name}")
        print(f"MIME Type: {retrieved_metadata.mime_type}")
        print(f"File URI (for prompting): {retrieved_metadata.uri}")
        
    except APIError as e:
        print(f"An API error occurred during upload or retrieval: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        # 4. Guaranteed deletion using the finally block
        if uploaded_file:
            try:
                client.files.delete(name=uploaded_file.name)
                print(f"\nCleanup successful: Deleted file {uploaded_file.name}")
            except APIError as e:
                print(f"Error during final cleanup of {uploaded_file.name}: {e}")

upload_and_validate_file(FILE_PATHS["policy_manual"])


# --- Exercise 2: Inventory Management – Listing and Targeted Deletion ---

def manage_corpus_inventory():
    """Uploads files, lists all, and performs targeted deletion."""
    uploaded_names = []
    print(f"\n{'='*50}\nRunning Exercise 2: Inventory Management\n{'='*50}")
    
    try:
        # 1. Upload two distinct files
        f1 = client.files.upload(file=FILE_PATHS["q1_report"])
        f2 = client.files.upload(file=FILE_PATHS["q2_report"])
        uploaded_names.append(f1.name)
        uploaded_names.append(f2.name)
        print(f"Uploaded files: {f1.name} and {f2.name}")
        time.sleep(1) 

        # 2. & 3. Use client.files.list() to retrieve all files and print details
        print("\n--- Current File Inventory (client.files.list()) ---")
        
        # client.files.list() returns an iterable
        all_files_listed = list(client.files.list()) 
        print(f"Total files found in inventory: {len(all_files_listed)}")
        
        for f in all_files_listed:
            # Conditional check for targeted management
            status = "(TARGETED FOR DELETION)" if f.name in uploaded_names else "(OTHER FILE)"
            print(f"  {status} ID: {f.name}, Display Name: {f.display_name}")

    except APIError as e:
        print(f"An API error occurred during file operations: {e}")
        
    finally:
        # 4. Targeted cleanup routine
        print("\n--- Targeted Cleanup ---")
        for name_to_delete in uploaded_names:
            try:
                client.files.delete(name=name_to_delete)
                print(f"Successfully deleted: {name_to_delete}")
            except APIError as e:
                print(f"Failed to delete {name_to_delete}. It may have already expired or been deleted: {e}")

manage_corpus_inventory()


# --- Exercise 3: Multi-File RAG Corpus Management (Advanced Modification) ---

def run_multi_file_rag():
    """Uploads multiple files, queries them simultaneously in a RAG context, and cleans up."""
    rag_corpus = []
    print(f"\n{'='*50}\nRunning Exercise 3: Multi-File RAG Query\n{'='*50}")
    
    try:
        # 1. Upload two different files and store the File objects
        print("Uploading policy manual...")
        file_policy = client.files.upload(file=FILE_PATHS["policy_manual"])
        rag_corpus.append(file_policy)
        
        print("Uploading Q1 report...")
        file_q1 = client.files.upload(file=FILE_PATHS["q1_report"])
        rag_corpus.append(file_q1)
        
        print(f"Corpus size: {len(rag_corpus)} files uploaded.")
        time.sleep(1)

        # 2. Construct the prompt and contents list
        prompt_text = (
            "Based on the provided documents (policy manual and Q1 report), "
            "synthesize the overall financial impact of the new vacation policy "
            "when considering the Q1 travel budget. Provide a concise summary."
        )
        
        # The contents list includes the text prompt and all File objects (multimodal input)
        # Order: [Text, File1, File2]
        contents = [prompt_text] + rag_corpus 
        
        # 3. Execute the generation request
        print("\nSending multi-file RAG query to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=contents
        )
        
        print("\n--- Gemini Response (Synthesized RAG) ---")
        print(response.text)
        
    except APIError as e:
        print(f"An API error occurred during RAG or upload: {e}")
        
    finally:
        # 4. Comprehensive cleanup routine
        print("\n--- RAG Corpus Cleanup ---")
        for f_obj in rag_corpus:
            try:
                client.files.delete(name=f_obj.name)
                print(f"Deleted RAG file: {f_obj.name}")
            except APIError as e:
                print(f"Failed to delete {f_obj.name}: {e}")

run_multi_file_rag()


# --- Exercise 4: Structured Multimodal Prompting with Audio ---

def structured_audio_prompting():
    """Uploads an audio file and asks for structured analysis following best practices."""
    uploaded_audio = None
    print(f"\n{'='*50}\nRunning Exercise 4: Structured Multimodal Prompting (Audio)\n{'='*50}")

    try:
        # 1. Upload the audio file
        print(f"Uploading audio file: {FILE_PATHS['audio_sample']}...")
        # Note: Even though the file is empty, the API accepts the upload for demonstration
        uploaded_audio = client.files.upload(file=FILE_PATHS["audio_sample"])
        print(f"Audio file uploaded successfully. ID: {uploaded_audio.name}")
        time.sleep(1)

        # 2. Construct the detailed, structured prompt (putting media first)
        detailed_prompt = [
            uploaded_audio, # Best practice: place single media input first
            (
                "Analyze the provided audio clip. Follow these steps precisely: "
                "1. Identify the main theme or type of sound (e.g., music, speech, nature). "
                "2. Provide a simulated brief transcription of the first 10 seconds of the clip. "
                "3. Output the final answer STRICTLY in the following JSON format: "
                '{"theme": "...", "transcription_summary": "...", "confidence_score": "..."}'
            )
        ]

        # 3. Execute the generation request
        print("\nSending structured audio analysis query to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=detailed_prompt
        )
        
        print("\n--- Structured JSON Response ---")
        # Attempt to parse and pretty print the JSON response for readability
        try:
            parsed_json = json.loads(response.text.strip().replace("
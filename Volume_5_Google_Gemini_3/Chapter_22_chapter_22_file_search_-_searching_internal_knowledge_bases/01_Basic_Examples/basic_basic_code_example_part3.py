
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

# Source File: basic_basic_code_example_part3.py
# Description: Basic Code Example
# ==========================================

# Example of Custom Chunking Configuration (This replaces the upload step in the main script)

# --- 3. UPLOAD, CHUNK, AND INDEX THE FILE WITH CUSTOM SETTINGS ---
print("\n--- 3. UPLOADING WITH CUSTOM CHUNKING CONFIGURATION ---")

# We configure the chunking to be more granular:
# Max 200 tokens per chunk, with 20 tokens of overlap between chunks.
custom_chunking_config = {
    'chunking_config': {
      'white_space_config': {
        'max_tokens_per_chunk': 200,
        'max_overlap_tokens': 20
      }
    }
}

operation = client.file_search_stores.upload_to_file_search_store(
    file=FILE_NAME,
    file_search_store_name=store_name,
    config={
        'display_name': f'Internal-{FILE_NAME}',
        **custom_chunking_config # Merging the chunking config into the main config dict
    }
)

# ... (The polling loop remains identical) ...

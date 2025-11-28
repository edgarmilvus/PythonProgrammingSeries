
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

# Source File: theory_theoretical_foundations_part3.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
from google.genai.types import GenerateContentConfig

# Configuration Details
MODEL_ID = "gemini-2.5-flash"

# URLs for comparison (Example: Two different documentation pages or articles)
URL_A = "https://ai.google.dev/gemini-api/docs/url-context"
URL_B = "https://ai.google.dev/gemini-api/docs/grounding"

# 1. Initialize the client (assumes GEMINI_API_KEY is set in the environment)
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    exit()

# 2. Define the tools configuration, explicitly enabling URL Context
tools_config = [
    {"url_context": {}},
]

# 3. Construct the prompt, embedding the target URLs directly into the text
prompt = (
    f"Analyze and compare the primary differences between the functionality "
    f"described in the documentation at {URL_A} and the documentation at {URL_B}. "
    f"Focus specifically on the input requirements for each tool."
)

print(f"--- Sending Request to {MODEL_ID} ---")
print(f"Prompt: {prompt}\n")

# 4. Execute the API call with the tools configuration
try:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=GenerateContentConfig(
            tools=tools_config,
        )
    )

    # 5. Print the model's synthesized response
    print("--- Model Response (Comparison) ---")
    for part in response.candidates[0].content.parts:
        print(part.text)

    # 6. Verify the grounding sources using the metadata
    print("\n--- URL Context Metadata (Verification) ---")
    metadata = response.candidates[0].url_context_metadata
    
    if metadata and metadata.url_metadata:
        for url_info in metadata.url_metadata:
            status = url_info.url_retrieval_status
            retrieved_url = url_info.retrieved_url
            print(f"  URL: {retrieved_url}")
            print(f"  Status: {status}")
    else:
        print("No URL context metadata found.")

    # 7. Display token usage for cost analysis
    print("\n--- Usage Statistics ---")
    usage = response.usage_metadata
    if usage:
        print(f"Total Tokens Used: {usage.total_token_count}")
        # Note: 'tool_use_prompt_token_count' reflects the size of the retrieved web content
        print(f"Tokens from Web Content: {usage.tool_use_prompt_token_count}")

except Exception as e:
    print(f"\nAn error occurred during content generation: {e}")


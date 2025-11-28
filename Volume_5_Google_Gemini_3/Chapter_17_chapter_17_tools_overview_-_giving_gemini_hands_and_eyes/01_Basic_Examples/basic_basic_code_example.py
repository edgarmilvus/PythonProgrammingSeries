
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
from google import genai
from google.genai import types

# --- Configuration ---
# Ensure your GEMINI_API_KEY is set in your environment variables.

def get_real_time_answer(prompt: str):
    """
    Generates a response using the Gemini model, explicitly enabling the 
    built-in Google Search tool for real-time grounding.
    """
    print("--- 1. Initializing Client and Model ---")
    try:
        # Initialize the client. It automatically picks up the API key 
        # from the environment variable.
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing client: {e}")
        print("Please ensure the GEMINI_API_KEY is set correctly.")
        return

    # We use a model optimized for complex reasoning and tool use.
    MODEL_NAME = 'gemini-2.5-flash'
    
    # --- 2. Defining the Tool ---
    # Built-in tools are enabled by creating a types.Tool object 
    # and specifying the tool type (e.g., google_search).
    # We do not need to provide schemas or definitions for built-in tools.
    search_tool = types.Tool(google_search={})
    
    # --- 3. Configuring the Generation Request ---
    # The tools are passed within the GenerateContentConfig object.
    config = types.GenerateContentConfig(
        tools=[search_tool]
    )
    
    print(f"Prompt: '{prompt}'")
    print(f"Tool Enabled: Google Search")
    print("-" * 40)
    
    # --- 4. Making the API Call ---
    # The model decides internally if the tool is necessary, executes the search 
    # on Google's servers, and uses the results to formulate the final answer.
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config
        )

        # --- 5. Outputting the Results ---
        print("\n--- Model Response ---")
        print(response.text)
        print("\n" + "=" * 40)

        # Built-in tools provide metadata showing the grounding sources used.
        if response.candidates and response.candidates[0].grounding_metadata:
            metadata = response.candidates[0].grounding_metadata
            print(f"Grounding Status: Success")
            
            # The grounding chunks provide the specific search results used.
            if metadata.grounding_chunks:
                print(f"Sources Used (Total Chunks: {len(metadata.grounding_chunks)}):")
                # Display the URI of the first source for verification
                for i, chunk in enumerate(metadata.grounding_chunks[:3]):
                    print(f"  Source {i+1}: {chunk.web.uri}")
            else:
                print("No specific web sources detailed in metadata.")
        else:
            print("Grounding Status: No external tool was used for this response.")

    except Exception as e:
        print(f"\nAn error occurred during content generation: {e}")

# --- Execution ---
if __name__ == "__main__":
    # A question requiring very recent, real-time data.
    current_event_prompt = "Summarize the key outcomes of the most recent G7 summit regarding economic sanctions."
    get_real_time_answer(current_event_prompt)


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

from google import genai
from google.genai import types
import os
import textwrap
from IPython.display import display, Markdown

# --- 1. Client Initialization and Setup ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Ensure the GEMINI_API_KEY environment variable is set. Details: {e}")
    exit()

def analyze_sandboxed_data(analysis_prompt: str):
    """
    Sends a prompt to Gemini with the Code Execution tool enabled,
    and parses the multi-part response to show the execution flow.
    """
    print("--- Starting Sandboxed Code Execution Request ---")
    print(f"Prompt: {textwrap.fill(analysis_prompt, width=100)}\n")

    # --- 2. Configuration: Enabling the Code Execution Tool ---
    # This is the critical step that activates the secure sandbox environment.
    config = types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    )

    # --- 3. API Call ---
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # A model supporting code execution
        contents=analysis_prompt,
        config=config,
    )

    # --- 4. Iterative Response Parsing ---
    # The response comes back in multiple 'parts' representing the model's
    # thought process, the generated code, the result, and the summary.

    candidate = response.candidates[0]

    if not candidate.content.parts:
        print("\n[ERROR] No content parts found in the response.")
        return

    print("\n--- Parsing Execution Steps ---")
    
    for i, part in enumerate(candidate.content.parts):
        print(f"\n[Part {i+1}]")

        # A. Standard Text Output (Model's thoughts or final summary)
        if part.text is not None:
            print(f"Type: Model Text/Summary")
            # Use Markdown display for better formatting if running in notebook/Colab
            display(Markdown(part.text))
        
        # B. Executable Code (The code generated and submitted to the sandbox)
        if part.executable_code is not None:
            code = part.executable_code.code
            print(f"Type: Executable Code (Language: {part.executable_code.language})")
            print("--------------------------------------------------")
            print(code.strip())
            print("--------------------------------------------------")

        # C. Code Execution Result (The output returned from the sandbox)
        if part.code_execution_result is not None:
            output = part.code_execution_result.output
            outcome = part.code_execution_result.outcome
            print(f"Type: Sandbox Result (Outcome: {outcome})")
            print("--- Sandbox Standard Output (stdout) ---")
            print(output.strip())
            print("----------------------------------------")
            
        # D. Inline Data (Used for returning generated images/graphs)
        if part.inline_data is not None:
            data = part.inline_data
            mime_type = data.mime_type
            if mime_type.startswith('image/'):
                print(f"Type: Generated Image (MIME: {mime_type})")
                # In a real application, you would decode and save/display the base64 data.
                print(f"[Image Data Received: {len(data.data)} bytes]")
            else:
                print(f"Type: Inline Data (MIME: {mime_type}) - Not Displayed")


# --- 5. Define the Analysis Prompt ---

# We embed the data directly into the prompt and ask for a complex action
# that requires Pandas and Matplotlib, both supported sandbox libraries.
financial_data_prompt = """
I have a list of daily closing prices for a stock:
[150.2, 151.1, 150.5, 152.3, 153.0, 154.5, 153.9, 155.1, 156.0, 155.5]

Please generate Python code to perform the following steps:
1. Load this data into a Pandas Series.
2. Calculate the 5-day Simple Moving Average (SMA).
3. Print both the original prices and the calculated 5-day SMA.
4. Use Matplotlib to plot the original prices and the 5-day SMA on the same graph.
"""

# --- 6. Execute the Function ---
analyze_sandboxed_data(financial_data_prompt)

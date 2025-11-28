
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
import json
from google import genai
from google.genai.errors import APIError

# --- Setup and Utility Functions ---

# Ensure the API key is set
# NOTE: In a production environment, you should secure your API key 
# using environment variables or a secret manager.
if "GEMINI_API_KEY" not in os.environ:
    print("FATAL: Please set the GEMINI_API_KEY environment variable.")
    # In a live environment, you would exit here, but for demonstration, we proceed
    # assuming the environment is correctly configured.

# Initialize the client (using the recommended model for thought signatures)
# Gemini 3 Pro requires strict signature management during function calling.
MODEL_NAME = "gemini-3-pro" 
try:
    client = genai.Client()
except Exception as e:
    print(f"Could not initialize GenAI client: {e}")
    exit()

# 1. Tool Definitions (Used in Exercises 1 and 3)
def get_stock_price(ticker: str) -> dict:
    """Gets the current stock price for a given ticker."""
    if ticker.upper() == "GOOGL":
        return {"price": 175.50, "currency": "USD"}
    return {"error": "Ticker not found"}

def analyze_trade(price: float) -> dict:
    """Analyzes the stock price and returns a trade recommendation."""
    if price > 170.0:
        return {"recommendation": "Sell", "reason": "Price is above recent moving average."}
    return {"recommendation": "Hold", "reason": "Price is stable."}

def get_location_data(city: str) -> dict:
    """Retrieves current data (e.g., temperature) for a city."""
    data = {"Tokyo": "25C, Sunny", "Berlin": "18C, Cloudy"}
    return {"data": data.get(city, "Unknown location")}

# Mapping of tool names to actual functions
TOOL_FUNCTIONS = {
    "get_stock_price": get_stock_price,
    "analyze_trade": analyze_trade,
    "get_location_data": get_location_data
}

# Declarations for the API
FINANCE_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "get_stock_price",
                "description": "Gets the current stock price for a given ticker.",
                "parameters": {"type": "object", "properties": {"ticker": {"type": "string"}}, "required": ["ticker"]}
            },
            {
                "name": "analyze_trade",
                "description": "Analyzes the stock price and returns a trade recommendation.",
                "parameters": {"type": "object", "properties": {"price": {"type": "number"}}, "required": ["price"]}
            }
        ]
    }
]

LOCATION_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "get_location_data",
                "description": "Retrieves current data (e.g., temperature) for a city.",
                "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}
            }
        ]
    }
]

# --- Core Logic for Signature Management ---

def execute_function_calls(function_calls: list) -> list:
    """Executes the list of function calls and returns the function responses."""
    responses = []
    for call in function_calls:
        name = call.name
        args = dict(call.args)
        
        # Execute the corresponding Python function
        result = TOOL_FUNCTIONS.get(name)(**args)
        
        # Create the FunctionResponse part
        responses.append(
            genai.types.Part.from_function_response(
                name=name,
                response=result
            )
        )
    return responses

def extract_signatures_and_calls(response_parts: list) -> tuple[list, list]:
    """
    Extracts function calls and their mandatory thought signatures from 
    a model response, preparing them for re-injection into history.
    
    Returns: (List of original Part objects with signatures, List of FunctionCall objects to execute)
    """
    function_calls_with_signatures_parts = []
    function_calls_to_execute = []
    
    for part in response_parts:
        if part.function_call:
            function_calls_to_execute.append(part.function_call)
            
            # CRITICAL: Store the original Part object. When the SDK serializes 
            # this Part back into the contents list, it correctly preserves 
            # the thoughtSignature field if present.
            function_calls_with_signatures_parts.append(part)
            
    return function_calls_with_signatures_parts, function_calls_to_execute

# ====================================================================
# EXERCISE 1: Sequential Signature Validation (The Two-Step Planner)
# ====================================================================

print("--- EXERCISE 1: Sequential Signature Validation (Two-Step Planner) ---")

user_prompt = "Check the price of GOOGL and recommend a trade."
initial_user_content = genai.types.Content(role="user", parts=[genai.types.Part.from_text(user_prompt)])
history = [initial_user_content]
all_model_parts = [] # Stores all FC parts (with signatures) for history

try:
    # --- Step 1: Get Stock Price (FC1 + Sig A) ---
    print("\n[Turn 1, Step 1] Requesting stock price...")
    response_1 = client.models.generate_content(
        model=MODEL_NAME,
        contents=history,
        config=genai.types.GenerateContentConfig(tools=FINANCE_TOOLS)
    )

    fc_parts_1, calls_to_execute_1 = extract_signatures_and_calls(response_1.candidates[0].content.parts)
    
    # Store FC1 part (includes Sig A)
    all_model_parts.extend(fc_parts_1) 
    
    # Execute tool and generate FR1
    fr_parts_1 = execute_function_calls(calls_to_execute_1)
    print(f"  -> Model called: {calls_to_execute_1[0].name}. Signature A extracted.")

    # --- Step 2: Analyze Trade (FC2 + Sig B) ---
    # History must include: User Prompt, FC1 (with Sig A), FR1
    history_step_2 = [
        initial_user_content,
        genai.types.Content(role="model", parts=all_model_parts), # FC1 + Sig A
        genai.types.Content(role="user", parts=fr_parts_1)        # FR1
    ]
    
    print("[Turn 1, Step 2] Requesting trade analysis, re-injecting Sig A...")
    response_2 = client.models.generate_content(
        model=MODEL_NAME,
        contents=history_step_2,
        config=genai.types.GenerateContentConfig(tools=FINANCE_TOOLS)
    )

    fc_parts_2, calls_to_execute_2 = extract_signatures_and_calls(response_2.candidates[0].content.parts)
    
    # Store FC2 part (includes Sig B)
    all_model_parts.extend(fc_parts_2)
    
    # Execute tool and generate FR2
    fr_parts_2 = execute_function_calls(calls_to_execute_2)
    print(f"  -> Model called: {calls_to_execute_2[0].name}. Signature B extracted.")

    # --- Step 3: Final Response ---
    # History must include: User Prompt, FC1 (Sig A), FR1, FC2 (Sig B), FR2
    # Note: We combine all Model FCs into one Content block for simplicity, 
    # but they are correctly ordered by the history list itself.
    history_step_3 = [
        initial_user_content,
        genai.types.Content(role="model", parts=all_model_parts[:-1]), # FC1 (Sig A)
        genai.types.Content(role="user", parts=fr_parts_1),            # FR1
        genai.types.Content(role="model", parts=all_model_parts[-1:]), # FC2 (Sig B)
        genai.types.Content(role="user", parts=fr_parts_2)             # FR2
    ]
    
    print("[Turn 1, Step 3] Requesting final text output, re-injecting Sig A AND Sig B...")
    response_3 = client.models.generate_content(
        model=MODEL_NAME,
        contents=history_step_3,
        config=genai.types.GenerateContentConfig(tools=FINANCE_TOOLS)
    )

    print("  -> Success! Final Model Response:")
    print(f"     Recommendation: {response_3.text.strip()}")

except APIError as e:
    print(f"FATAL ERROR during sequential call: {e}")
    print("This indicates a failure in signature management (e.g., omitting Sig A or Sig B).")

# ====================================================================
# EXERCISE 2: Parallel Signature Isolation
# ====================================================================

print("\n--- EXERCISE 2: Parallel Signature Isolation ---")

user_prompt_parallel = "What is the current data for Tokyo and Berlin?"
initial_user_content_p = genai.types.Content(role="user", parts=[genai.types.Part.from_text(user_prompt_parallel)])
history_parallel = [initial_user_content_p]

try:
    # --- Step 1: Parallel Calls (FC1 + Sig A, FC2) ---
    print("\n[Turn 1, Step 1] Requesting parallel location data...")
    response_p1 = client.models.generate_content(
        model=MODEL_NAME,
        contents=history_parallel,
        config=genai.types.GenerateContentConfig(tools=LOCATION_TOOLS)
    )

    fc_parts_p1 = response_p1.candidates[0].content.parts
    
    print(f"  -> Model returned {len(fc_parts_p1)} function calls.")
    
    # Inspection: Check the thoughtSignature field explicitly
    
    # Part 1 inspection (Expected: Signature present)
    part1_has_sig = hasattr(fc_parts_p1[0], 'thought_signature') and fc_parts_p1[0].thought_signature
    if part1_has_sig:
        print(f"  -> FC 1 ({fc_parts_p1[0].function_call.name}): Signature FOUND ({fc_parts_p1[0].thought_signature[:10]}...).")
    else:
        print("  -> ERROR: Signature not found on the first function call part (Expected to be mandatory).")
        
    # Part 2 inspection (Expected: Signature absent)
    part2_has_sig = hasattr(fc_parts_p1[1], 'thought_signature') and fc_parts_p1[1].thought_signature
    if not part2_has_sig:
        print(f"  -> FC 2 ({fc_parts_p1[1].function_call.name}): Signature ABSENT (Correct for parallel calls).")
    else:
        print("  -> ERROR: Signature found on the second function call part (Incorrect for parallel calls).")

    # --- Step 2: Send Tool Outputs ---
    # History must preserve the exact structure: FC1 (Sig A), FC2 (No Sig)
    
    calls_to_execute_p1 = [p.function_call for p in fc_parts_p1 if p.function_call]
    fr_parts_p1 = execute_function_calls(calls_to_execute_p1)
    
    # History structure: User Prompt, Model Response (FC1+Sig A, FC2), User Response (FR1, FR2)
    history_step_p2 = [
        initial_user_content_p,
        genai.types.Content(role="model", parts=fc_parts_p1), # FC1 (Sig A) + FC2 (No Sig) - Preserved exactly
        genai.types.Content(role="user", parts=fr_parts_p1)   # FR1 + FR2
    ]

    print("[Turn 1, Step 2] Sending tool outputs, preserving single signature...")
    response_p2 = client.models.generate_content(
        model=MODEL_NAME,
        contents=history_step_p2,
        config=genai.types.GenerateContentConfig(tools=LOCATION_TOOLS)
    )

    print("  -> Success! Final Model Response:")
    print(f"     Summary: {response_p2.text.strip()}")

except APIError as e:
    print(f"FATAL ERROR during parallel call: {e}")
    print("This usually means the structure of FC1 (Sig A) and FC2 (No Sig) was not preserved.")

# ====================================================================
# EXERCISE 3: The Agentic Workflow Challenge (Dummy Signature Injection)
# ====================================================================

print("\n--- EXERCISE 3: Dummy Signature Injection Challenge ---")
# Use the official dummy signature to skip validation for injected history
DUMMY_SIGNATURE = "context_engineering_is_the_way_to_go" 

# 1. Define the simulated history (FC1 + FR1)
# Simulate a previous system executing get_stock_price (FC1)
simulated_fc1 = genai.types.Part(
    function_call=genai.types.FunctionCall(
        name="get_stock_price",
        args={"ticker": "GOOGL"}
    ),
    # CRITICAL: Inject the dummy signature to satisfy Gemini 3 Pro validation
    thought_signature=DUMMY_SIGNATURE 
)

simulated_fr1 = genai.types.Part.from_function_response(
    name="get_stock_price",
    response={"price": 160.0, "currency": "USD"}
)

# 2. Construct the history for the second step
user_prompt_dummy = "Based on the previous stock price check, recommend a trade."
initial_user_content_dummy = genai.types.Content(role="user", parts=[genai.types.Part.from_text(user_prompt_dummy)])

history_dummy = [
    initial_user_content_dummy,
    genai.types.Content(role="model", parts=[simulated_fc1]), # Injected FC1 with Dummy Sig
    genai.types.Content(role="user", parts=[simulated_fr1])  # Injected FR1
]

print(f"\n[Step 1] Attempting to inject history using dummy signature: '{DUMMY_SIGNATURE}'")

try:
    # --- Step 2: Analyze Trade (FC2 + Sig B) ---
    response_dummy = client.models.generate_content(
        model=MODEL_NAME,
        contents=history_dummy,
        config=genai.types.GenerateContentConfig(tools=FINANCE_TOOLS)
    )
    
    fc_parts_2_dummy, calls_to_execute_2_dummy = extract_signatures_and_calls(response_dummy.candidates[0].content.parts)
    
    if calls_to_execute_2_dummy and calls_to_execute_2_dummy[0].name == "analyze_trade":
        print("  -> SUCCESS: Model bypassed validation and correctly called 'analyze_trade'.")
        print(f"     Arguments: {dict(calls_to_execute_2_dummy[0].args)}")
        
        # Verify the model returned a new, real signature for FC2
        real_sig_b = fc_parts_2_dummy[0].thought_signature
        if real_sig_b and real_sig_b != DUMMY_SIGNATURE:
            print(f"     Model returned a new, valid signature for its own FC2: {real_sig_b[:10]}...")
    else:
        print("  -> FAILURE: Model did not proceed to the expected function call.")

except APIError as e:
    print(f"FATAL ERROR: The API returned a 400 error. The dummy signature failed or was omitted: {e}")

# ====================================================================
# EXERCISE 4: Streaming Signature Extraction
# ====================================================================

print("\n--- EXERCISE 4: Streaming Signature Extraction ---")

prompt_streaming = "Explain the concept of quantum entanglement using only analogies related to maritime navigation, then summarize the key points in one sentence."
full_response_text = ""
extracted_signature = None

print("\n[Streaming] Starting stream for complex reasoning task...")

try:
    response_stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=[prompt_streaming]
    )

    for chunk in response_stream:
        # Aggregate text content
        if chunk.text:
            full_response_text += chunk.text
        
        # Check the parts of the chunk for the thought signature
        if chunk.candidates and chunk.candidates[0].content:
            for part in chunk.candidates[0].content.parts:
                # Use hasattr to check for the signature field
                if hasattr(part, 'thought_signature') and part.thought_signature:
                    extracted_signature = part.thought_signature
                    
                    # Log where the signature was found (text or non-text part)
                    if not part.text:
                         print(f"  -> Found signature in a non-text chunk! ({extracted_signature[:10]}...)")
                    else:
                         # This usually happens in the final chunk
                         print(f"  -> Found signature in the final text chunk. ({extracted_signature[:10]}...)")

    print("\n[Streaming Complete] Final Aggregated Text Summary:")
    print("--------------------------------------------------")
    print(full_response_text.strip())
    print("--------------------------------------------------")

    if extracted_signature:
        print(f"Verification: Successfully extracted the thought signature (Length: {len(extracted_signature)}).")
        # Note: This signature is RECOMMENDED, not mandatory, for non-FC turns.
    else:
        print("Verification: Failed to extract the thought signature (Model may not have generated a thought).")

except Exception as e:
    print(f"An error occurred during streaming: {e}")

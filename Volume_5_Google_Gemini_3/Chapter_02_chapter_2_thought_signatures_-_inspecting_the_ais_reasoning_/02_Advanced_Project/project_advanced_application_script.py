
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
import json
import time
from typing import List, Dict, Any, Tuple

# Use the official Google Gen AI SDK
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. ENVIRONMENT SETUP AND INITIALIZATION ---

# Ensure the API key is set in your environment variables
# os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY'

try:
    # Initialize the client. We use the low-level client for manual history management.
    client = genai.Client()
    MODEL_NAME = 'gemini-3.5-pro' # Using a model that supports mandatory signatures
except Exception as e:
    print(f"Error initializing client: {e}")
    exit()

# --- 2. TOOL DEFINITIONS AND SIMULATION FUNCTIONS ---

def check_flight_status(flight_number: str) -> Dict[str, Any]:
    """
    Simulates checking a flight status.
    In a real application, this would be an external API call.
    """
    print(f"\n[TOOL EXECUTION] Checking status for flight: {flight_number}")
    # Simulate a delayed flight scenario to force sequential planning
    if flight_number == "AA100":
        return {
            "status": "Delayed",
            "new_departure_time": "14:00",
            "delay_reason": "Maintenance check"
        }
    return {"status": "On Time", "departure_time": "12:00"}

def book_taxi(time: str, pickup_location: str) -> Dict[str, Any]:
    """
    Simulates booking a taxi service.
    """
    print(f"[TOOL EXECUTION] Booking taxi for {pickup_location} at {time}")
    if "14:00" in time:
        return {"booking_status": "Success", "confirmation_id": "TX9876"}
    return {"booking_status": "Failed", "reason": "Time slot unavailable"}

# Map tool names to their execution functions
TOOL_EXECUTION_MAP = {
    "check_flight_status": check_flight_status,
    "book_taxi": book_taxi
}

# Define the Function Declarations for the model
FLIGHT_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="check_flight_status",
            description="Gets the current status and revised schedule for a specific flight.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "flight_number": types.Schema(type=types.Type.STRING, description="The specific flight identifier (e.g., AA100).")
                },
                required=["flight_number"]
            )
        )
    ]
)

TAXI_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="book_taxi",
            description="Books a taxi service for a specific time and location.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "time": types.Schema(type=types.Type.STRING, description="The desired pickup time in 24-hour format."),
                    "pickup_location": types.Schema(type=types.Type.STRING, description="The location for pickup.")
                },
                required=["time", "pickup_location"]
            )
        )
    ]
)

ALL_TOOLS = [FLIGHT_TOOL, TAXI_TOOL]

# --- 3. CORE LOGIC: MANUAL SIGNATURE MANAGEMENT LOOP ---

def execute_agent_workflow(prompt: str, tools: List[types.Tool]):
    """
    Manually manages the conversation history, function calls, and thought signatures
    for a multi-step agentic workflow.
    """
    # History starts with the initial user prompt
    conversation_history: List[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(prompt)]
        )
    ]
    
    print(f"--- STARTING AGENT WORKFLOW ---")
    print(f"[Turn 1, Step 1] Initial Prompt: {prompt}")

    # The agent loop continues until the model returns a text response (no more function calls)
    step_count = 1
    
    while True:
        print(f"\n--- STEP {step_count} EXECUTION ---")
        
        try:
            # 1. Send the current history and tools to the model
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=conversation_history,
                config=types.GenerateContentConfig(tools=tools)
            )

        except APIError as e:
            print(f"\n[CRITICAL ERROR] API Call Failed at Step {step_count}.")
            print("This often indicates a missing thoughtSignature in the history.")
            print(f"Error details: {e}")
            break
        
        # Check if the model returned a final text response
        if not response.candidates or not response.candidates[0].content.parts:
            print("[ERROR] Model returned no content.")
            break

        model_content = response.candidates[0].content
        
        # Check for function calls (Agentic Decision)
        function_calls = [
            part.function_call for part in model_content.parts 
            if part.function_call
        ]

        if not function_calls:
            # 2. Final step: Model returns text output
            final_text = model_content.parts[0].text
            print(f"[Model Response] Final Text Output:\n{final_text}")
            
            # Optional: Check for non-FC thought signature (recommended but not mandatory)
            if model_content.parts[-1].thought_signature:
                print(f"[Signature Note] Final text part included a signature (Optional to return).")
            
            print("\n--- WORKFLOW COMPLETE ---")
            break

        # 3. Process Function Calls and Signatures (Turn 1, Step X)
        
        # Prepare the parts list to be appended to history
        history_parts_to_append: List[types.Part] = []
        function_responses_to_send: List[types.Part] = []
        
        print(f"[Model Decision] {len(function_calls)} function call(s) detected.")

        # Iterate through the model's response parts to extract calls and signatures
        for i, part in enumerate(model_content.parts):
            
            # A. Extract the Function Call (FC)
            if part.function_call:
                fc = part.function_call
                
                # B. Extract the Thought Signature (TS)
                # CRITICAL: If a function call exists, check for the signature.
                # Per docs, only the *first* FC in a parallel response needs it, 
                # but in sequential, the first FC of *each step* needs it.
                
                signature = getattr(part, 'thought_signature', None)
                
                if signature:
                    print(f"   > Found mandatory thoughtSignature: {signature[:10]}...")
                elif i == 0 and len(function_calls) > 0:
                    # This should trigger a critical error if the model behaved correctly
                    print("[WARNING] First function call of the step is missing a signature.")

                # C. Reconstruct the Model Part for History (MUST preserve signature)
                # We create a new Part object that mirrors the model's response exactly
                history_part = types.Part(
                    function_call=fc,
                    thought_signature=signature  # This is the critical re-injection
                )
                history_parts_to_append.append(history_part)

                # D. Execute the tool locally and prepare the Function Response (FR)
                func_name = fc.name
                func_args = json.loads(fc.args) # Args are often returned as a string/dict structure
                
                if func_name in TOOL_EXECUTION_MAP:
                    # Execute the simulated function
                    tool_output = TOOL_EXECUTION_MAP[func_name](**func_args)
                    
                    print(f"   > Executed {func_name}. Output: {tool_output['status']}")
                    
                    # Create the function response part (Role: user)
                    fr_part = types.Part.from_function_response(
                        name=func_name,
                        response=tool_output
                    )
                    function_responses_to_send.append(fr_part)
                else:
                    print(f"[ERROR] Unknown function: {func_name}")

        # 4. Update History for the Next Step (Turn 1, Step X+1)
        
        # Append the Model's decision (FCs + Signatures) to the history
        # This is a single 'model' block containing all FC parts
        conversation_history.append(
            types.Content(
                role="model",
                parts=history_parts_to_append
            )
        )
        
        # Append the User's function execution results (FRs) to the history
        # This is a single 'user' block containing all FR parts
        conversation_history.append(
            types.Content(
                role="user",
                parts=function_responses_to_send
            )
        )
        
        print(f"[History Update] Appended Model FCs (with signatures) and User FRs.")
        step_count += 1
        time.sleep(0.5) # Throttle requests

# --- 4. EXECUTION ---

if __name__ == "__main__":
    
    COMPLEX_PROMPT = "I need to check flight AA100 status. If it is delayed, please book a taxi pickup at the airport at the new arrival time."
    
    # Execute the workflow
    execute_agent_workflow(COMPLEX_PROMPT, ALL_TOOLS)


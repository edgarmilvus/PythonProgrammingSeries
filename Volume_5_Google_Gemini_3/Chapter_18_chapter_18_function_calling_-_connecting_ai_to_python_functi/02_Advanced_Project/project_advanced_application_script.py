
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
from typing import Dict, Any, List
from google import genai
from google.genai import types

# --- 1. MOCK EXTERNAL FUNCTIONS (The "Tools" the AI will call) ---

def get_inventory_level(product_id: str) -> Dict[str, int]:
    """
    Simulates querying a database (e.g., via SQLAlchemy) for current stock.
    Returns the stock level for a given product ID.
    """
    print(f"\n[TOOL EXECUTION] Querying database for Product ID: {product_id}...")
    
    # Mock data source: Low stock for P-404, high stock for P-101
    mock_inventory = {
        "P-404": 50,  # Low stock
        "P-101": 500, # High stock
        "P-999": 120  # Borderline stock
    }
    
    level = mock_inventory.get(product_id, 0)
    print(f"[TOOL RESULT] Found stock level: {level} units.")
    return {"stock_level": level, "product_id": product_id}

def schedule_follow_up(attendees: List[str], topic: str) -> Dict[str, str]:
    """
    Simulates calling an external API (e.g., Google Calendar API) to schedule a meeting.
    Returns a confirmation message.
    """
    print(f"\n[TOOL EXECUTION] Scheduling meeting with {', '.join(attendees)}...")
    
    # In a real application, this would involve API calls, error handling, etc.
    if not attendees:
        return {"status": "error", "message": "Cannot schedule meeting without attendees."}
        
    confirmation_id = f"MEET-{hash(topic) % 1000}"
    
    result = {
        "status": "success",
        "confirmation_id": confirmation_id,
        "topic": topic,
        "attendees": attendees,
        "message": f"Meeting '{topic}' successfully scheduled. Confirmation ID: {confirmation_id}"
    }
    print(f"[TOOL RESULT] Scheduling complete: {confirmation_id}")
    return result

# Map function names to the actual callable Python functions
FUNCTION_MAP = {
    "get_inventory_level": get_inventory_level,
    "schedule_follow_up": schedule_follow_up
}

# --- 2. DEFINE FUNCTION DECLARATIONS (Schemas for the AI) ---

# Schema for get_inventory_level
inventory_declaration = {
    "name": "get_inventory_level",
    "description": "Retrieves the current number of units in stock for a specified product ID from the ERP system.",
    "parameters": {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "string",
                "description": "The unique identifier of the product (e.g., 'P-404').",
            },
        },
        "required": ["product_id"],
    },
}

# Schema for schedule_follow_up
schedule_declaration = {
    "name": "schedule_follow_up",
    "description": "Schedules an internal follow-up meeting with team members regarding critical topics like low stock.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of required attendees (e.g., ['Procurement Team', 'Warehouse Manager']).",
            },
            "topic": {
                "type": "string",
                "description": "The subject of the meeting.",
            },
        },
        "required": ["attendees", "topic"],
    },
}

# Bundle all function declarations into a Tool configuration
erp_tools = types.Tool(function_declarations=[inventory_declaration, schedule_declaration])

# --- 3. CORE FUNCTION CALLING LOGIC (Multi-Turn Workflow) ---

def run_multi_turn_function_call(user_prompt: str, client: genai.Client):
    """
    Handles the complete, multi-step conversation required for compositional function calling.
    """
    print("--- Starting AI Conversation Flow ---")
    
    # Configuration: Provide the model with the tools
    config = types.GenerateContentConfig(tools=[erp_tools])
    
    # 1. Initialize conversation history with the user's first prompt
    conversation_history: List[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    # Maximum number of turns to prevent infinite loops
    MAX_TURNS = 5
    
    for turn in range(MAX_TURNS):
        print(f"\n--- Turn {turn + 1}: Calling Gemini ---")
        
        # Send the entire history and tools to the model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_history,
            config=config,
        )
        
        # Check if the model decided to call a function (or multiple functions)
        function_calls = response.candidates[0].content.parts
        
        # Check for direct text response (the final output)
        if response.text and not any(p.function_call for p in function_calls):
            print("\n[FINAL RESPONSE] Model generated a direct text response.")
            print(response.text)
            return

        # --- Execute Function Calls ---
        
        # The model might return multiple function calls (Parallel Function Calling)
        tool_results: List[types.Part] = []
        
        for part in function_calls:
            if part.function_call:
                tool_call = part.function_call
                
                function_name = tool_call.name
                arguments = dict(tool_call.args) # Convert immutable args to dict
                
                print(f"[MODEL REQUEST] Function Call Detected: {function_name}({arguments})")
                
                # Look up and execute the corresponding Python function
                if function_name in FUNCTION_MAP:
                    try:
                        # Execute the function with the arguments provided by the AI
                        result_data = FUNCTION_MAP[function_name](**arguments)
                        
                        # Create the structured function response part
                        function_response_part = types.Part.from_function_response(
                            name=function_name,
                            response={"result": result_data}, # Wrap result in a dict
                        )
                        tool_results.append(function_response_part)
                        
                    except Exception as e:
                        error_message = f"Function execution failed: {str(e)}"
                        print(f"[ERROR] {error_message}")
                        
                        # Send the error back to the model for context
                        error_response_part = types.Part.from_function_response(
                            name=function_name,
                            response={"error": error_message},
                        )
                        tool_results.append(error_response_part)
                else:
                    print(f"[ERROR] Unknown function: {function_name}")
        
        # --- Prepare for the Next Turn ---

        # 1. Append the model's function call request to the history
        # Note: The SDK automatically handles thought signatures when appending the content object.
        conversation_history.append(response.candidates[0].content)
        
        # 2. Append the results of the function execution back to the history
        # This is structured as a 'user' role response containing the tool output
        if tool_results:
            print(f"--- Turn {turn + 1} Complete. Sending {len(tool_results)} function result(s) back to Gemini. ---")
            
            # If multiple results were generated (parallel call), they are bundled here
            function_result_content = types.Content(role="user", parts=tool_results)
            conversation_history.append(function_result_content)
        else:
            # If no function calls were found but no text was returned, something is wrong
            print("[ERROR] Model returned neither text nor function calls. Aborting.")
            return

    print("\n[WARNING] Maximum number of turns reached. Conversation terminated.")


# --- 4. EXECUTION ---

if __name__ == "__main__":
    # Ensure API Key is set
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client()
    
    # Example 1: Compositional/Sequential Function Calling (A multi-turn conversation)
    # The AI must first check inventory, and based on that result, decide to schedule a meeting.
    prompt_sequential = (
        "What is the current stock level for product P-404? "
        "If the stock is below 100 units, schedule a follow-up meeting "
        "with the 'Procurement Team' and 'Warehouse Manager' "
        "about 'Urgent P-404 Restock'."
    )
    print("\n" + "="*80)
    print("EXAMPLE 1: SEQUENTIAL (COMPOSITIONAL) FUNCTION CALLING")
    print("User Prompt:", prompt_sequential)
    print("="*80)
    run_multi_turn_function_call(prompt_sequential, client)

    # Example 2: Parallel Function Calling (A single-turn conversation)
    # The AI should call two independent functions simultaneously.
    prompt_parallel = (
        "What is the inventory level for P-101? Also, schedule a meeting "
        "for the 'Sales Team' regarding 'Q4 Strategy Review'."
    )
    print("\n" + "="*80)
    print("EXAMPLE 2: PARALLEL FUNCTION CALLING (Single Turn, Multiple Calls)")
    print("User Prompt:", prompt_parallel)
    print("="*80)
    run_multi_turn_function_call(prompt_parallel, client)


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

import json
from typing import List, Dict, Any, Union

# --- 1. Mock Function Declarations (Tools) ---

def check_points(user_id: str) -> Dict[str, Any]:
    """Retrieves the current loyalty points for a user."""
    print(f"\n[TOOL EXECUTION] Checking points for {user_id}...")
    # Simulate a result that triggers the next step
    return {"user_id": user_id, "points": 12500, "status": "sufficient"}

def book_flight(flight_id: str, booking_class: str = "Economy") -> Dict[str, Any]:
    """Books a flight based on the provided flight ID."""
    print(f"[TOOL EXECUTION] Attempting to book flight {flight_id} ({booking_class})...")
    # Simulate a successful booking
    return {"flight_id": flight_id, "booking_status": "Success", "confirmation_code": "G3PRO-1A"}

# Map function names to their Python callable objects
TOOL_MAP = {
    "check_points": check_points,
    "book_flight": book_flight
}

# Define the tools in the format required by the API
TOOL_DECLARATIONS = [
    {
        "functionDeclarations": [
            {
                "name": "check_points",
                "description": "Checks a user's loyalty points balance.",
                "parameters": {"type": "object", "properties": {"user_id": {"type": "string"}}, "required": ["user_id"]}
            },
            {
                "name": "book_flight",
                "description": "Books a specified flight ID.",
                "parameters": {"type": "object", "properties": {"flight_id": {"type": "string"}, "booking_class": {"type": "string"}}, "required": ["flight_id"]}
            }
        ]
    }
]

# --- 2. Mock API Client (Simulating the History Management) ---

class MockGeminiClient:
    """
    Simulates the core API interaction, focusing on history management 
    and the explicit handling of thoughtSignatures.
    """
    def __init__(self):
        # The history list that accumulates all turns (User, Model, FunctionResponse)
        self.history: List[Dict[str, Any]] = []

    def _mock_api_call(self, prompt: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulates the model response based on the current history length.
        In a real scenario, this would be client.models.generate_content(...)
        """
        print(f"\n--- API CALL START (History Length: {len(history)}) ---")
        
        # Determine the mock response based on the conversation step
        
        if len(history) == 1:
            # Step 1: User asks, Model responds with first function call (FC1)
            # This is the start of Turn 1. FC1 MUST have a thoughtSignature.
            print("[MOCK] Model initiates FC1 (check_points).")
            return {
                "role": "model",
                "parts": [
                    {
                        "functionCall": {"name": "check_points", "args": {"user_id": "user_99"}},
                        "thoughtSignature": "<Signature_A_PointsCheck>" # MANDATORY SIGNATURE A
                    }
                ]
            }
        
        elif len(history) == 3:
            # Step 2: Model receives FC1 result, responds with second function call (FC2)
            # This is still Turn 1. FC2 MUST have a new thoughtSignature.
            print("[MOCK] Model initiates FC2 (book_flight).")
            return {
                "role": "model",
                "parts": [
                    {
                        "functionCall": {"name": "book_flight", "args": {"flight_id": "AA100"}},
                        "thoughtSignature": "<Signature_B_FlightBooking>" # MANDATORY SIGNATURE B
                    }
                ]
            }
            
        elif len(history) == 5:
            # Step 3: Model receives FC2 result, generates final text output
            # This is the completion of Turn 1.
            print("[MOCK] Model generates final text output.")
            return {
                "role": "model",
                "parts": [
                    {
                        "text": "Your flight AA100 has been successfully booked using your 12500 loyalty points. Confirmation code: G3PRO-1A."
                        # Signature here is optional but recommended (not mandatory for FC completion)
                    }
                ]
            }
        else:
            raise ValueError("Mock API received unexpected history length.")

    def send_message(self, prompt: str = None, function_responses: List[Dict[str, Any]] = None):
        """
        Manages the conversation loop, updating history and calling the mock API.
        """
        
        # 1. Update history with the new user input (if starting a new turn)
        if prompt:
            self.history.append({
                "role": "user",
                "parts": [{"text": prompt}]
            })
            
        # 2. Add function responses (tool outputs) to history (if continuing a turn)
        if function_responses:
            self.history.append({
                "role": "user",
                "parts": function_responses
            })
            
        # 3. Call the API using the current history and tools
        # In a real API call, the tools would be passed here:
        # response = client.models.generate_content(
        #     model='gemini-3-pro', 
        #     contents=self.history, 
        #     tools=TOOL_DECLARATIONS
        # )
        
        response_data = self._mock_api_call(prompt, self.history)
        
        # 4. Update history with the model's response
        self.history.append(response_data)
        
        # 5. Check if the model requested a function call
        function_calls = [
            part.get("functionCall") for part in response_data.get("parts", []) 
            if "functionCall" in part
        ]
        
        if function_calls:
            print(f"\n[MODEL RESPONSE] Function Call(s) detected: {len(function_calls)}")
            
            # --- CRITICAL STEP: EXTRACTING THE THOUGHT SIGNATURE ---
            
            # Find the thought signature(s) to pass back in the next step.
            # In sequential calling, every FC part has a signature (if it's the first in the step).
            
            tool_outputs = []
            
            for i, part in enumerate(response_data["parts"]):
                fc = part.get("functionCall")
                signature = part.get("thoughtSignature")
                
                if fc:
                    # Execute the function using the extracted arguments
                    func_name = fc["name"]
                    func = TOOL_MAP.get(func_name)
                    
                    if not func:
                        raise NotImplementedError(f"Tool {func_name} not found.")
                        
                    # Execute the function
                    tool_result = func(**fc["args"])
                    
                    # Store the result as a functionResponse part
                    tool_outputs.append({
                        "functionResponse": {
                            "name": func_name,
                            "response": tool_result
                        }
                    })
                    
                    # --- CRITICAL STEP: VALIDATION CHECK ---
                    # For Gemini 3 Pro, the signature is MANDATORY for FC parts.
                    if not signature and i == 0:
                        raise RuntimeError("Validation Error: Missing thoughtSignature on the first functionCall part in a step.")
                        
                    print(f"[SIGNATURE TRACE] Extracted Signature: {signature}")
            
            # --- RECURSIVE CALL: Continue the turn with tool outputs ---
            # We call send_message again, passing the tool outputs, but NO new prompt.
            # This keeps us within Turn 1, advancing to the next Step.
            print("\n[AGENT] Continuing Turn 1 (Next Step) by sending tool outputs back...")
            self.send_message(function_responses=tool_outputs)
            
        else:
            # Final text output received
            print("\n--- FINAL MODEL OUTPUT ---")
            print(response_data["parts"][0]["text"])
            print("--------------------------")
            
            return response_data

# --- 3. Execution Flow ---

if __name__ == "__main__":
    client = MockGeminiClient()
    
    initial_prompt = "I need to check my loyalty points, and if I have over 10,000, please book flight AA100 for me."
    
    print("--- STARTING CONVERSATION (Turn 1, Step 1) ---")
    client.send_message(prompt=initial_prompt)

    # After execution, the full history contains the complete trace:
    # [User Prompt, Model FC1 + Sig A, User FR1, Model FC2 + Sig B, User FR2, Model Final Text]
    
    print("\n\n--- FULL CONVERSATION HISTORY (POST-EXECUTION) ---")
    print(json.dumps(client.history, indent=2))

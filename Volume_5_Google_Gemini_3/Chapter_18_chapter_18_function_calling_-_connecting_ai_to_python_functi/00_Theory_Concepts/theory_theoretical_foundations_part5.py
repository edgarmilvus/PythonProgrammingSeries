
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

# Source File: theory_theoretical_foundations_part5.py
# Description: Theoretical Foundations
# ==========================================

# Conceptual Python structures illustrating the core components of Function Calling

from google import genai
from google.genai import types

# --- 1. The Function Declaration (The Recipe Book) ---
# This dictionary defines the structure and rules for the model to follow.
# Note the use of JSON Schema types ('object', 'string', 'array', 'integer').
SCHEDULE_MEETING_DECLARATION = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting (e.g., ['Bob', 'Alice']).",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "topic"],
    },
}

# --- 2. The Actual Python Function (The Sous Chef's Capability) ---
def schedule_meeting(attendees: list[str], date: str, topic: str) -> dict:
    """The function that performs the real-world action."""
    print(f"Executing API call: Scheduling {topic} on {date} for {attendees}.")
    # In a real application, this would call an external API (e.g., Calendar API)
    return {"status": "success", "meeting_id": "Mtg-4567", "details": f"Scheduled for {date}"}

# --- 3. Configuration and Initial Call ---
client = genai.Client()
tools_config = types.Tool(function_declarations=[SCHEDULE_MEETING_DECLARATION])
config = types.GenerateContentConfig(tools=[tools_config])

# User prompt
user_prompt = "Schedule a meeting with Bob and Alice for 03/14/2025 about Q3 planning."
contents = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

# Step 1 & 2: Send request and receive the function call suggestion
response_1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents,
    config=config,
)

# --- 4. Execution Logic (Step 3) ---
if response_1.candidates[0].content.parts[0].function_call:
    function_call = response_1.candidates[0].content.parts[0].function_call
    
    # Dispatcher mechanism: Match the model's request to the local function
    if function_call.name == "schedule_meeting":
        # Execute the function using the model's arguments
        execution_result = schedule_meeting(**function_call.args)
        
        # --- 5. Sending the Result Back (Step 4) ---
        
        # A. Append the model's function call turn to history
        contents.append(response_1.candidates[0].content) 

        # B. Create the function response part
        response_part = types.Part.from_function_response(
            name=function_call.name,
            response={"result": execution_result},
        )
        
        # C. Append the function response in the 'user' role
        contents.append(types.Content(role="user", parts=[response_part]))
        
        # D. Call the model again for final synthesis
        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=config,
            contents=contents,
        )
        
        print("\n--- Final User-Friendly Response ---")
        print(final_response.text)
    else:
        # Handle unrecognized function call
        print(f"Error: Unknown function requested: {function_call.name}")
else:
    print("\n--- Direct Text Response ---")
    print(response_1.text)


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
import math
from google import genai
from google.genai import types

# --- 1. Define the actual Python function (The Tool) ---

def calculate_circle_area(radius: float) -> dict[str, float]:
    """
    Calculates the area of a circle given its radius.

    Args:
        radius: The length of the circle's radius.

    Returns:
        A dictionary containing the calculated area.
    """
    # Ensure the radius is non-negative before calculation
    if radius < 0:
        return {"error": "Radius cannot be negative."}
        
    area = math.pi * (radius ** 2)
    # Return the result in a structured format suitable for the model
    return {"calculated_area": area}

# --- 2. Define the Function Declaration (The Schema) ---

# This JSON structure describes the Python function to the Gemini model.
# It uses a subset of the OpenAPI schema standard.
CALCULATOR_SCHEMA = {
    "name": "calculate_circle_area",
    "description": "Calculates the area of a circle (Area = Pi * radius^2).",
    "parameters": {
        "type": "object",
        "properties": {
            "radius": {
                "type": "number",  # Use 'number' for both floats and integers
                "description": "The radius of the circle, must be a positive number.",
            }
        },
        # 'required' lists the arguments the model MUST provide.
        "required": ["radius"],
    },
}

# --- 3. Configuration and Initial Request ---

# Initialize the Gemini client. Assumes GEMINI_API_KEY is set in environment.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client. Check API key: {e}")
    exit()

# 3a. Bundle the function schema into a Tool object.
# A single Tool can contain multiple function declarations.
circle_tool = types.Tool(function_declarations=[CALCULATOR_SCHEMA])

# 3b. Configure the generation request to include the tools.
config = types.GenerateContentConfig(tools=[circle_tool])

# Define the user's prompt that requires the tool.
USER_PROMPT = "What is the area of a circle with a radius of 15.5 units?"

# Start the conversation history list, beginning with the user's prompt.
conversation_history = [
    types.Content(role="user", parts=[types.Part.from_text(USER_PROMPT)])
]

print(f"--- 1st Turn: Sending Prompt to Gemini ---")
print(f"User: {USER_PROMPT}\n")

# Send the request with the tools defined
response_1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation_history,
    config=config,
)

# --- 4. Handle the Model's Response (Function Call Check) ---

# Check if the model decided to call a function.
# This check is Pythonic (EAFP - Easier to Ask for Forgiveness than Permission).
try:
    # Access the function call object deep within the response structure
    tool_call = response_1.candidates[0].content.parts[0].function_call
    
    # Check if a function call object exists
    if tool_call:
        print(f"--- 2nd Turn: Function Call Suggested by AI ---")
        print(f"AI suggests calling: {tool_call.name}")
        print(f"Arguments provided: {tool_call.args}")

        # Execute the corresponding Python function using the extracted arguments.
        # The **tool_call.args unpacks the dictionary into keyword arguments.
        if tool_call.name == "calculate_circle_area":
            function_result = calculate_circle_area(**tool_call.args)
            print(f"Function executed successfully. Result: {function_result}")

            # --- 5. Send the Function Result Back to the Model (Completion) ---
            
            # 5a. Create a Part containing the function execution result.
            function_response_part = types.Part.from_function_response(
                name=tool_call.name,
                response=function_result, # Send the dictionary result
            )

            # 5b. Update the conversation history for the final turn.
            # Append the model's function call response (Content)
            conversation_history.append(response_1.candidates[0].content)
            # Append the application's function result (Content, role="user")
            conversation_history.append(
                types.Content(role="user", parts=[function_response_part])
            )
            
            print(f"\n--- 3rd Turn: Sending Result Back to Gemini for Final Answer ---")

            # 5c. Call the model again with the updated history.
            final_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation_history,
                config=config,
            )

            print(f"Gemini's Final User-Friendly Response:\n{final_response.text}")

        else:
            print(f"Error: Function name '{tool_call.name}' is unknown.")
            
    else:
        # If no function call was suggested, the model must have generated text.
        print(f"--- 2nd Turn: Direct Text Response from AI ---")
        print(f"Model Text: {response_1.text}")

except AttributeError:
    # Handles cases where 'function_call' attribute is missing or structure is different
    # This is a robust way to handle the response object.
    print(f"Response structure error or no function call found.")
    print(f"Raw Response Text: {response_1.text}")
    

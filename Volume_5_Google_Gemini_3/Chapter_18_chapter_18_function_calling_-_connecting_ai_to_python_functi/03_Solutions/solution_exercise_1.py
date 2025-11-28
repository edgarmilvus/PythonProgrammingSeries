
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
from google.genai import types
from typing import List, Dict, Any

# --- Configuration and Initialization ---
# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Ensure API key is set. Details: {e}")
    # Exit silently if running in an automated environment without the key, 
    # but print a warning if this were a production application.
    # For this exercise, we assume the environment is correctly configured.
    pass

MODEL_NAME = "gemini-2.5-flash"


# =================================================================
# EXERCISE 1: THE UNIVERSAL CURRENCY CONVERTER (Single-Turn Extraction)
# =================================================================

# 1. Define the Python Function (Mock)
def convert_currency(amount: float, source_currency: str, target_currency: str) -> dict:
    """Mocks a currency conversion API call."""
    # Mock result for the sake of the exercise
    if source_currency.upper() == "USD" and target_currency.upper() == "EUR":
        converted_amount = amount * 0.93  # Mock rate
        return {"result": round(converted_amount, 2), "unit": target_currency.upper()}
    return {"result": amount, "unit": source_currency.upper()}

# 2. Define the Schema
currency_converter_schema = {
    "name": "convert_currency",
    "description": "Converts a specified amount from a source currency to a target currency.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "The numerical amount of money to convert (e.g., 1250.75).",
            },
            "source_currency": {
                "type": "string",
                "description": "The currency code of the source money (e.g., 'USD', 'GBP').",
            },
            "target_currency": {
                "type": "string",
                "description": "The currency code of the desired output currency (e.g., 'EUR', 'JPY').",
            },
        },
        "required": ["amount", "source_currency", "target_currency"],
    },
}

def exercise_1():
    print("\n" + "="*50)
    print("EXERCISE 1: CURRENCY CONVERTER (Single-Turn Extraction)")
    print("="*50)
    
    tools = types.Tool(function_declarations=[currency_converter_schema])
    config = types.GenerateContentConfig(tools=[tools])
    
    prompt = "If I have $1,250.75 in my account, how many Euros would that be?"
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    
    # 4. Check for a function call
    try:
        # Access the function call object from the response structure
        function_call = response.candidates[0].content.parts[0].function_call
        
        if function_call:
            print(f"Prompt: {prompt}")
            print(f"✅ Function Call Detected!")
            print(f"Function Name: {function_call.name}")
            # The args attribute is a dictionary-like object
            print(f"Arguments: {dict(function_call.args)}")
            
        else:
            print("❌ No function call found in the response.")
            print(f"Model Text Response: {response.text}")
            
    except (IndexError, AttributeError) as e:
        print(f"❌ Error processing response structure: {e}")


# =================================================================
# EXERCISE 2: THE CONVERSATIONAL CALCULATOR (Full Two-Turn Loop)
# =================================================================

# 1. Define the Python Function
def execute_math_operation(operation: str, num1: float, num2: float) -> float:
    """Performs a specified arithmetic operation."""
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            # Return a large number or handle error gracefully
            return float('inf') 
        return num1 / num2
    else:
        raise ValueError(f"Unknown operation: {operation}")

# 2. Define the Schema
calculator_schema = {
    "name": "execute_math_operation",
    "description": "Performs basic arithmetic operations (add, subtract, multiply, divide) on two numbers.",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "The mathematical operation to perform.",
                "enum": ["add", "subtract", "multiply", "divide"],
            },
            "num1": {"type": "number", "description": "The first number."},
            "num2": {"type": "number", "description": "The second number."},
        },
        "required": ["operation", "num1", "num2"],
    },
}

def exercise_2():
    print("\n" + "="*50)
    print("EXERCISE 2: CONVERSATIONAL CALCULATOR (Full Two-Turn)")
    print("="*50)

    tools = types.Tool(function_declarations=[calculator_schema])
    config = types.GenerateContentConfig(tools=[tools])
    
    # Prompt requires two steps: multiplication then addition
    user_prompt = "What is the result of multiplying 45 by 12, and then adding 30?"
    
    # --- TURN 1: Send prompt and get function call ---
    contents = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    print(f"1. User Prompt: {user_prompt}")
    response_1 = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )
    
    try:
        # Extract function call details
        tool_call = response_1.candidates[0].content.parts[0].function_call
        if not tool_call:
            print("❌ Model did not suggest a function call in Turn 1.")
            return

        print(f"2. Model Suggests: {tool_call.name}({dict(tool_call.args)})")
        
        # --- EXECUTION: Execute the function ---
        function_result = execute_math_operation(**tool_call.args)
        print(f"3. Function executed. Result: {function_result}")
        
        # --- TURN 2: Send result back to the model for final response ---
        
        # 1. Append the model's function call content (mandatory for context)
        contents.append(response_1.candidates[0].content)
        
        # 2. Create the function response part
        function_response_part = types.Part.from_function_response(
            name=tool_call.name,
            # The response dictionary must contain the result
            response={"result": function_result},
        )
        
        # 3. Append the function response as a 'user' turn
        contents.append(types.Content(role="user", parts=[function_response_part]))
        
        # 4. (Optional but helpful) Append a final instruction to complete the multi-step reasoning
        contents.append(types.Content(role="user", parts=[types.Part(text=f"Now, please use that result and complete the original request by adding 30 to it, giving the final answer.")]))


        print("4. Sending function result and follow-up back to model...")
        final_response = client.models.generate_content(
            model=MODEL_NAME,
            config=config,
            contents=contents,
        )
        
        print("\n5. Final Model Response:")
        print(f"✅ {final_response.text}")
            
    except Exception as e:
        print(f"An error occurred during the two-turn process: {e}")


# =================================================================
# EXERCISE 3: VIRTUAL FILE SYSTEM NAVIGATOR (Advanced Types and Validation)
# =================================================================

# 1. Define the Python Function
def file_system_action(action: str, filenames: List[str] = None) -> Dict[str, Any]:
    """Mocks file system operations with input validation."""
    
    if action == "list_current_dir":
        # Ignore filenames for this action
        current_dir = os.getcwd()
        # Mocking a list of files
        mock_files = ["app.py", "config.json", "data_log.txt", "README.md"]
        return {"status": "success", "action": action, "current_directory": current_dir, "files": mock_files}

    if action in ["create_file", "delete_file"]:
        # 3. Validation Logic: Ensure filenames list is not empty
        if not filenames or len(filenames) == 0:
            return {"status": "error", "message": f"Error: Filenames list cannot be empty for action: {action}"}
        
        return {
            "status": "success",
            "action": action,
            "files_affected": len(filenames),
            "files_list": filenames
        }
    
    return {"status": "error", "message": f"Invalid action specified: {action}"}

# 2. Define the Schema (using array type)
file_manager_schema = {
    "name": "file_system_action",
    "description": "Performs file system operations like listing, creating, or deleting files.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "The file operation to perform.",
                "enum": ["list_current_dir", "create_file", "delete_file"],
            },
            "filenames": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of file names relevant to the action.",
            },
        },
        # Note: 'filenames' is not required globally, as list_current_dir doesn't need it.
        "required": ["action"], 
    },
}

def exercise_3():
    print("\n" + "="*50)
    print("EXERCISE 3: VIRTUAL FILE SYSTEM (Arrays & Validation)")
    print("="*50)
    
    tools = types.Tool(function_declarations=[file_manager_schema])
    config = types.GenerateContentConfig(tools=[tools])
    
    # Scenario 1: Listing files (should trigger list_current_dir, filenames ignored)
    prompt_1 = "List the files in the current folder."
    response_1 = client.models.generate_content(model=MODEL_NAME, contents=prompt_1, config=config)
    
    print(f"Scenario 1 Prompt: {prompt_1}")
    tool_call_1 = response_1.candidates[0].content.parts[0].function_call
    if tool_call_1:
        result_1 = file_system_action(**dict(tool_call_1.args))
        print(f"  Call: {tool_call_1.name}({dict(tool_call_1.args)})")
        print(f"  Result: {json.dumps(result_1, indent=2)}")
    else:
        print("  ❌ No function call detected.")
    
    print("-" * 20)

    # Scenario 2: Deleting files (should trigger delete_file with an array)
    prompt_2 = "I need to delete report_q1.pdf and temp_log.txt."
    response_2 = client.models.generate_content(model=MODEL_NAME, contents=prompt_2, config=config)
    
    print(f"Scenario 2 Prompt: {prompt_2}")
    tool_call_2 = response_2.candidates[0].content.parts[0].function_call
    if tool_call_2:
        result_2 = file_system_action(**dict(tool_call_2.args))
        print(f"  Call: {tool_call_2.name}({dict(tool_call_2.args)})")
        print(f"  Result: {json.dumps(result_2, indent=2)}")
    else:
        print("  ❌ No function call detected.")


# =================================================================
# EXERCISE 4: THE HOME AUTOMATION CHALLENGE (Parallel Function Calling)
# =================================================================

# --- 3. Define the Python Functions (Mock) ---
def power_disco_ball(power: bool) -> dict:
    return {"status": "success", "device": "disco_ball", "state": "on" if power else "off"}

def start_music(energetic: bool, loud: bool) -> dict:
    return {"status": "success", "device": "music_system", "energetic": energetic, "loud": loud}

def dim_lights(brightness: float) -> dict:
    return {"status": "success", "device": "main_lights", "brightness": brightness}

# 2. Define New Function
def set_hvac_temperature(temperature: int, unit: str) -> dict:
    """Sets the room temperature."""
    return {"status": "success", "device": "HVAC", "temperature": temperature, "unit": unit}

# --- 1. Reuse/Define Schemas ---
power_disco_ball_schema = {
    "name": "power_disco_ball",
    "description": "Powers the spinning disco ball.",
    "parameters": {"type": "object", "properties": {"power": {"type": "boolean", "description": "Whether to turn the disco ball on or off."}}, "required": ["power"]},
}
start_music_schema = {
    "name": "start_music",
    "description": "Play some music matching the specified parameters.",
    "parameters": {"type": "object", "properties": {"energetic": {"type": "boolean", "description": "Whether the music is energetic or not."}, "loud": {"type": "boolean", "description": "Whether the music is loud or not."}}, "required": ["energetic", "loud"]},
}
dim_lights_schema = {
    "name": "dim_lights",
    "description": "Dim the lights.",
    "parameters": {"type": "object", "properties": {"brightness": {"type": "number", "description": "The brightness of the lights, 0.0 is off, 1.0 is full."}}, "required": ["brightness"]},
}
set_hvac_temperature_schema = {
    "name": "set_hvac_temperature",
    "description": "Sets the heating, ventilation, and air conditioning temperature.",
    "parameters": {
        "type": "object",
        "properties": {
            "temperature": {"type": "integer", "description": "The desired temperature setting."},
            "unit": {"type": "string", "description": "The temperature unit.", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["temperature", "unit"],
    },
}

# Map function names to actual executable functions
FUNCTION_MAP = {
    "power_disco_ball": power_disco_ball,
    "start_music": start_music,
    "dim_lights": dim_lights,
    "set_hvac_temperature": set_hvac_temperature,
}

def exercise_4():
    print("\n" + "="*50)
    print("EXERCISE 4: HOME AUTOMATION (Parallel Function Calling)")
    print("="*50)

    all_schemas = [
        power_disco_ball_schema, 
        start_music_schema, 
        dim_lights_schema, 
        set_hvac_temperature_schema
    ]
    
    # Configure the model to use all tools
    house_tools = [types.Tool(function_declarations=all_schemas)]
    
    # Use tool_config to ensure the model knows it can call ANY function
    config = types.GenerateContentConfig(
        tools=house_tools,
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    )
    
    # Prompt requires setting temperature AND starting a party (multiple actions)
    prompt = "It's too cold in here, set the temperature to 72 Fahrenheit. Also, turn this place into a party now!"
    print(f"Prompt: {prompt}\n")
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    
    # Note: For parallel calls, access the list of calls directly via response.function_calls
    function_calls = response.function_calls
    
    if not function_calls:
        print("❌ No function calls were detected.")
        return

    print(f"✅ Detected {len(function_calls)} parallel function calls:")
    
    results = []
    
    # 4. Execution: Iterate through all function calls
    for i, fn_call in enumerate(function_calls):
        fn_name = fn_call.name
        # Convert args to a standard Python dictionary
        fn_args = dict(fn_call.args) 
        
        print(f"\n--- Call {i+1} ({fn_name}) ---")
        print(f"Args: {fn_args}")
        
        if fn_name in FUNCTION_MAP:
            # Execute the corresponding Python function
            result = FUNCTION_MAP[fn_name](**fn_args)
            print(f"Execution Result: {result}")
            results.append((fn_call, result))
        else:
            print(f"Warning: Unknown function name {fn_name}")
            
    # Optional: Send all results back to the model for a final summary
    if results:
        print("\n--- Sending results back for final summary ---")
        
        # 1. Start history with the user prompt
        contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        # 2. Append the model's multi-part function call content
        contents.append(response.candidates[0].content)
        
        # 3. Append all function responses in a single user turn
        function_response_parts = []
        for fn_call, result in results:
            function_response_parts.append(
                types.Part.from_function_response(
                    name=fn_call.name,
                    response={"result": result}
                )
            )
        
        contents.append(types.Content(role="user", parts=function_response_parts))
        
        final_response = client.models.generate_content(
            model=MODEL_NAME,
            config=config,
            contents=contents,
        )
        print("\n--- Final Model Summary ---")
        print(final_response.text)


# --- Execute all exercises ---
if __name__ == "__main__":
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()

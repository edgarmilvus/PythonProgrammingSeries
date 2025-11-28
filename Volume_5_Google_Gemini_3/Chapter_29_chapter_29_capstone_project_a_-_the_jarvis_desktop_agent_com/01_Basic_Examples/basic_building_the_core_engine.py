
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

# Source File: basic_building_the_core_engine.py
# Description: Building the Core Engine
# ==========================================

import time
import os
from typing import Any, List, Tuple

# Playwright is used to control the browser and capture screenshots
from playwright.sync_api import sync_playwright

# Google GenAI imports for model interaction and tool definitions
from google import genai
from google.genai import types
from google.genai.types import Content, Part

# --- 1. CONFIGURATION AND SETUP ---

# Initialize the Gemini Client
# Assumes GEMINI_API_KEY is set in environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Ensure the GEMINI_API_KEY environment variable is set.")
    exit()

# Constants for screen dimensions (recommended by documentation)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
MODEL_NAME = 'gemini-2.5-computer-use-preview-10-2025'
TURN_LIMIT = 8 # Limit the number of steps to prevent infinite loops

# --- 2. COORDINATE TRANSLATION HELPERS ---

def denormalize_x(x: int, screen_width: int) -> int:
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    # The model works on a 1000x1000 grid internally
    return int(x / 1000 * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    return int(y / 1000 * screen_height)

# --- 3. ACTION EXECUTION ENGINE (Client-Side Tool Handler) ---

def execute_function_calls(candidate, page, screen_width, screen_height):
    """
    Parses the model's FunctionCalls and executes the corresponding Playwright actions.
    """
    results = []
    function_calls = []
    # Extract all function calls from the candidate response
    for part in candidate.content.parts:
        if part.function_call:
            function_calls.append(part.function_call)

    if not function_calls:
        return results

    print(f"  -> Model proposed {len(function_calls)} action(s).")

    for function_call in function_calls:
        action_result = {}
        fname = function_call.name
        args = function_call.args
        print(f"  -> Executing: {fname}")

        try:
            if fname == "open_web_browser":
                # This action is often redundant if the browser is already open
                pass 
            
            elif fname == "navigate":
                # Navigate to a specific URL
                url = args["url"]
                page.goto(url)

            elif fname == "click_at":
                # Calculate actual pixel coordinates
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y)
                
            elif fname == "type_text_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", True) # Defaulting to True per docs example

                # 1. Click to focus the input field
                page.mouse.click(actual_x, actual_y)
                
                # 2. Clear the field (Simulating Ctrl/Meta+A then Backspace)
                # Note: 'Meta' is Command on Mac, Control/Windows key on others.
                # Playwright handles cross-platform key mapping reasonably well.
                page.keyboard.press("Control+A") 
                page.keyboard.press("Backspace")
                
                # 3. Type the text
                page.keyboard.type(text)
                
                # 4. Press Enter if requested
                if press_enter:
                    page.keyboard.press("Enter")
                    
            elif fname == "scroll_document":
                direction = args["direction"]
                # Playwright's mouse wheel action simulates scrolling
                if direction == "down":
                    page.mouse.wheel(0, 500) # Scroll 500 pixels down
                elif direction == "up":
                    page.mouse.wheel(0, -500) # Scroll 500 pixels up
                else:
                    print(f"Warning: Scroll direction '{direction}' not fully implemented.")

            else:
                print(f"Warning: Unimplemented or custom function {fname}. Skipping.")
                
            # Wait for potential navigations or dynamic rendering to stabilize
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(1.5) # A slight pause helps stabilize the visual state

        except Exception as e:
            print(f"Error executing {fname}: {e}")
            action_result = {"error": str(e)}

        # Store the result of the action execution
        results.append((fname, action_result))

    return results

# --- 4. STATE CAPTURE AND RESPONSE FORMATTING ---

def get_function_responses(page, results):
    """
    Captures the new screenshot and URL, and packages them into FunctionResponse objects.
    """
    # Capture the state *after* the action(s) have been executed
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    function_responses = []
    
    # Create one FunctionResponse for each executed action
    for name, result in results:
        # Include the current URL and any error messages in the response payload
        response_data = {"url": current_url}
        response_data.update(result)
        
        # Construct the FunctionResponse, including the screenshot as inline data
        function_responses.append(
            types.FunctionResponse(
                name=name,
                response=response_data,
                parts=[
                    types.FunctionResponsePart(
                        inline_data=types.FunctionResponseBlob(
                            mime_type="image/png",
                            data=screenshot_bytes
                        )
                    )
                ]
            )
        )
    return function_responses

# --- 5. MAIN AGENT LOOP EXECUTION ---

def run_jarvis_agent(user_goal: str, initial_url: str):
    """Initializes the browser and runs the core Computer Use agent loop."""
    
    print("\n[AGENT INITIALIZATION]")
    print(f"Goal: {user_goal}")
    
    # 1. Setup Playwright environment (within the function for clean exit)
    playwright = sync_playwright().start()
    # headless=False allows us to watch the agent work
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
    )
    page = context.new_page()

    try:
        # Navigate to the starting page
        page.goto(initial_url)
        print(f"Starting at: {initial_url}")

        # 2. Configure the Model Request
        config = types.GenerateContentConfig(
            # Enable the Computer Use tool for browser environment
            tools=[types.Tool(computer_use=types.ComputerUse(
                environment=types.Environment.ENVIRONMENT_BROWSER
            ))],
            # Request the model's internal reasoning for transparency
            thinking_config=types.ThinkingConfig(include_thoughts=True),
        )

        # 3. Initialize Conversation History (Contents)
        initial_screenshot = page.screenshot(type="png")
        
        contents = [
            Content(role="user", parts=[
                Part(text=user_goal),
                # The first turn includes the user prompt AND the initial screen state
                Part.from_bytes(data=initial_screenshot, mime_type='image/png')
            ])
        ]

        # 4. The Agent Loop
        for i in range(TURN_LIMIT):
            print(f"\n--- Turn {i+1}/{TURN_LIMIT} ---")
            print("1. Agent Thinking...")
            
            # Send the entire history (text + images + function responses)
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=config,
            )

            candidate = response.candidates[0]
            
            # Append the model's response (which may contain text or function calls)
            contents.append(candidate.content)

            # Check if the model decided to output a final answer or requires action
            has_function_calls = any(part.function_call for part in candidate.content.parts)
            
            if not has_function_calls:
                # Task complete: Extract and print the final text response
                text_response = " ".join([part.text for part in candidate.content.parts if part.text])
                print("\n[TASK COMPLETE]")
                print("Agent Final Output:", text_response)
                break
            
            # If actions are required, execute them
            print("2. Executing actions...")
            results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

            # 3. Capture new state and format feedback
            print("3. Capturing new state and sending feedback...")
            function_responses = get_function_responses(page, results)

            # 4. Append function responses to history for the next turn
            contents.append(
                Content(role="user", parts=[Part(function_response=fr) for fr in function_responses])
            )
        
        if i == TURN_LIMIT - 1 and has_function_calls:
            print("\n[WARNING] Turn limit reached before task completion.")

    finally:
        # Ensure resources are released
        print("\n[CLEANUP] Closing browser...")
        browser.close()
        playwright.stop()

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Define the task to solve
    USER_GOAL = "Navigate to the pricing page on this site, find the current price for the Gemini 2.5 Pro model in USD, and output the price only."
    INITIAL_URL = "https://ai.google.dev/gemini-api/docs"
    
    run_jarvis_agent(USER_GOAL, INITIAL_URL)

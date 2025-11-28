
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

import time
import os
from typing import Any, List, Tuple
from playwright.sync_api import sync_playwright

from google import genai
from google.genai import types
from google.genai.types import Content, Part

# --- 1. CONFIGURATION AND INITIALIZATION ---

# Constants based on documentation recommendation (1440x900)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
MODEL_NAME = 'gemini-2.5-computer-use-preview-10-2025'

# Initialize the Gemini Client (Assumes GEMINI_API_KEY is set in environment)
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client. Ensure GEMINI_API_KEY is set: {e}")
    exit()

# --- 2. COORDINATE TRANSLATION HELPERS ---

def denormalize_x(x: int, screen_width: int) -> int:
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    # The model works on a 1000x1000 grid, regardless of actual screen size.
    return int(x / 1000 * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    return int(y / 1000 * screen_height)

# --- 3. ACTION EXECUTION HANDLER ---

def execute_function_calls(candidate, page, screen_width, screen_height):
    """
    Parses function calls from the model response and executes them using Playwright.
    """
    results = []
    function_calls = []
    # Extract all function calls from the candidate response parts
    for part in candidate.content.parts:
        if part.function_call:
            function_calls.append(part.function_call)

    for function_call in function_calls:
        action_result = {}
        fname = function_call.name
        args = function_call.args
        print(f"  -> Executing action: {fname}")

        try:
            if fname == "open_web_browser":
                # Browser is already open, skip action but acknowledge
                pass 
            elif fname == "click_at":
                # Denormalize coordinates before clicking
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y)
            elif fname == "type_text_at":
                # Denormalize coordinates for the click/focus before typing
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", False)

                page.mouse.click(actual_x, actual_y)
                # Simple clear logic (Mandatory for reliable typing)
                page.keyboard.press("Control+A") # Select all
                page.keyboard.press("Backspace") # Delete selected
                page.keyboard.type(text)
                if press_enter:
                    page.keyboard.press("Enter")
            elif fname == "navigate":
                # Directly navigate to a URL
                page.goto(args["url"])
            else:
                # Handle unimplemented or custom functions
                print(f"Warning: Unimplemented UI action: {fname}. Skipping.")
                action_result = {"status": "skipped_unimplemented_function"}

            # Wait for the page to settle after the action
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(1) # Give the browser a moment to render

        except Exception as e:
            print(f"Error executing {fname}: {e}")
            action_result = {"error": str(e)}

        # Store the outcome of the execution
        results.append((fname, action_result))

    return results

# --- 4. STATE CAPTURE AND FEEDBACK GENERATION ---

def get_function_responses(page, results):
    """
    Captures the new state (screenshot and URL) and formats it as FunctionResponse
    for the model's next turn.
    """
    # Capture the new visual state
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    function_responses = []

    # Create a response object for every executed function call
    for name, result in results:
        response_data = {"url": current_url}
        response_data.update(result)
        
        # Construct the FunctionResponse, including the visual context (screenshot)
        function_responses.append(
            types.FunctionResponse(
                name=name,
                response=response_data,
                parts=[types.FunctionResponsePart(
                        inline_data=types.FunctionResponseBlob(
                            mime_type="image/png",
                            data=screenshot_bytes))
                ]
            )
        )
    return function_responses

# --- 5. MAIN AGENT LOOP EXECUTION ---

print("Starting Computer Use Agent...")

# 5a. Playwright Setup
playwright = sync_playwright().start()
# headless=False allows you to watch the automation in real-time
browser = playwright.chromium.launch(headless=False) 
context = browser.new_context(
    viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
)
page = context.new_page()

try:
    # 5b. Initial Navigation
    INITIAL_URL = "https://ai.google.dev/gemini-api/docs"
    page.goto(INITIAL_URL)
    page.wait_for_load_state("networkidle")
    print(f"Browser initialized, navigated to: {INITIAL_URL}")

    # 5c. Model Configuration
    config = types.GenerateContentConfig(
        tools=[types.Tool(computer_use=types.ComputerUse(
            environment=types.Environment.ENVIRONMENT_BROWSER
        ))],
        # Requesting thoughts helps in debugging and understanding the AI's plan
        thinking_config=types.ThinkingConfig(include_thoughts=True),
    )

    # 5d. Initial State Capture and Prompt
    initial_screenshot = page.screenshot(type="png")
    USER_PROMPT = "Find and click the 'Get Started' link on this page."
    print(f"\nGoal: {USER_PROMPT}")

    # Initialize conversation history with the user's prompt and the initial screenshot
    contents = [
        Content(role="user", parts=[
            Part(text=USER_PROMPT),
            Part.from_bytes(data=initial_screenshot, mime_type='image/png')
        ])
    ]

    # 5e. The Agent Loop (Limited to 3 turns for this basic example)
    turn_limit = 3
    for i in range(turn_limit):
        print(f"\n--- Agent Turn {i+1} ---")
        
        # 1. Send Request to the Model
        print("Agent is thinking...")
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0]
        
        # Append the model's response (which includes text and function calls) to history
        contents.append(candidate.content)

        # Check if the model suggested any actions
        has_function_calls = any(part.function_call for part in candidate.content.parts)
        
        # Print the model's text response/thoughts
        text_response = " ".join([part.text for part in candidate.content.parts if part.text])
        print(f"Model Response: {text_response}")

        if not has_function_calls:
            print("\nTask completed or agent stopped generating actions.")
            break

        # 2. & 3. Execute Received Actions
        print("Executing actions...")
        results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

        # 4. Capture New Environment State and Generate Feedback
        print("Capturing new state and generating feedback...")
        function_responses = get_function_responses(page, results)

        # Append the function responses (including the new screenshot) to history
        # This closes the loop and sets up the context for the next turn
        contents.append(
            Content(role="user", parts=[Part(function_response=fr) for fr in function_responses])
        )

    print("\n--- Agent Loop Finished ---")

finally:
    # 5f. Cleanup
    print("Closing browser...")
    browser.close()
    playwright.stop()

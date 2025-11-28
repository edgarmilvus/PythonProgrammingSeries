
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

import time
from typing import Any, List, Tuple, Dict
from playwright.sync_api import sync_playwright

from google import genai
from google.genai import types
from google.genai.types import Content, Part

# --- 1. CONFIGURATION AND INITIALIZATION ---

# Constants for screen dimensions (recommended by Google for best results)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

# Initialize the Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client. Ensure GOOGLE_API_KEY is set. Error: {e}")
    exit()

# Setup Playwright
print("Initializing browser and sandboxed environment...")
playwright = sync_playwright().start()
# Launch Chromium in non-headless mode so we can watch the actions
browser = playwright.chromium.launch(headless=False)
context = browser.new_context(
    viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
)
page = context.new_page()

# --- 2. HELPER FUNCTIONS: COORDINATE SCALING ---

def denormalize_x(x: int, screen_width: int) -> int:
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    # The model predicts coordinates scaled to a 1000x1000 grid.
    return int(x / 1000 * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    return int(y / 1000 * screen_height)

# --- 3. HELPER FUNCTION: ACTION EXECUTION ---

def execute_function_calls(candidate: types.Candidate, page: Any, screen_width: int, screen_height: int) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Parses the model's function calls and executes them using Playwright.
    Returns a list of (function_name, result_payload) tuples.
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
                # Browser is already open, no action needed for this case
                pass 
            elif fname == "navigate":
                # Navigate to a specific URL
                page.goto(args["url"], timeout=30000)
            elif fname == "click_at":
                # Convert normalized coordinates (0-1000) to actual pixels
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y)
            elif fname == "type_text_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", True) # Default is True
                clear_before_typing = args.get("clear_before_typing", True) # Default is True

                # 1. Click to focus the element
                page.mouse.click(actual_x, actual_y)
                
                # 2. Clear the field if requested (using Mac/Windows agnostic shortcuts)
                if clear_before_typing:
                    page.keyboard.press("Control+A") # Select all
                    page.keyboard.press("Backspace") # Delete selection
                
                # 3. Type the text
                page.keyboard.type(text)
                
                # 4. Press Enter if requested
                if press_enter:
                    page.keyboard.press("Enter")
            elif fname == "scroll_document":
                # Scroll the entire page up/down/left/right
                direction = args["direction"].lower()
                if direction == "down":
                    # Simulate page down key press for a smooth scroll
                    page.keyboard.press("PageDown")
                elif direction == "up":
                    page.keyboard.press("PageUp")
                else:
                    # For simplicity, we only implement vertical scrolling here
                    print(f"Warning: Scroll direction '{direction}' not fully implemented.")
            elif fname == "wait_5_seconds":
                print("  -> Waiting 5 seconds for content to load...")
                time.sleep(5)
            else:
                # Catch any unimplemented functions
                print(f"Warning: Unimplemented UI action: {fname}")
                action_result = {"status": f"unimplemented_action_{fname}"}

            # Crucial: Wait for the page to settle after an action
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(1) # Small buffer for visual rendering

        except Exception as e:
            print(f"Error executing {fname}: {e}")
            action_result = {"error": str(e)}

        results.append((fname, action_result))

    return results

# --- 4. HELPER FUNCTION: STATE CAPTURE ---

def get_function_responses(page: Any, results: List[Tuple[str, Dict[str, Any]]]) -> List[types.Content]:
    """
    Captures the new environment state (screenshot and URL) and formats 
    it into FunctionResponse objects for the model.
    """
    # Capture the state *after* all actions in this turn have completed
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    function_responses = []

    # Create a response for each function call that was executed
    for name, result in results:
        response_data = {"url": current_url}
        response_data.update(result) # Add any execution errors/status

        function_responses.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
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
                ]
            )
        )
    return function_responses

# --- 5. THE MAIN AGENT LOOP ---

try:
    # Set initial navigation point
    page.goto("https://www.google.com")

    # Configure the model to use the Computer Use tool
    config = types.GenerateContentConfig(
        tools=[types.Tool(computer_use=types.ComputerUse(
            environment=types.Environment.ENVIRONMENT_BROWSER
        ))],
        # Request thoughts for better debugging and transparency
        thinking_config=types.ThinkingConfig(include_thoughts=True),
    )

    # Define the high-level goal
    USER_PROMPT = "Search for 'best ergonomic keyboard 2024'. Click the first search result that is NOT an advertisement or a shopping result. Once on the target page, scroll down to ensure the full content is loaded, then stop."
    print(f"\n[GOAL] Competitive Research Task: {USER_PROMPT}")

    # Initialize conversation history with the goal and the initial screenshot
    initial_screenshot = page.screenshot(type="png")
    contents = [
        Content(role="user", parts=[
            Part(text=USER_PROMPT),
            Part.from_bytes(data=initial_screenshot, mime_type='image/png')
        ])
    ]

    # Start the Agent Loop
    turn_limit = 8 # Limit the number of turns to prevent infinite loops
    for i in range(turn_limit):
        print(f"\n--- Turn {i+1}/{turn_limit} ---")
        
        # 1. Send the current state and history to the model
        print("Agent Thinking...")
        response = client.models.generate_content(
            model='gemini-2.5-computer-use-preview-10-2025',
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0]
        
        # 2. Append the model's response (including thoughts and function calls) to history
        contents.append(candidate.content)

        # Check if the task is complete (model responds with text, not actions)
        has_function_calls = any(part.function_call for part in candidate.content.parts)
        if not has_function_calls:
            text_response = " ".join([part.text for part in candidate.content.parts if part.text])
            print("\n[TASK COMPLETE] Agent Final Response:", text_response)
            break
        
        # 3. Execute the function calls
        print("Executing actions...")
        results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

        # 4. Capture the new environment state and format the function responses
        print("Capturing new state and preparing feedback...")
        function_responses = get_function_responses(page, results)

        # 5. Append the function responses (including the new screenshot) to history
        # This prepares the context for the next turn
        contents.extend(function_responses)

    else:
        print(f"\n[WARNING] Agent loop terminated after {turn_limit} turns without completion.")

finally:
    # Cleanup
    print("\nClosing browser and cleaning up resources...")
    browser.close()
    playwright.stop()

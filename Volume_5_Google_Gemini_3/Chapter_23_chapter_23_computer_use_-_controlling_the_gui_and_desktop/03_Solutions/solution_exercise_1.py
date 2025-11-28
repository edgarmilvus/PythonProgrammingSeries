
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

import time
import sys
from typing import Any, List, Tuple, Dict, Optional
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from google import genai
from google.genai import types
from google.genai.types import Content, Part

# --- Configuration and Setup ---

# Constants for screen dimensions (Recommended by Google for Computer Use)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

# Initialize the Gemini Client (Assumes API Key is set in environment variables)
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client. Ensure API key is set: {e}")
    # In a real application, you might exit here. For this solution, we proceed assuming client initialization is successful.
    pass


# --- Helper Functions (Coordinate Translation) ---

def denormalize_x(x: int, screen_width: int) -> int:
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    # The model uses a 1000x1000 grid for coordinates
    return int(x / 1000 * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    return int(y / 1000 * screen_height)


# --- Exercise 3: Custom Function Definition and Declaration ---

def log_transaction_data(key: str, value: str) -> Dict[str, str]:
    """
    Custom function to simulate logging important data to an external system.
    Called by the model when it identifies key information on the screen.
    """
    print(f"\n[CUSTOM LOGGING] Recording data: {key} = {value}")
    # In a real scenario, this would write to a database or call an external API.
    return {"status": "success", "log_entry": f"{key}: {value}", "timestamp": str(time.time())}

# Build function declarations for the custom tool
CUSTOM_FUNCTION_DECLARATIONS = [
    types.FunctionDeclaration.from_callable(client=client, callable=log_transaction_data),
]


# --- Action Execution Handler (Exercises 1, 2, and 4) ---

# Exercise 2: Define actions requiring user confirmation
# Added 'navigate' and 'key_combination' as risky actions, as required.
RISKY_ACTIONS = ["navigate", "key_combination", "drag_and_drop", "open_web_browser"]

def execute_function_calls(candidate, page, screen_width, screen_height):
    """
    Parses function calls from the model, executes them via Playwright,
    and handles safety checks and error reporting.
    """
    results = []
    function_calls = []
    # Extract all function calls from the model's response parts
    for part in candidate.content.parts:
        if part.function_call:
            function_calls.append(part.function_call)

    for function_call in function_calls:
        action_result = {}
        fname = function_call.name
        args = function_call.args
        print(f"\n  -> Proposed Action: {fname} with args: {args}")

        # --- Exercise 2: Safety Confirmation Check ---
        if fname in RISKY_ACTIONS:
            print(f"  !!! SECURITY ALERT: Action '{fname}' requires user confirmation.")
            # Prompt user for input in the console
            user_input = input("  Proceed with this action? (Y/N): ").upper()
            if user_input != 'Y':
                print(f"  Action {fname} denied by user.")
                # Return denial status to the model
                action_result = {"status": "action_denied", "reason": "User confirmation required and denied."}
                results.append((fname, action_result))
                continue # Skip execution and move to the next function call

        # --- Execution Logic (Exercises 1, 3, 4) ---
        try:
            if fname == "open_web_browser":
                # Typically a no-op if the browser is already initialized
                pass
            
            elif fname == "click_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y, timeout=5000)
            
            elif fname == "type_text_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", False)
                clear_before_typing = args.get("clear_before_typing", True) # Default behavior

                page.mouse.click(actual_x, actual_y, timeout=5000)
                
                if clear_before_typing:
                    # Simulate clearing the field (Ctrl+A / Cmd+A, then Backspace)
                    # Note: Playwright handles platform differences for Control/Meta keys well
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                
                page.keyboard.type(text)
                if press_enter:
                    page.keyboard.press("Enter")
            
            # --- Exercise 1: Implement go_back ---
            elif fname == "go_back":
                page.go_back(timeout=5000)
                print("  -> Executing: Browser navigated back.")

            # --- Exercise 1: Implement scroll_document ---
            elif fname == "scroll_document":
                direction = args["direction"].lower()
                # Use Playwright's mouse.wheel() for scrolling
                if direction == "down":
                    page.mouse.wheel(0, 500)
                elif direction == "up":
                    page.mouse.wheel(0, -500)
                elif direction == "right":
                    page.mouse.wheel(500, 0)
                elif direction == "left":
                    page.mouse.wheel(-500, 0)
                else:
                    raise ValueError(f"Invalid scroll direction: {direction}")
                print(f"  -> Executing: Document scrolled {direction}.")
            
            elif fname == "navigate":
                url = args["url"]
                # Increased timeout for navigation as recommended by documentation
                page.goto(url, timeout=15000) 
                print(f"  -> Executing: Navigating to {url}")
            
            # --- Exercise 3: Custom Function Call ---
            elif fname == "log_transaction_data":
                # Directly call the custom Python function
                action_result = log_transaction_data(args["key"], args["value"])
            
            # --- Handling other supported or unimplemented actions ---
            elif fname in ["hover_at", "key_combination", "scroll_at", "wait_5_seconds", "search", "go_forward", "drag_and_drop"]:
                 # For brevity, treat other required actions as unimplemented, but acknowledge them
                print(f"Warning: Function {fname} is supported but not fully implemented in this example.")
                action_result = {"status": "unimplemented_action", "details": f"Function {fname} skipped."}
            else:
                print(f"Warning: Unknown function {fname}. Skipping.")
                action_result = {"status": "unknown_function", "details": f"Function {fname} is not recognized."}


            # Wait for potential navigations/renders after a successful action
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(1) # Give the browser a moment to settle

        # --- Exercise 4: Robust Error Reporting ---
        except PlaywrightTimeoutError as e:
            # Catch specific Playwright timeout errors
            error_msg = f"Playwright Timeout Error during {fname}: {e}"
            print(f"!!! Error executing {fname}: {error_msg}")
            action_result = {"error": error_msg, "status": "execution_timeout"}
        except Exception as e:
            # Catch all other exceptions
            error_msg = f"General Execution Error during {fname}: {e}"
            print(f"!!! Error executing {fname}: {error_msg}")
            action_result = {"error": error_msg, "status": "general_execution_failure"}

        results.append((fname, action_result))

    return results


# --- State Capture and Response Generation ---

def get_function_responses(page, results):
    """
    Captures the current environment state (screenshot, URL) and packages
    it with the results of the executed functions to send back to the model.
    (Exercise 4: Ensures state capture happens even after execution errors)
    """
    try:
        # Capture the state *after* all actions in the turn have been attempted
        screenshot_bytes = page.screenshot(type="png")
        current_url = page.url
    except Exception as e:
        print(f"CRITICAL: Failed to capture screenshot or URL: {e}")
        # Use placeholder data if state capture fails
        screenshot_bytes = b''
        current_url = "ERROR_STATE"

    function_responses = []
    for name, result in results:
        # The response payload includes the URL and any specific result/error
        response_data = {"url": current_url}
        response_data.update(result)
        
        # Build the FunctionResponse object
        function_responses.append(
            types.FunctionResponse(
                name=name,
                response=response_data,
                parts=[
                    # Include the screenshot as a FunctionResponsePart
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


# --- Main Agent Loop Implementation ---

def run_agent_loop(initial_url: str, user_prompt: str, turn_limit: int = 8):
    """
    Initializes the browser and runs the multi-turn Computer Use agent loop.
    """
    print("--- Initializing Computer Use Agent ---")
    
    # Setup Playwright
    playwright = sync_playwright().start()
    try:
        # Launch browser non-headless so we can observe the automation
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT})
        page = context.new_page()
        page.goto(initial_url, timeout=15000)
    except Exception as e:
        print(f"FATAL: Playwright setup failed: {e}")
        playwright.stop()
        return

    try:
        # Configure the model (Including Exercise 3: Custom Functions)
        config = types.GenerateContentConfig(
            tools=[
                types.Tool(
                    computer_use=types.ComputerUse(
                        environment=types.Environment.ENVIRONMENT_BROWSER
                    )
                ),
                types.Tool(function_declarations=CUSTOM_FUNCTION_DECLARATIONS) # Custom tool
            ],
            thinking_config=types.ThinkingConfig(include_thoughts=True),
        )

        # Initialize history with the user prompt and initial screenshot
        initial_screenshot = page.screenshot(type="png")
        print(f"\n[GOAL]: {user_prompt}")
        print(f"[START URL]: {initial_url}")

        contents = [
            Content(role="user", parts=[
                Part(text=user_prompt),
                Part.from_bytes(data=initial_screenshot, mime_type='image/png')
            ])
        ]

        # Agent Loop
        for i in range(turn_limit):
            print(f"\n{'='*10} TURN {i+1}/{turn_limit} {'='*10}")
            print("Agent Thinking...")
            
            # 1. Send Request to Model
            response = client.models.generate_content(
                model='gemini-2.5-computer-use-preview-10-2025',
                contents=contents,
                config=config,
            )

            candidate = response.candidates[0]
            contents.append(candidate.content) # Add model response to history

            # Check for thinking/text response
            text_response = " ".join([part.text for part in candidate.content.parts if part.text])
            if text_response:
                print(f"[Agent Thought]: {text_response}")

            # 2. Check for Function Calls
            has_function_calls = any(part.function_call for part in candidate.content.parts)
            
            if not has_function_calls:
                print("\n[Agent Finished]: No more actions proposed or task completed.")
                break

            # 3. Execute Actions (Incorporates Exercises 1, 2, 4)
            results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

            # 4. Capture New State and Generate Function Responses
            print("Capturing new state and generating feedback...")
            function_responses = get_function_responses(page, results)

            # Append Function Responses (feedback) to history for the next turn
            contents.append(
                Content(role="user", parts=[Part(function_response=fr) for fr in function_responses])
            )
            
            # Safety break if we hit the turn limit
            if i == turn_limit - 1:
                print("\n[WARNING] Turn limit reached.")
                
    finally:
        # Cleanup
        print("\n--- Closing Browser and Cleanup ---")
        browser.close()
        playwright.stop()


# --- Execution Example ---

# Note: The initial URL should be a stable, public site for reliable testing.
INITIAL_TEST_URL = "https://ai.google.dev/gemini-api/docs"
TEST_PROMPT = (
    "First, search for 'pricing' on this page by typing into the search bar. "
    "Then, scroll down to ensure you see the bottom of the page. "
    "Finally, navigate back to the previous page using the browser history."
)

# To run the integrated solution, uncomment the line below.
# run_agent_loop(initial_url=INITIAL_TEST_URL, user_prompt=TEST_PROMPT)


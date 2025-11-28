
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

# Source File: project_full_system_integration_main_application.py
# Description: Full System Integration (Main Application)
# ==========================================

import time
import os
from typing import Any, List, Tuple, Dict
from playwright.sync_api import sync_playwright, Page, BrowserContext

from google import genai
from google.genai import types
from google.genai.types import Content, Part, FunctionCall, FunctionResponse

# --- A. CONFIGURATION AND INITIALIZATION ---

# Constants for screen dimensions (recommended by Google for Computer Use model)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
MODEL_NAME = 'gemini-2.5-computer-use-preview-10-2025'
TURN_LIMIT = 8 # Safety limit for the agent loop

# Initialize the Gemini Client
# Assumes GEMINI_API_KEY environment variable is set
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    print("Please ensure GEMINI_API_KEY is set in your environment.")
    exit()

# --- B. COORDINATE TRANSLATION HELPERS ---

def denormalize_x(x: int, screen_width: int) -> int:
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    # The model outputs coordinates scaled to a 1000x1000 grid.
    return int(x / 1000 * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    return int(y / 1000 * screen_height)

# --- C. ACTION EXECUTION HANDLER ---

def execute_function_calls(candidate: types.Candidate, page: Page, screen_width: int, screen_height: int) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Parses the model's function calls and executes the corresponding UI actions
    using Playwright.
    """
    results: List[Tuple[str, Dict[str, Any]]] = []
    function_calls: List[FunctionCall] = [
        part.function_call for part in candidate.content.parts if part.function_call
    ]

    if not function_calls:
        return results

    print(f"  -> Model proposed {len(function_calls)} actions.")

    for function_call in function_calls:
        action_result: Dict[str, Any] = {}
        fname = function_call.name
        args = function_call.args
        print(f"  -> Executing: {fname} with args: {args}")

        try:
            if fname == "open_web_browser":
                # Browser is already open, but we acknowledge the command
                pass 
            
            elif fname == "navigate":
                page.goto(args["url"])
            
            elif fname == "click_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y)
                
            elif fname == "type_text_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", True) # Defaulting to True
                clear_before_typing = args.get("clear_before_typing", True)

                # 1. Click to focus the area
                page.mouse.click(actual_x, actual_y)

                # 2. Clear the field if requested (Crucial for reliable typing)
                if clear_before_typing:
                    # Uses common desktop shortcut for Select All (Control+A) and Backspace
                    # Note: On Mac, this might need to be 'Meta+A'
                    page.keyboard.press("Control+A") 
                    page.keyboard.press("Backspace")
                
                # 3. Type the new text
                page.keyboard.type(text)
                
                # 4. Press Enter if requested
                if press_enter:
                    page.keyboard.press("Enter")

            elif fname == "scroll_document":
                direction = args["direction"].lower()
                # Playwright uses mouse wheel events for scrolling
                # Positive delta_y scrolls down, negative scrolls up.
                scroll_magnitude = 500 # Fixed scroll amount in pixels
                
                if direction == "down":
                    page.mouse.wheel(0, scroll_magnitude)
                elif direction == "up":
                    page.mouse.wheel(0, -scroll_magnitude)
                else:
                    print(f"Warning: Scroll direction '{direction}' not fully implemented.")
                    action_result = {"error": f"Unsupported scroll direction: {direction}"}

            elif fname == "wait_5_seconds":
                print("  -> Waiting 5 seconds...")
                time.sleep(5)
                
            elif fname == "go_back":
                page.go_back()
                
            elif fname == "search":
                page.goto("https://www.google.com") # Simple implementation of starting a new search
                
            else:
                print(f"Warning: Unimplemented or unsupported function {fname}. Skipping.")
                action_result = {"error": f"Function {fname} is not implemented in the client."}

            # Wait for browser load state after action execution
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(1.5) # Short pause to allow rendering stabilization

        except Exception as e:
            print(f"Critical Error executing {fname}: {e}")
            action_result = {"error": str(e)}

        results.append((fname, action_result))

    return results

# --- D. STATE CAPTURE HANDLER ---

def get_function_responses(page: Page, results: List[Tuple[str, Dict[str, Any]]]) -> List[Content]:
    """
    Captures the current state (screenshot and URL) and formats it into
    FunctionResponse objects for the model's next turn.
    """
    # Capture the new screen state
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    
    function_responses: List[Content] = []
    
    # Create one FunctionResponse for each executed action
    for name, result in results:
        # Include URL and any execution results (like errors)
        response_data = {"url": current_url}
        response_data.update(result)
        
        # Build the FunctionResponse object
        response_part = types.FunctionResponse(
            name=name,
            response=response_data,
            # Attach the screenshot as a blob to the function response
            parts=[types.FunctionResponsePart(
                    inline_data=types.FunctionResponseBlob(
                        mime_type="image/png",
                        data=screenshot_bytes))
            ]
        )
        
        # Wrap the response in a Content object for the conversation history
        function_responses.append(Content(role="user", parts=[Part(function_response=response_part)]))
        
    return function_responses

# --- E. MAIN AGENT EXECUTION LOOP ---

def run_jarvis_agent(user_prompt: str):
    """
    Initializes the browser and runs the core conversational agent loop.
    """
    print("--- Initializing Jarvis Desktop Agent ---")
    
    # 1. Setup Playwright
    playwright_instance = sync_playwright().start()
    # Launch in non-headless mode so the user can observe the actions
    browser = playwright_instance.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT})
    page = context.new_page()

    try:
        # 2. Navigate to the initial starting page
        page.goto("https://www.google.com")
        print(f"Browser navigated to: {page.url}")

        # 3. Configure the Gemini Model
        # We enable the Computer Use tool for browser automation
        config = types.GenerateContentConfig(
            tools=[types.Tool(computer_use=types.ComputerUse(
                environment=types.Environment.ENVIRONMENT_BROWSER
            ))],
            thinking_config=types.ThinkingConfig(include_thoughts=True), # Optional: helps debug agent reasoning
        )

        # 4. Prepare Initial History
        # Capture the initial screen state (Google homepage)
        initial_screenshot = page.screenshot(type="png")
        print(f"\nGoal received: {user_prompt}")

        # The first 'user' turn includes the text prompt and the initial screenshot
        contents: List[Content] = [
            Content(role="user", parts=[
                Part(text=user_prompt),
                Part.from_bytes(data=initial_screenshot, mime_type='image/png')
            ])
        ]

        # 5. Start the Agent Loop
        for i in range(TURN_LIMIT):
            print(f"\n--- Turn {i+1}/{TURN_LIMIT} ---")
            print("Jarvis is thinking...")
            
            # Send the current history and configuration to Gemini
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=config,
            )

            candidate = response.candidates[0]
            # Append the model's response (text and/or function calls) to history
            contents.append(candidate.content)
            
            # Check if the model suggested any actions
            has_function_calls = any(part.function_call for part in candidate.content.parts)
            
            # If the model provides a final text response and no function calls, the task is complete
            if not has_function_calls:
                text_response = " ".join([part.text for part in candidate.content.parts if part.text])
                print("\n[TASK COMPLETE]")
                print(f"Jarvis Final Report: {text_response}")
                break

            # 6. Execute Actions and Capture New State
            print("Executing actions...")
            results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

            # 7. Prepare Function Responses for the next turn
            print("Capturing new environment state...")
            function_responses = get_function_responses(page, results)

            # Append the function responses (including the new screenshot) to history
            # This forms the next 'user' turn for the model to analyze
            contents.extend(function_responses)
            
        else:
            print(f"\n[TASK TIMEOUT] Agent reached the turn limit of {TURN_LIMIT}.")

    except Exception as e:
        print(f"\n[CRITICAL FAILURE] An error occurred during the agent loop: {e}")

    finally:
        # 8. Cleanup
        print("\n--- Cleaning up browser resources ---")
        browser.close()
        playwright_instance.stop()

# --- F. EXECUTION ENTRY POINT ---

if __name__ == "__main__":
    # The complex user prompt that requires navigation, typing, and scrolling
    RESEARCH_GOAL = "Find the cheapest 4K monitor under $500 on Google Shopping. Once the search results load, scroll down once to ensure all listings are visible, and then state the current URL."
    
    run_jarvis_agent(RESEARCH_GOAL)

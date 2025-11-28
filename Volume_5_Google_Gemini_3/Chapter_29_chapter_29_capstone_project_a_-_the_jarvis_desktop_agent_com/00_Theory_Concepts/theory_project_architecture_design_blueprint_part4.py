
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

# Source File: theory_project_architecture_design_blueprint_part4.py
# Description: Project Architecture & Design Blueprint
# ==========================================

import time
from typing import Any, List, Tuple
from playwright.sync_api import sync_playwright

from google import genai
from google.genai import types
from google.genai.types import Content, Part

# --- 1. CONSTANTS AND SETUP ---

# Use the recommended screen dimensions for reliable performance
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
MODEL_NAME = 'gemini-2.5-computer-use-preview-10-2025'
client = genai.Client()

# Initialize Playwright browser instance
print("Initializing browser...")
playwright = sync_playwright().start()
# Set headless=False to see the agent's actions in real-time
browser = playwright.chromium.launch(headless=False)
context = browser.new_context(viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT})
page = context.new_page()


# --- 2. HELPER FUNCTIONS (Denormalization and Execution) ---

def denormalize_x(x: int, screen_width: int) -> int:
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    # Variable: screen_width (The actual pixel width of the viewport)
    return int(x / 1000 * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    # Variable: screen_height (The actual pixel height of the viewport)
    return int(y / 1000 * screen_height)

def execute_function_calls(candidate, page, screen_width, screen_height):
    """
    Parses the model's function calls and executes them using Playwright.
    Returns a list of results for feedback.
    """
    results = []
    function_calls = []
    for part in candidate.content.parts:
        if part.function_call:
            function_calls.append(part.function_call)

    for function_call in function_calls:
        action_result = {}
        fname = function_call.name
        args = function_call.args
        print(f"  -> Executing: {fname}")

        try:
            if fname == "open_web_browser":
                # Browser is already open, action is a no-op
                pass 
            elif fname == "click_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y)
            elif fname == "type_text_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", False)
                clear_before_typing = args.get("clear_before_typing", True)

                page.mouse.click(actual_x, actual_y)
                
                if clear_before_typing:
                    # Clear field using standard shortcut (CMD/CTRL+A, Backspace)
                    page.keyboard.press("Control+A") 
                    page.keyboard.press("Backspace")
                    
                page.keyboard.type(text)
                
                if press_enter:
                    page.keyboard.press("Enter")
            elif fname == "navigate":
                url = args["url"]
                page.goto(url)
            elif fname == "scroll_document":
                direction = args["direction"]
                # Playwright implementation for scroll_document requires using page.evaluate 
                # (simplified here for core actions)
                print(f"Scrolling document {direction}...")
            # NOTE: All other supported actions (hover_at, go_back, etc.) 
            # must be implemented for a production agent.
            else:
                print(f"Warning: Unimplemented or custom function {fname}")

            # Wait for page elements to settle after action
            page.wait_for_load_state(timeout=5000)
            time.sleep(1)

        except Exception as e:
            print(f"Error executing {fname}: {e}")
            action_result = {"error": str(e)}

        results.append((fname, action_result))

    return results

# --- 3. HELPER FUNCTIONS (State Capture and Response) ---

def get_function_responses(page, results):
    """
    Captures the new environment state (screenshot, URL) and packages it
    into FunctionResponse objects to send back to Gemini.
    """
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    function_responses = []
    
    for name, result in results:
        response_data = {"url": current_url}
        response_data.update(result)
        
        # This is the crucial visual feedback loop
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


# --- 4. THE MAIN AGENT LOOP ---

def run_jarvis_agent(initial_prompt: str, start_url: str = "https://www.google.com"):
    try:
        # Go to initial page
        page.goto(start_url)

        # Configure the model (Step 1)
        config = types.GenerateContentConfig(
            tools=[types.Tool(computer_use=types.ComputerUse(
                environment=types.Environment.ENVIRONMENT_BROWSER
            ))],
            thinking_config=types.ThinkingConfig(include_thoughts=True),
        )

        # Initialize history
        initial_screenshot = page.screenshot(type="png")
        USER_PROMPT = initial_prompt
        print(f"Goal: {USER_PROMPT}")

        # First turn contents (Text + Initial Screenshot)
        contents = [
            Content(role="user", parts=[
                Part(text=USER_PROMPT),
                Part.from_bytes(data=initial_screenshot, mime_type='image/png')
            ])
        ]

        # Agent Loop
        turn_limit = 10 # Safety break
        for i in range(turn_limit):
            print(f"\n--- Turn {i+1} ---")
            print("Thinking...")
            
            # 1. Send Request
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=config,
            )

            candidate = response.candidates[0]
            # Add model response to history
            contents.append(candidate.content)

            # Check if the task is finished
            has_function_calls = any(part.function_call for part in candidate.content.parts)
            if not has_function_calls:
                text_response = " ".join([part.text for part in candidate.content.parts if part.text])
                print("Agent finished:", text_response)
                break

            # 2. Execute actions
            print("Executing actions...")
            results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

            # 3. Capture state and generate feedback
            print("Capturing state and generating feedback...")
            function_responses = get_function_responses(page, results)

            # 4. Append feedback to history for the next user turn
            contents.append(
                Content(role="user", parts=[Part(function_response=fr) for fr in function_responses])
            )

    except Exception as e:
        print(f"\nCritical Error in Agent Loop: {e}")
        
    finally:
        # Cleanup
        print("\nClosing browser...")
        browser.close()
        playwright.stop()

# Example usage (This line will be executed later in the chapter)
# run_jarvis_agent("Search for the current stock price of Google and copy the number.")

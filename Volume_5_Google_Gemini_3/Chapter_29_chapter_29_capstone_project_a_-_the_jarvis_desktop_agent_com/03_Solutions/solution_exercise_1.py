
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
import os
import io
from typing import Any, List, Tuple, Dict, Optional

# Playwright is required for browser control and screen capture
from playwright.sync_api import sync_playwright

# Google GenAI imports for the client, types, and content structure
from google import genai
from google.genai import types
from google.genai.types import Content, Part

# --- 1. Initialization and Constants ---

# CRITICAL: Initialize the Gemini Client. 
# Assumes GEMINI_API_KEY is set in the environment variables.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    exit()

# Model constant as specified in the official documentation
COMPUTER_USE_MODEL = 'gemini-2.5-computer-use-preview-10-2025'

# Recommended screen dimensions for optimal Computer Use model performance (16:10 aspect ratio)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
NORMALIZED_GRID = 1000

# --- 2. Coordinate Denormalization Helpers ---

def denormalize_x(x: int, screen_width: int) -> int:
    """
    Converts a normalized x coordinate (0-1000) provided by the model 
    into an actual pixel coordinate based on the screen width.
    """
    # Ensure x is clamped between 0 and 1000 before scaling
    x = max(0, min(NORMALIZED_GRID, x))
    return int(x / NORMALIZED_GRID * screen_width)

def denormalize_y(y: int, screen_height: int) -> int:
    """
    Converts a normalized y coordinate (0-1000) provided by the model 
    into an actual pixel coordinate based on the screen height.
    """
    # Ensure y is clamped between 0 and 1000 before scaling
    y = max(0, min(NORMALIZED_GRID, y))
    return int(y / NORMALIZED_GRID * screen_height)

# --- 3. Action Execution Handler (The Core Logic) ---

def execute_function_calls(
    candidate: types.Candidate, 
    page: Any, 
    screen_width: int, 
    screen_height: int
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Parses the model's response for function calls (UI actions) and executes them 
    using Playwright. Returns the results for subsequent FunctionResponses.
    
    Args:
        candidate: The model's candidate response containing function calls.
        page: The Playwright page object representing the browser window.
        screen_width: The actual width of the viewport.
        screen_height: The actual height of the viewport.

    Returns:
        A list of tuples: (function_name, execution_result_dict).
    """
    results: List[Tuple[str, Dict[str, Any]]] = []
    function_calls: List[types.FunctionCall] = [
        part.function_call for part in candidate.content.parts if part.function_call
    ]

    # Check for safety decisions (e.g., require_confirmation)
    # NOTE: A full production agent must handle safety_decision fields 
    # (like 'require_confirmation') before execution. We proceed here 
    # assuming 'regular/allowed' for demonstration simplicity.

    for function_call in function_calls:
        action_result: Dict[str, Any] = {}
        fname = function_call.name
        args = function_call.args
        
        print(f"\n[AGENT ACTION] -> Executing: {fname} with args: {args}")

        try:
            # --- Browser Navigation and Control Actions ---
            if fname == "open_web_browser":
                # In this setup, the browser is already open via Playwright initialization.
                print("    -> Browser already initialized.")
                pass
            
            elif fname == "navigate":
                url = args.get("url")
                if url:
                    page.goto(url)
                else:
                    raise ValueError("URL argument missing for navigate.")
            
            elif fname == "search":
                # Navigates to the default search engine (assuming Google)
                page.goto("https://www.google.com")

            elif fname == "go_back":
                page.go_back()
            
            elif fname == "go_forward":
                page.go_forward()

            elif fname == "wait_5_seconds":
                print("    -> Waiting 5 seconds for content to load...")
                time.sleep(5)
            
            # --- Mouse/Pointer Actions ---

            elif fname == "click_at":
                x = args.get("x")
                y = args.get("y")
                if x is None or y is None:
                    raise ValueError("Coordinates missing for click_at.")
                
                actual_x = denormalize_x(x, screen_width)
                actual_y = denormalize_y(y, screen_height)
                page.mouse.click(actual_x, actual_y)
            
            elif fname == "hover_at":
                x = args.get("x")
                y = args.get("y")
                if x is None or y is None:
                    raise ValueError("Coordinates missing for hover_at.")
                
                actual_x = denormalize_x(x, screen_width)
                actual_y = denormalize_y(y, screen_height)
                page.mouse.move(actual_x, actual_y) # Playwright uses move for hover

            elif fname == "drag_and_drop":
                # NOTE: This is a complex action requiring start/end coordinates.
                x1 = args.get("x1")
                y1 = args.get("y1")
                x2 = args.get("x2")
                y2 = args.get("y2")
                
                if None in [x1, y1, x2, y2]:
                    raise ValueError("Start/end coordinates missing for drag_and_drop.")
                
                actual_x1 = denormalize_x(x1, screen_width)
                actual_y1 = denormalize_y(y1, screen_height)
                actual_x2 = denormalize_x(x2, screen_width)
                actual_y2 = denormalize_y(y2, screen_height)

                page.mouse.move(actual_x1, actual_y1)
                page.mouse.down()
                page.mouse.move(actual_x2, actual_y2, steps=10)
                page.mouse.up()
                print(f"    -> Dragged from ({actual_x1}, {actual_y1}) to ({actual_x2}, {actual_y2}).")


            # --- Input and Keyboard Actions ---

            elif fname == "type_text_at":
                x = args.get("x")
                y = args.get("y")
                text = args.get("text")
                press_enter = args.get("press_enter", True)
                clear_before_typing = args.get("clear_before_typing", True)

                if None in [x, y, text]:
                    raise ValueError("Coordinates or text missing for type_text_at.")

                actual_x = denormalize_x(x, screen_width)
                actual_y = denormalize_y(y, screen_height)

                # 1. Click to focus the element
                page.mouse.click(actual_x, actual_y)

                # 2. Clear the field if requested (standard method: Select All + Backspace)
                if clear_before_typing:
                    # Use 'Control+A' for Windows/Linux or 'Meta+A' (Command+A) for Mac
                    # Since this is a capstone, we stick to a common cross-platform approach or choose one.
                    # Playwright supports OS-agnostic key names like 'Control' or 'Meta'
                    if os.name == 'posix': # Mac/Linux
                        page.keyboard.press("Meta+A") 
                    else: # Windows
                        page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                
                # 3. Type the text
                page.keyboard.type(text)
                
                # 4. Press Enter if requested
                if press_enter:
                    page.keyboard.press("Enter")

            elif fname == "key_combination":
                keys = args.get("keys")
                if keys:
                    # Example: 'Control+A', 'Enter', 'Shift+Tab'
                    page.keyboard.press(keys)
                else:
                    raise ValueError("Keys argument missing for key_combination.")


            # --- Scrolling Actions ---

            elif fname == "scroll_document":
                direction = args.get("direction")
                if direction not in ["up", "down", "left", "right"]:
                    raise ValueError(f"Invalid direction: {direction}")
                
                # Use Playwright's mouse wheel simulation for smooth, visible scrolling
                if direction == "down":
                    page.mouse.wheel(0, 800)
                elif direction == "up":
                    page.mouse.wheel(0, -800)
                elif direction == "right":
                    page.mouse.wheel(800, 0)
                elif direction == "left":
                    page.mouse.wheel(-800, 0)

            elif fname == "scroll_at":
                # Scrolls a specific element or area. This requires identifying the element 
                # at the coordinate and executing a JS scroll command on it.
                # Since Playwright doesn't easily identify elements purely by coordinate 
                # without an explicit selector, we simulate a scroll on the main document 
                # but log the target coordinate as intended by the model.
                
                x = args.get("x")
                y = args.get("y")
                direction = args.get("direction")
                magnitude = args.get("magnitude", 800) # Default magnitude is 800
                
                print(f"    -> Scroll requested at normalized ({x}, {y}). Simulating document scroll.")

                # Fallback to document scroll simulation based on direction
                if direction == "down":
                    page.mouse.wheel(0, magnitude)
                elif direction == "up":
                    page.mouse.wheel(0, -magnitude)
                # Left/Right scrolling is generally less common for element scrolling,
                # so we focus on vertical scroll for this implementation.

            # --- Unimplemented/Custom Functions ---
            else:
                print(f"Warning: Unimplemented or custom function {fname}. Skipping execution.")
                action_result = {"status": "unimplemented", "function": fname}
                
            
            # CRITICAL: Wait for the action to visually complete and for the page 
            # to finish loading new content after navigation or interaction.
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(1) # Small buffer for visual rendering

        except Exception as e:
            print(f"CRITICAL ERROR executing {fname}: {e}")
            action_result = {"error": str(e), "status": "execution_failed"}

        # Store the result of the execution for the FunctionResponse
        results.append((fname, action_result))

    return results

# --- 4. State Capture and Function Response Generation ---

def get_function_responses(page: Any, results: List[Tuple[str, Dict[str, Any]]]) -> List[Part]:
    """
    Captures the current state (screenshot and URL) and packages it with 
    the results of the executed actions into a list of FunctionResponse Parts.
    """
    print("    -> Capturing new screenshot and URL...")
    
    # Capture the new visual state of the environment
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    
    function_responses: List[Part] = []

    # If multiple actions were executed (parallel calls), we send one response 
    # for each action, all containing the same new screenshot.
    for name, result in results:
        # The response payload must include the current URL and any specific 
        # outcome (like errors) from the execution.
        response_data = {"url": current_url}
        response_data.update(result)
        
        # Construct the FunctionResponse object
        func_response = types.FunctionResponse(
            name=name,
            response=response_data,
            parts=[
                # The screenshot is sent back as an inline image Part
                types.FunctionResponsePart(
                    inline_data=types.FunctionResponseBlob(
                        mime_type="image/png",
                        data=screenshot_bytes
                    )
                )
            ]
        )
        function_responses.append(Part(function_response=func_response))
        
    return function_responses

# --- 5. Main Agent Loop: The Jarvis Desktop Assistant ---

def run_jarvis_agent(user_goal: str, initial_url: str = "https://www.google.com"):
    """
    Initializes the environment and runs the continuous agent loop 
    to achieve the specified user goal using Computer Use capabilities.
    """
    print("--- Jarvis Desktop Agent Initializing ---")
    
    # 1. Setup Playwright Environment
    # We use headless=False so the user can watch the automation in real-time.
    playwright = None
    browser = None
    try:
        print("1. Starting Playwright browser instance...")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        
        # Set the context viewport to match the model's expected dimensions
        context = browser.new_context(
            viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
        )
        page = context.new_page()

        # 2. Navigate to the initial starting page
        print(f"2. Navigating to initial URL: {initial_url}")
        page.goto(initial_url)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # 3. Configure the Model and Initial History
        
        # We include the Computer Use tool, specifying the browser environment.
        config = types.GenerateContentConfig(
            tools=[types.Tool(
                computer_use=types.ComputerUse(
                    environment=types.Environment.ENVIRONMENT_BROWSER,
                    # Optionally, exclude specific dangerous actions if needed
                    # excluded_predefined_functions=["drag_and_drop", "key_combination"]
                )
            )],
            # Including thoughts helps debug and understand the model's reasoning
            thinking_config=types.ThinkingConfig(include_thoughts=True),
        )

        print(f"\n[USER GOAL]: {user_goal}")

        # Capture the very first state (the initial page)
        initial_screenshot = page.screenshot(type="png")

        # Initialize the conversation history with the user's prompt 
        # and the initial visual context (screenshot)
        contents: List[Content] = [
            Content(role="user", parts=[
                Part(text=user_goal),
                Part.from_bytes(data=initial_screenshot, mime_type='image/png')
            ])
        ]

        # 4. Start the Agent Execution Loop
        turn_limit = 10 # Prevent infinite loops
        task_completed = False
        
        for i in range(turn_limit):
            print(f"\n=======================================================")
            print(f"| AGENT TURN {i+1}/{turn_limit}: Reasoning and Planning |")
            print("=======================================================")
            
            # A. Send the current history and state to the model
            response = client.models.generate_content(
                model=COMPUTER_USE_MODEL,
                contents=contents,
                config=config,
            )

            # B. Process the model's response
            if not response.candidates:
                print("Error: Model returned no candidates.")
                break
                
            candidate = response.candidates[0]
            
            # Append the model's thinking and proposed actions to history
            contents.append(candidate.content)

            # Extract text response (often the final answer or summary of action)
            text_response = " ".join([part.text for part in candidate.content.parts if part.text])
            
            # Check if the model suggested any function calls
            has_function_calls = any(part.function_call for part in candidate.content.parts)
            
            # Check if the model included explicit thoughts
            if candidate.thinking_parts:
                print("\n[AGENT THOUGHTS]:")
                for part in candidate.thinking_parts:
                    print(f"    - {part.text}")
            
            if not has_function_calls:
                # The model believes the task is finished or cannot proceed
                print("\n[AGENT RESPONSE]:", text_response)
                task_completed = True
                break

            # C. Execute Actions
            print("\n[AGENT EXECUTION]: Executing proposed actions...")
            results = execute_function_calls(
                candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT
            )

            # D. Capture New State and Respond
            print("\n[AGENT FEEDBACK]: Capturing new state and reporting back...")
            function_responses = get_function_responses(page, results)

            # Append the function responses (including the new screenshot) 
            # as the next user turn, closing the loop.
            contents.append(
                Content(role="user", parts=function_responses)
            )
            
        if not task_completed:
            print("\n--- Agent Loop Terminated ---")
            if i == turn_limit - 1:
                 print("Turn limit reached. Task may be incomplete.")
        else:
            print("\n--- Task Successfully Completed ---")

    except Exception as e:
        print(f"\n[FATAL ERROR IN AGENT]: {e}")
        
    finally:
        # 6. Cleanup
        if browser:
            print("\nClosing browser...")
            browser.close()
        if playwright:
            playwright.stop()
        print("--- Jarvis Agent Shutdown Complete ---")

# --- Example Usage (Simulating Voice Input) ---

if __name__ == "__main__":
    # This simulates receiving a voice command that has been transcribed 
    # into a text prompt.
    
    # CHALLENGE 1: Web Research and Data Extraction
    # The agent must navigate, type, click, scroll, and extract information.
    voice_command_1 = (
        "Go to Wikipedia, search for 'Python programming language', "
        "and scroll down until you see the 'History' section. "
        "Then, tell me the year Python was first released."
    )

    # CHALLENGE 2: Form Filling and Navigation
    # A more complex task requiring multiple steps of typing and clicking.
    # Note: Requires a real website with an interactive form. We use a simpler task 
    # that starts on Google and requires specific navigation.
    voice_command_2 = (
        "Search Google for 'best sci-fi movies 2024'. Click the first result "
        "that takes you to a movie review site, and then click the 'Back' button "
        "in the browser."
    )

    # Choose which challenge to run
    # run_jarvis_agent(user_goal=voice_command_1, initial_url="https://www.wikipedia.org/")
    run_jarvis_agent(user_goal=voice_command_2, initial_url="https://www.google.com/")

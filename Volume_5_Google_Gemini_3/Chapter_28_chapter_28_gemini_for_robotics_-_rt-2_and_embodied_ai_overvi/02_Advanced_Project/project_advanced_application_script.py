
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

import os
import json
from google import genai
from google.genai import types
from typing import List, Dict, Any, Tuple

# --- Configuration and Setup ---

# CRITICAL: Replace with your actual Gemini API Key
# For production, use environment variables or secret managers
try:
    API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    print("FATAL: GEMINI_API_KEY environment variable not set.")
    # Exiting early in a real script, but continuing with a placeholder for demonstration
    API_KEY = "YOUR_MOCK_API_KEY" 

MODEL_ID = "gemini-robotics-er-1.5-preview"
client = genai.Client(api_key=API_KEY)

# Define the robot's physical configuration (normalized 0-1000)
# This is the reference point (0,0) for relative movements
ROBOT_ORIGIN_Y = 800
ROBOT_ORIGIN_X = 500

# --- Mock Environment Functions ---

def load_mock_image_bytes(filename: str) -> bytes:
    """
    Mocks loading an image file. In a real scenario, this would load a camera feed.
    For this script, we assume a placeholder image exists or we use dummy bytes.
    """
    print(f"INFO: Simulating loading image data from '{filename}'...")
    # In a real application, replace this with:
    # with open(filename, 'rb') as f: return f.read()
    # Using a small placeholder byte stream for execution simulation
    return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x77\x53\xde\x00\x00\x00\x0cIDATx\xda\x63\xf8\xff\xff\x3f\x00\x05\xfe\x02\xfe\xcf\x83\x11\x00\x00\x00\x00IEND\xae\x42\x60\x82'

# --- Robot Controller API (Mock Functions) ---

def move(x: int, y: int, high: bool):
    """
    Moves the robotic arm to the given relative coordinates (x, y).
    'high=True' means motion is above obstacles (high clearance).
    'high=False' means motion is near the surface (low clearance/interaction height).
    """
    z_height = 15 if high else 5
    print(f"EXECUTING: move(x={x}, y={y}, z={z_height}) -> {'High Clearance' if high else 'Surface Interaction'}")

def setGripperState(opened: bool):
    """
    Controls the robot's end effector (gripper).
    'opened=True' opens the gripper; 'opened=False' closes the gripper.
    """
    action = "Opening gripper" if opened else "Closing gripper"
    print(f"EXECUTING: setGripperState({opened}) -> {action}")

def returnToOrigin():
    """
    Returns the robot arm to a safe, initial home position.
    """
    print("EXECUTING: returnToOrigin() -> Robot reset complete.")

# --- Helper Functions for Coordination ---

def calculate_relative_coords(normalized_y: int, normalized_x: int) -> Tuple[int, int]:
    """
    Converts normalized image coordinates (0-1000) to relative robot coordinates.
    Note: Image Y (vertical) often maps to Robot X, and Image X (horizontal) 
    often maps to Robot Y, depending on camera calibration. We use a simple 
    subtraction model here.
    """
    # Assuming standard mapping: Image X -> Robot X, Image Y -> Robot Y
    # Relative X = Target X - Origin X
    # Relative Y = Target Y - Origin Y
    
    # In many real setups, the axes are swapped for better control intuition:
    # Let's map normalized X (horizontal) to relative X, and normalized Y (vertical) to relative Y.
    relative_x = normalized_x - ROBOT_ORIGIN_X
    relative_y = normalized_y - ROBOT_ORIGIN_Y
    
    # Scaling factor might be needed here (e.g., divide by 10 for cm), but we use 1:1 for simplicity
    return relative_x, relative_y

def parse_and_locate_objects(image_bytes: bytes, target_prompt: str) -> Dict[str, Tuple[int, int]]:
    """
    Uses Gemini Robotics-ER 1.5 for visual perception and object location.
    Returns a dictionary mapping object labels to their normalized [y, x] coordinates.
    """
    print("\n--- PHASE 1: Visual Perception (Locating Objects) ---")
    
    # Prompt for structured output (JSON format for easy parsing)
    perception_prompt = f"""
        Locate and point to the following items: {target_prompt}. The label 
        returned should be an identifying name for the object detected.
        The answer must follow the json format: 
        [{{\"point\": [y, x], \"label\": <label1>}}, ...].
        The points are in [y, x] format normalized to 0-1000.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
                perception_prompt
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,
                # Use thinking_budget=0 for low-latency spatial understanding
                thinking_config=types.ThinkingConfig(thinking_budget=0) 
            )
        )
        
        # Parse the JSON output
        json_output = json.loads(response.text.strip())
        
        # Map labels to coordinates
        locations = {}
        for item in json_output:
            # Note: item['point'] is [y, x]
            locations[item['label'].lower()] = tuple(item['point']) 
            print(f"Found: {item['label']} at normalized point: {item['point']}")
            
        return locations
        
    except Exception as e:
        print(f"Error during perception phase: {e}")
        # Return mock data if API call fails (for demonstration purposes)
        if API_KEY == "YOUR_MOCK_API_KEY":
            return {
                "damaged blue widget": (450, 200),
                "reject bin": (300, 750),
                "pass bin": (700, 750)
            }
        return {}


def orchestrate_pick_and_place(
    target_label: str, 
    target_coords: Tuple[int, int], 
    dest_label: str, 
    dest_coords: Tuple[int, int]
):
    """
    Uses Gemini Robotics-ER 1.5 with Function Calling to generate the robot action sequence.
    """
    print("\n--- PHASE 2: Task Orchestration (Generating Action Sequence) ---")
    
    # 1. Calculate relative coordinates for the LLM prompt
    target_rel_x, target_rel_y = calculate_relative_coords(target_coords[0], target_coords[1])
    dest_rel_x, dest_rel_y = calculate_relative_coords(dest_coords[0], dest_coords[1])
    
    # 2. Define the robot API for the model to use (Schema definition)
    robot_tools = [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="move",
                    description="Moves the arm to the given relative coordinates (x, y). 'high' boolean controls clearance.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "x": types.Schema(type=types.Type.INTEGER, description="Relative X coordinate from origin."),
                            "y": types.Schema(type=types.Type.INTEGER, description="Relative Y coordinate from origin."),
                            "high": types.Schema(type=types.Type.BOOLEAN, description="True for high clearance, False for surface interaction.")
                        },
                        required=["x", "y", "high"]
                    )
                ),
                types.FunctionDeclaration(
                    name="setGripperState",
                    description="Opens or closes the robot gripper.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "opened": types.Schema(type=types.Type.BOOLEAN, description="True to open, False to close.")
                        },
                        required=["opened"]
                    )
                ),
                types.FunctionDeclaration(
                    name="returnToOrigin",
                    description="Resets the robot to the initial home pose."
                )
            ]
        )
    ]
    
    # 3. Craft the detailed orchestration prompt
    orchestration_prompt = f"""
        You are the control agent for a six-degrees-of-freedom robotic arm. 
        Your task is to perform a pick-and-place operation.
        
        The robot origin is normalized Y={ROBOT_ORIGIN_Y}, X={ROBOT_ORIGIN_X}.
        
        Task: Pick up the '{target_label}' 
        (Relative coordinates: X={target_rel_x}, Y={target_rel_y}) 
        and place it into the '{dest_label}' 
        (Relative coordinates: X={dest_rel_x}, Y={dest_rel_y}).
        
        Steps required:
        1. Move to a high position above the target.
        2. Open the gripper.
        3. Move to the surface level at the target location.
        4. Close the gripper to grasp the object.
        5. Lift the object to a high position.
        6. Move to a high position above the destination.
        7. Move down to the surface level at the destination.
        8. Open the gripper to release the object.
        9. Lift the arm and return to origin.
        
        Provide the sequence of function calls using the available tools as a JSON list of objects, 
        where each object has a "function" key (the function name) and an "args" key (a dictionary 
        of arguments for the function). Include your reasoning before the JSON output.
    """
    
    # 4. Call Gemini to generate the function calls
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[orchestration_prompt],
        config=types.GenerateContentConfig(
            temperature=0.5, # Allows for creative/robust planning
            tools=robot_tools
        )
    )
    
    # 5. Extract reasoning and function calls
    if not response.function_calls:
        print("\nModel Reasoning:")
        print(response.text)
        print("\nERROR: Model failed to generate function calls.")
        return
        
    # The initial text part often contains the reasoning
    reasoning_text = response.text.split('[')[0].strip()
    print("\nModel Reasoning:")
    print(reasoning_text)
    
    # 6. Execute the generated sequence
    print("\n--- PHASE 3: Execution of Orchestrated Actions ---")
    
    for call in response.function_calls:
        function_name = call.name
        args = dict(call.args)
        
        # Use a simple dispatcher to call the local mock functions
        if function_name == "move":
            move(args["x"], args["y"], args["high"])
        elif function_name == "setGripperState":
            setGripperState(args["opened"])
        elif function_name == "returnToOrigin":
            returnToOrigin()
        else:
            print(f"WARNING: Unknown function call: {function_name}")


# --- Main Execution Flow ---

def main_aqcsr_script():
    """Main function to run the Automated Quality Control and Sorting Robot simulation."""
    
    # 1. Define the targets for visual inspection
    TARGET_OBJECTS = "damaged blue widget, reject bin, pass bin"
    
    # 2. Load the image frame
    scene_image_bytes = load_mock_image_bytes("qc_station_frame_1.png")
    
    # 3. Perform Visual Perception
    object_locations = parse_and_locate_objects(scene_image_bytes, TARGET_OBJECTS)
    
    if not object_locations:
        print("\nFATAL: Could not locate required objects. Aborting task.")
        return

    # 4. Identify specific coordinates for the task
    try:
        target_item_label = "damaged blue widget"
        target_item_coords = object_locations[target_item_label]
        
        destination_label = "reject bin"
        destination_coords = object_locations[destination_label]
        
        print(f"\n[SUMMARY] Target Item: {target_item_label} @ {target_item_coords}")
        print(f"[SUMMARY] Destination: {destination_label} @ {destination_coords}")
        print(f"[SUMMARY] Robot Origin: Y={ROBOT_ORIGIN_Y}, X={ROBOT_ORIGIN_X}")

    except KeyError as e:
        print(f"\nFATAL: Missing critical object in scene: {e}. Aborting task.")
        return

    # 5. Execute Task Orchestration (Pick and Place)
    orchestrate_pick_and_place(
        target_item_label, 
        target_item_coords, 
        destination_label, 
        destination_coords
    )

    print("\n\n--- AQCSR Task Complete ---")

if __name__ == "__main__":
    main_aqcsr_script()

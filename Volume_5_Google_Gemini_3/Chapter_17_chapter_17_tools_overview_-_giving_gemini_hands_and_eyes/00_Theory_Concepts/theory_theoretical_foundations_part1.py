
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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

# The Python code defines the tool (the function).
# The model uses the function name, docstring, and type hints
# to understand how to call it.

def get_current_weather(city: str, unit: str = "celsius") -> str:
    """
    Retrieves the current weather conditions for a specified city.
    
    This tool is essential for answering questions related to real-time 
    environmental conditions or planning travel.
    
    Args:
        city: The name of the city for which to retrieve the weather.
        unit: The temperature unit, either 'celsius' or 'fahrenheit'. 
              Defaults to 'celsius'.
              
    Returns:
        A JSON string containing the temperature, humidity, and condition.
    """
    # In a real application, this would call an external API (e.g., OpenWeatherMap)
    # For this example, we return a mock result.
    if "Tokyo" in city:
        return '{"temperature": 25, "humidity": 60, "condition": "Sunny"}'
    elif "London" in city:
        return '{"temperature": 15, "humidity": 85, "condition": "Cloudy"}'
    else:
        return '{"temperature": "N/A", "humidity": "N/A", "condition": "Unknown"}'

# --- The Role of the Boolean Type ---
# Tools often require clear Boolean inputs (True/False) to control execution flow.
# For instance, a function might accept a boolean parameter to force a data refresh.

def toggle_emergency_mode(state: bool) -> str:
    """
    Sets the operational state of the primary reactor.
    
    Args:
        state: Must be True to engage emergency lockdown, or False to disengage.
    
    Returns:
        Confirmation message of the state change.
    """
    if state:
        return "Emergency lockdown engaged successfully."
    else:
        return "Emergency lockdown disengaged. Normal operations resumed."

# In the API call, the developer passes a list of these functions 
# (e.g., [get_current_weather, toggle_emergency_mode]) to the model.
# The Gemini SDK handles the conversion of these Python objects into the 
# required JSON schema for the model's internal reasoning engine.

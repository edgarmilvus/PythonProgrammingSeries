
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
import time
from google import genai
from google.genai.errors import APIError

# --- Setup ---
# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    # Attempt to initialize the client. This will fail if the API key is missing.
    client = genai.Client()
    CLIENT_INITIALIZED = True
except Exception as e:
    print(f"Warning: Error initializing client. Ensure GEMINI_API_KEY is set. Details: {e}")
    CLIENT_INITIALIZED = False
    client = None

# Define the models based on the official documentation provided
LOW_LATENCY_MODEL = "gemini-2.5-flash"
HIGH_REASONING_MODEL = "gemini-2.5-pro"

# --- Utility Function for Benchmarking (Used in E1 and E2) ---

def run_gemini_query(model_name: str, prompt: str):
    """Executes a Gemini API call and measures latency."""
    if not CLIENT_INITIALIZED:
        return f"Client not initialized. Cannot run query on {model_name}.", 0.0
        
    start_time = time.time()
    try:
        # print(f"-> Querying {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        end_time = time.time()
        latency = end_time - start_time
        return response.text, latency
    except APIError as e:
        end_time = time.time()
        latency = end_time - start_time
        return f"API Error ({model_name}): {e}", latency
    except Exception as e:
        end_time = time.time()
        latency = end_time - start_time
        return f"General Error ({model_name}): {e}", latency

# =================================================================
# EXERCISE 1 SOLUTION: High-Volume Latency Benchmark
# =================================================================

def exercise_1_latency_benchmark():
    """Quantifies the latency difference between Flash and Pro."""
    print("\n" + "="*50)
    print("EXERCISE 1: High-Volume Latency Benchmark")
    print("="*50)
    
    if not CLIENT_INITIALIZED: return

    summarization_prompt = (
        "Summarize the following paragraph in one concise sentence: "
        "The Python Software Foundation (PSF) is a non-profit corporation "
        "created in 2001 to promote, protect, and advance the Python programming "
        "language, and to support and facilitate the growth of a diverse and "
        "international community of Python programmers."
    )
    
    num_runs = 5
    flash_latencies = []
    pro_latencies = []
    
    print(f"Running {num_runs} iterations for latency measurement...")

    # Run Flash
    for i in range(num_runs):
        _, latency = run_gemini_query(LOW_LATENCY_MODEL, summarization_prompt)
        flash_latencies.append(latency)
        print(f"  {LOW_LATENCY_MODEL} run {i+1}: {latency:.3f}s")
        
    # Run Pro
    for i in range(num_runs):
        _, latency = run_gemini_query(HIGH_REASONING_MODEL, summarization_prompt)
        pro_latencies.append(latency)
        print(f"  {HIGH_REASONING_MODEL} run {i+1}: {latency:.3f}s")
        
    avg_flash_latency = sum(flash_latencies) / num_runs
    avg_pro_latency = sum(pro_latencies) / num_runs
    
    print("\n--- Benchmark Results ---")
    print(f"Model: {LOW_LATENCY_MODEL} | Avg Latency: {avg_flash_latency:.3f} seconds")
    print(f"Model: {HIGH_REASONING_MODEL} | Avg Latency: {avg_pro_latency:.3f} seconds")
    
    if avg_flash_latency < avg_pro_latency:
        speed_ratio = avg_pro_latency / avg_flash_latency
        print(f"\nConclusion: Flash was approximately {speed_ratio:.1f} times faster for this simple task, validating its low-latency design.")
    else:
        print("\nConclusion: The latency difference was minimal or Pro was faster (may occur due to transient network factors).")

# =================================================================
# EXERCISE 2 SOLUTION: Complex Reasoning Quality Test
# =================================================================

def exercise_2_reasoning_test():
    """Compares Flash and Pro on a complex logical deduction task."""
    print("\n" + "="*50)
    print("EXERCISE 2: Complex Reasoning Quality Test")
    print("="*50)
    
    if not CLIENT_INITIALIZED: return
    
    # A complex prompt requiring logical tracing and understanding of scope/mutability in Python
    complex_prompt = (
        "Analyze the following Python code snippet and explain, step-by-step, "
        "why the final printed value of 'my_list' is [10, 2, 3] and not [1, 2, 3] or [10, 20, 30]. "
        "Be sure to discuss how the function handles mutable arguments and the effect of variable reassignment.\n\n"
        "def modify_list(data):\n"
        "    data[0] = 10\n"
        "    data = [20, 30, 40]\n"
        "    return data\n\n"
        "my_list = [1, 2, 3]\n"
        "new_list = modify_list(my_list)\n"
        "print(my_list)"
    )
    
    # Run Flash
    flash_response, flash_latency = run_gemini_query(LOW_LATENCY_MODEL, complex_prompt)
    print(f"\n[FLASH RESPONSE: {LOW_LATENCY_MODEL} ({flash_latency:.2f}s)]")
    print("-" * 20)
    print(flash_response)
    
    # Run Pro
    pro_response, pro_latency = run_gemini_query(HIGH_REASONING_MODEL, complex_prompt)
    print(f"\n[PRO RESPONSE: {HIGH_REASONING_MODEL} ({pro_latency:.2f}s)]")
    print("-" * 20)
    print(pro_response)
    
    print("\n--- Manual Analysis Note ---")
    print("The Pro model is expected to provide a more detailed, structured explanation, explicitly separating the in-place mutation (affecting global scope) from the local variable reassignment (not affecting global scope), demonstrating superior reasoning.")

# =================================================================
# EXERCISE 3 SOLUTION: Multimodal Model Dispatch Strategy
# =================================================================

# Based on the official documentation provided:
MODEL_DISPATCHER = {
    # Chosen for "price-performance" and "low-latency, high volume tasks."
    "Low_Latency_Chat": "gemini-2.5-flash", 
    
    # Chosen for "state-of-the-art thinking model" and "reasoning over complex problems."
    "Deep_Text_Analysis": "gemini-2.5-pro", 
    
    # Chosen because it supports "Image generation" capability and "Images and text" output.
    "Image_Generation": "gemini-2.5-flash-image", 
    
    # Chosen because it is the only listed model supporting "Audio generation" capability.
    "Text_to_Audio": "gemini-2.5-pro-preview-tts", 
    
    # Chosen as "OUR MOST INTELLIGENT MODEL" for multimodal understanding (Inputs: Text, Image, Video, Audio, and PDF).
    "Next_Gen_Multimodal_Understanding": "gemini-3-pro-preview" 
}

def get_optimal_model(use_case: str):
    """Retrieves the optimal model ID and provides justification based on documentation."""
    model_id = MODEL_DISPATCHER.get(use_case)
    
    if not model_id:
        return f"Error: Use case '{use_case}' not found in dispatcher."
    
    justification = ""
    if use_case == "Low_Latency_Chat":
        justification = "Chosen 'gemini-2.5-flash' for its price-performance ratio and low-latency capabilities, ideal for high-volume chat."
    elif use_case == "Deep_Text_Analysis":
        justification = "Chosen 'gemini-2.5-pro' for its state-of-the-art thinking capabilities, crucial for complex reasoning over long context."
    elif use_case == "Image_Generation":
        justification = "Chosen 'gemini-2.5-flash-image' as it explicitly supports Image Generation output."
    elif use_case == "Text_to_Audio":
        justification = "Chosen 'gemini-2.5-pro-preview-tts' because the documentation lists 'Audio generation' as a supported capability only for this model."
    elif use_case == "Next_Gen_Multimodal_Understanding":
        justification = "Chosen 'gemini-3-pro-preview' as the documentation defines it as 'OUR MOST INTELLIGENT MODEL' for superior multimodal input processing."
        
    print(f"\n--- Model Dispatcher Result ---")
    print(f"Use Case: {use_case}")
    print(f"Optimal Model ID: {model_id}")
    print(f"Justification: {justification}")
    return model_id

# =================================================================
# EXERCISE 4 SOLUTION: Dynamic Model Switching
# =================================================================

class DynamicGeminiClient:
    """
    Simulates dynamic model selection based on user session data and query complexity.
    """
    def __init__(self, flash_model: str, pro_model: str):
        self.flash_model = flash_model
        self.pro_model = pro_model
        self.COMPLEXITY_THRESHOLD = 500  # Character count threshold for complexity

    def get_model_for_query(self, session_data: dict, prompt: str) -> str:
        """
        Determines the optimal model based on user tier and prompt length.
        """
        user_tier = session_data.get('user_tier', 'Standard')
        prompt_length = len(prompt)
        
        print(f"\n[Processing Request] User Tier: {user_tier}, Prompt Length: {prompt_length}")

        if user_tier == "Premium":
            # Premium users pay for the best reasoning model (Pro)
            print(f"-> Logic: Premium Tier detected. Dispatching: {self.pro_model}")
            return self.pro_model
        
        # Logic for Standard Users
        if prompt_length > self.COMPLEXITY_THRESHOLD:
            # Standard user, but the query requires long context/deep work (Pro justification)
            print(f"-> Logic: Standard Tier, but query exceeds {self.COMPLEXITY_THRESHOLD} chars. UPGRADING to: {self.pro_model} for enhanced reasoning.")
            return self.pro_model
        else:
            # Standard user, simple, short query. Use cost-effective, low-latency Flash.
            print(f"-> Logic: Standard Tier, simple query. Dispatching: {self.flash_model} for cost and speed.")
            return self.flash_model

def exercise_4_dynamic_switching():
    print("\n" + "="*50)
    print("EXERCISE 4: Dynamic Model Switching Simulation")
    print("="*50)
    
    dynamic_client = DynamicGeminiClient(
        flash_model=LOW_LATENCY_MODEL, 
        pro_model=HIGH_REASONING_MODEL
    )
    
    # Scenario 1: Premium User, Simple Query
    premium_session = {'user_id': 101, 'user_tier': 'Premium'}
    simple_prompt = "What are the three core principles of object-oriented programming?" # Length ~65
    model_p1 = dynamic_client.get_model_for_query(premium_session, simple_prompt)
    
    # Scenario 2: Standard User, Simple Query
    standard_session = {'user_id': 202, 'user_tier': 'Standard'}
    model_s1 = dynamic_client.get_model_for_query(standard_session, simple_prompt)
    
    # Scenario 3: Standard User, Complex Query (Long Context)
    # Simulate a prompt over 500 characters, forcing an upgrade
    long_context_prompt = "A" * 550 
    model_s2 = dynamic_client.get_model_for_query(standard_session, long_context_prompt)
    
    print("\n--- Final Model Selections Summary ---")
    print(f"1. Premium User (Short Query): {model_p1}")
    print(f"2. Standard User (Short Query): {model_s1}")
    print(f"3. Standard User (Long Query): {model_s2}")


# --- Execute all exercises ---
if CLIENT_INITIALIZED:
    exercise_1_latency_benchmark()
    exercise_2_reasoning_test()
    
    print("\n" + "="*50)
    print("EXERCISE 3: Model Dispatch Strategy Execution")
    print("="*50)
    get_optimal_model("Low_Latency_Chat")
    get_optimal_model("Deep_Text_Analysis")
    get_optimal_model("Image_Generation")
    get_optimal_model("Text_to_Audio")
    get_optimal_model("Next_Gen_Multimodal_Understanding")
    
    exercise_4_dynamic_switching()
else:
    print("\nSkipping live API exercises (1 and 2) due to client initialization failure. Exercises 3 and 4 (logic based) remain valid.")



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

import os
import time
from google import genai
from google.genai.errors import APIError

# --- Configuration and Setup ---

# 1. Initialize the client. The client automatically looks for the GEMINI_API_KEY
# in your environment variables, which is the standard security practice.
try:
    # We initialize the client once for the entire session.
    client = genai.Client()
    print("Gemini Client initialized successfully.")
except Exception as e:
    # Handle case where the environment variable is not set
    print(f"Error initializing client: {e}")
    print("ACTION REQUIRED: Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

# --- Input Data and Task Definition ---

# We use a moderately long technical text block (approx 100 words) to ensure
# the difference in processing time between Flash and Pro models is measurable.
ARTICLE_TEXT = """
The recent advancements in perovskite solar cell technology have revolutionized
the renewable energy sector. Unlike traditional silicon-based photovoltaic cells,
perovskites are solution-processable, meaning they can be manufactured using
low-cost, high-throughput methods like roll-to-roll printing. However, their
primary challenge remains long-term stability under ambient conditions, particularly
humidity and heat. Researchers are currently focusing on encapsulating the active
layers using novel polymeric materials and integrating self-healing mechanisms
to extend their operational lifespan beyond the current laboratory benchmarks.
This stability hurdle is the key factor preventing widespread commercial adoption,
despite their superior efficiency ratings, which often exceed 25% in controlled tests.
If stability issues are resolved, perovskites could drastically lower the cost
of solar energy production globally, impacting grid infrastructure planning
and decentralized power solutions.
"""

# The prompt clearly defines different expectations for each model, reflecting
# their respective strengths (Flash for brevity, Pro for depth).
SUMMARIZATION_PROMPT = (
    "Analyze the following technical text about perovskite solar cells. "
    "If you are the Flash model, provide a single, 15-word, SEO-optimized headline summarizing the core topic. "
    "If you are the Pro model, provide a detailed, three-sentence executive summary "
    "focusing specifically on the current stability challenges and the potential future impact on global energy costs."
)

# --- Core Function for Model Interaction and Benchmarking ---

def run_model_benchmark(model_name: str, prompt: str, text_data: str):
    """
    Executes the generation request against the specified model, measures latency,
    and prints the result and performance metrics.
    """
    # Combine the instruction prompt and the data into the final content payload.
    full_prompt = f"{prompt}\n\n[TEXT TO ANALYZE]:\n{text_data}"
    
    print(f"\n{'='*50}\n--- Running Task on Model: {model_name} ---\n")
    
    start_time = time.time() # Start timing the API call precisely before the request is sent.
    
    try:
        # 2. Call the API, specifying the model code explicitly using the `model` parameter.
        response = client.models.generate_content(
            model=model_name,
            contents=full_prompt,
        )
        
        end_time = time.time() # Stop timing immediately after the response is received.
        latency = end_time - start_time
        
        # 3. Output the metrics and the resulting text.
        print(f"✅ Model Used: {model_name}")
        print(f"⏱️ Latency (Response Time): {latency:.4f} seconds")
        print("-" * 30)
        print("🤖 GENERATED RESPONSE:")
        # Use .strip() to clean up leading/trailing whitespace from the model's output.
        print(response.text.strip())
        print("-" * 30)
        
    except APIError as e:
        # Catch specific API errors (e.g., invalid key, rate limit, invalid model name)
        print(f"🚨 API Error occurred for {model_name}: {e}")
    except Exception as e:
        # Catch other unexpected Python errors
        print(f"❌ An unexpected error occurred: {e}")


# --- Execution: Comparing Flash vs. Pro Capabilities ---

# 4. Define the official model codes from the documentation.
FLASH_MODEL = "gemini-2.5-flash" # The price-performance leader, optimized for speed.
PRO_MODEL = "gemini-2.5-pro"     # The advanced thinking model, optimized for complex reasoning.

# 5. Execute the Quick Preview Task (Flash).
# Goal: Low latency, high throughput, simple task (headline generation).
print("\n[STEP 1: QUICK PREVIEW GENERATION - FLASH MODEL SELECTION]")
run_model_benchmark(
    model_name=FLASH_MODEL,
    prompt=SUMMARIZATION_PROMPT,
    text_data=ARTICLE_TEXT
)

# 6. Execute the Detailed Analysis Task (Pro).
# Goal: High reasoning quality, complex multi-part summary (executive analysis).
print("\n[STEP 2: DETAILED ANALYSIS GENERATION - PRO MODEL SELECTION]")
run_model_benchmark(
    model_name=PRO_MODEL,
    prompt=SUMMARIZATION_PROMPT,
    text_data=ARTICLE_TEXT
)

print(f"\n{'='*50}")
print("BENCHMARK COMPLETE. Analyze the latency difference and the quality of the output.")

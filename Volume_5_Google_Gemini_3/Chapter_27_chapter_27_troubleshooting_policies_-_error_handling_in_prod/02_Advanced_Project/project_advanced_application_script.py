
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

import asyncio
import logging
import random
import time
import os
from google import genai
from google.generativeai.errors import APIError
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 1. Configuration and Setup ---

# Set up structured logging for production diagnostics
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger("GeminiErrorHandler")

# Constants for the retry mechanism
MAX_RETRIES = 5
BACKOFF_BASE_SECONDS = 2  # Starting delay for exponential backoff
MODEL_NAME = 'gemini-2.5-flash'

# Ensure API Key is available
if not os.getenv("GEMINI_API_KEY"):
    logger.error("GEMINI_API_KEY environment variable is not set.")
    # In a real app, this would raise a fatal error or exit.
    # For this example, we assume the environment check passes or mock the client.
    pass 

# Initialize the asynchronous client
try:
    client = genai.AsyncClient()
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    client = None # Handle case where client setup fails

# --- 2. Error Definition and Classification ---

# Define the HTTP status codes that indicate a transient, retriable error.
# Based on the official documentation:
# 429: RESOURCE_EXHAUSTED (Rate Limit) -> Retriable with backoff
# 500: INTERNAL (Server Error/Context Too Long) -> Retriable after wait
# 503: UNAVAILABLE (Service Overloaded) -> Retriable after wait
# 504: DEADLINE_EXCEEDED (Timeout) -> Retriable, possibly with larger client timeout
TRANSIENT_ERROR_CODES = {429, 500, 503, 504}

def is_retriable_error(error: APIError) -> bool:
    """Checks the APIError status code to determine if a retry is warranted."""
    # The APIError object often wraps the underlying HTTP status code.
    # We safely extract the code using dict.get() to prevent KeyError if the structure changes.
    
    # Note: The exact structure of the error object may vary slightly between SDK versions.
    # We assume the error details (like the status code) are accessible or logged.
    
    # Attempt to extract the status code from the error message or attributes
    status_code = getattr(error, 'status_code', None)
    
    if status_code is None:
        # Fallback parsing if status_code attribute is missing (e.g., parsing the message string)
        # For robustness, we check if the error message contains known transient error strings.
        error_message = str(error)
        if "429" in error_message or "50" in error_message:
            return True
        logger.warning(f"Could not determine status code for error: {error_message}")
        return False
        
    return status_code in TRANSIENT_ERROR_CODES

def create_fallback_response(prompt: str, reason: str) -> dict:
    """Generates a standardized failure object for graceful degradation."""
    return {
        "success": False,
        "prompt": prompt,
        "result": None,
        "error_reason": reason,
        "timestamp": time.time()
    }

# --- 3. The Resilient API Call Function ---

async def call_gemini_with_retry(prompt_id: int, prompt: str) -> dict:
    """
    Attempts to call the Gemini API, implementing exponential backoff and jitter 
    for retriable errors (429, 500, 503, 504).
    """
    if client is None:
        return create_fallback_response(prompt, "Client initialization failed.")

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"P{prompt_id}: Attempt {attempt + 1}/{MAX_RETRIES}. Calling Gemini API...")
            
            # Configuration for the request
            config = {
                "temperature": 0.8,
                "safety_settings": [
                    HarmCategory.HARM_CATEGORY_HARASSMENT, HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ]
            }
            
            # Execute the asynchronous API call
            response = await client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt],
                config=config
            )
            
            # Successful response
            logger.info(f"P{prompt_id}: Success on attempt {attempt + 1}. Tokens used: {response.usage_metadata.total_token_count}")
            
            # Safely extract text using dict.get() pattern (though response object is used here,
            # we adhere to the principle of safe data access for structure consistency)
            result_text = response.text
            
            return {
                "success": True,
                "prompt": prompt,
                "result": result_text,
                "tokens": response.usage_metadata.total_token_count
            }

        except APIError as e:
            if is_retriable_error(e):
                # Transient error: Calculate backoff delay
                delay = BACKOFF_BASE_SECONDS * (2 ** attempt)  # Exponential component
                jitter = random.uniform(0, 1)  # Jitter component (0 to 1 second randomness)
                wait_time = delay + jitter
                
                logger.warning(
                    f"P{prompt_id}: Retriable API Error (Attempt {attempt + 1}). Status: {getattr(e, 'status_code', 'Unknown')}. "
                    f"Retrying in {wait_time:.2f}s."
                )
                
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"P{prompt_id}: Max retries reached ({MAX_RETRIES}). Failing request.")
                    break # Exit the retry loop
            
            else:
                # Fatal or Client-side error (400, 403, 404) - DO NOT RETRY
                error_code = getattr(e, 'status_code', 'Unknown')
                logger.critical(
                    f"P{prompt_id}: FATAL API Error ({error_code}). Non-retriable failure: {e}"
                )
                return create_fallback_response(prompt, f"Fatal API Error {error_code}: {e}")
        
        except Exception as e:
            # Catch unexpected exceptions (e.g., connection lost before API call)
            logger.exception(f"P{prompt_id}: Unexpected error during API call: {e}")
            return create_fallback_response(prompt, f"Unexpected Runtime Error: {e}")

    # If the loop completes due to max retries being hit
    return create_fallback_response(prompt, f"Failed after {MAX_RETRIES} attempts due to transient errors.")

# --- 4. Concurrent Task Runner using asyncio.TaskGroup ---

async def process_batch(prompts: list[str]) -> list[dict]:
    """
    Processes a list of prompts concurrently using asyncio.TaskGroup.
    TaskGroup ensures robust handling of exceptions across all tasks.
    """
    tasks = []
    results = []
    
    # Using asyncio.TaskGroup (Python 3.11+) is the modern, safer way 
    # to manage concurrent tasks compared to asyncio.gather().
    async with asyncio.TaskGroup() as tg:
        for i, prompt in enumerate(prompts):
            # Create a task for each prompt with its resilient API call function
            task = tg.create_task(call_gemini_with_retry(i + 1, prompt))
            tasks.append(task)
            
    # TaskGroup automatically handles exceptions and cancellation.
    # The results can be safely retrieved after the 'async with' block completes.
    for task in tasks:
        # The result of the task is the dictionary returned by call_gemini_with_retry
        results.append(task.result()) 
        
    return results

# --- 5. Main Execution and Simulation ---

def main():
    """Defines the workload and runs the asynchronous event loop."""
    
    # Define a set of prompts. We intentionally include prompts that might trigger different issues
    # (e.g., a complex prompt designed to potentially trigger a 504 DEADLINE_EXCEEDED 
    # or a 500 INTERNAL error in a high-load scenario).
    prompts_to_process = [
        "P1: Explain the concept of quantum entanglement in simple terms.",
        "P2: Write a concise summary of the causes of the French Revolution.",
        "P3: Generate a 10-point checklist for deploying a Python web application to production.",
        # P4 is complex/long, simulating a possible 500/504 error under load
        "P4: Analyze the ethical implications of using large language models in judicial decision-making, providing three distinct arguments for and against, and concluding with a synthesis of necessary regulatory frameworks. This response must be exactly 800 words.",
        "P5: What is the capital of Australia?"
    ]
    
    # Note: To simulate a 429 (Rate Limit) error in a real test, you would need to 
    # increase the number of concurrent tasks significantly (e.g., 50+ requests per second) 
    # or temporarily reduce your API quota.
    
    logger.info(f"Starting batch processing of {len(prompts_to_process)} prompts...")
    
    start_time = time.monotonic()
    
    # Run the asynchronous main function
    results = asyncio.run(process_batch(prompts_to_process))
    
    end_time = time.monotonic()
    
    # --- 6. Post-Processing and Reporting ---
    
    successful_count = sum(1 for r in results if r['success'])
    failed_count = len(results) - successful_count
    
    logger.info("-" * 50)
    logger.info(f"Batch Processing Complete in {end_time - start_time:.2f} seconds.")
    logger.info(f"Total Successful Requests: {successful_count}")
    logger.info(f"Total Failed Requests: {failed_count}")
    logger.info("-" * 50)
    
    # Detailed output report
    for result in results:
        status = "SUCCESS" if result['success'] else "FAILURE"
        prompt_snippet = result['prompt'][:30] + '...'
        
        if result['success']:
            # Use dict.get() for safe access, ensuring the key exists before attempting retrieval
            tokens_used = result.get('tokens', 'N/A') 
            logger.info(f"[{status}] {prompt_snippet} | Tokens: {tokens_used}")
        else:
            reason = result.get('error_reason', 'Unknown Failure')
            logger.error(f"[{status}] {prompt_snippet} | Reason: {reason}")
            
    # Example of retrieving a specific successful result
    first_success = next((r for r in results if r['success']), None)
    if first_success:
        print("\n--- Example Successful Output Snippet ---")
        print(first_success['result'][:200] + "...")
        print("---------------------------------------")


if __name__ == "__main__":
    # Ensure the event loop is clean for execution
    main()


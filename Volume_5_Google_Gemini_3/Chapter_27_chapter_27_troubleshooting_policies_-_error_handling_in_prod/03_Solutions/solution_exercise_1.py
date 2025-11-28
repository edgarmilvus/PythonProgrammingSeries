
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
import logging
import asyncio
from random import uniform

# --- Configuration for Logging ---
# Standardized logging format is crucial for production monitoring
logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# --- Mocking the Gemini API Error Structure ---
# In a real application, you would import: from google.generativeai.errors import APIError
class MockAPIError(Exception):
    """
    A mock class simulating google.generativeai.errors.APIError 
    to test error handling logic without live API calls.
    """
    def __init__(self, status_code, message="API Call Failed"):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Status {status_code}: {message}")

def mock_gemini_call(status_code):
    """Simulates a failed API call that raises a specific status code error."""
    if status_code >= 400:
        # Mapping status codes to official documentation descriptions
        if status_code == 400:
            error_msg = "INVALID_ARGUMENT: The request body is malformed."
        elif status_code == 403:
            error_msg = "PERMISSION_DENIED: API key lacks required permissions."
        elif status_code == 429:
            error_msg = "RESOURCE_EXHAUSTED: Exceeded the rate limit."
        elif status_code == 500:
            error_msg = "INTERNAL: Unexpected error occurred on Google's side (e.g., Context too long)."
        elif status_code == 504:
            error_msg = "DEADLINE_EXCEEDED: Service unable to finish processing within deadline."
        elif status_code == 503:
             error_msg = "UNAVAILABLE: Service temporarily overloaded or down."
        else:
            error_msg = f"Unknown API Error (HTTP {status_code})"
        
        raise MockAPIError(status_code, error_msg)
    
    return f"Success (HTTP {status_code})"


# ====================================================================
# SOLUTION 1: Categorizing and Logging Client vs. Server Errors
# ====================================================================

def handle_gemini_call_categorization(status_code):
    """
    Handles API call failures by categorizing the error type based on HTTP status.
    """
    logging.info(f"Attempting API call with simulated status: {status_code}")
    
    try:
        result = mock_gemini_call(status_code)
        logging.info(f"Call successful: {result}")
        return True
    
    except MockAPIError as e:
        # Client Errors (4xx) - Requires input/config fix, no retry
        if e.status_code == 400:
            # 400: INVALID_ARGUMENT
            logging.error(f"FATAL CLIENT ERROR (HTTP 400): {e.message}. Halting execution. Check API reference.")
            return False 
        
        elif e.status_code == 403:
            # 403: PERMISSION_DENIED
            logging.critical(f"CRITICAL AUTH ERROR (HTTP 403): {e.message}. Verify API key and project permissions.")
            return False
            
        elif 400 <= e.status_code < 500:
            # Other 4xx errors (e.g., 404 NOT_FOUND)
            logging.warning(f"CLIENT CONFIGURATION WARNING (HTTP {e.status_code}): {e.message}. Review request parameters.")
            return False
            
        # Server Errors (5xx) - Transient, requires retry
        elif 500 <= e.status_code < 600:
            # 500 (INTERNAL) or 503 (UNAVAILABLE)
            logging.warning(f"TRANSIENT SERVER ERROR (HTTP {e.status_code}): {e.message}. Initiating retry strategy.")
            return True # Indicates that a retry is warranted
        
        else:
            logging.error(f"UNEXPECTED ERROR: {e}")
            return False

print("\n--- Exercise 1: Error Categorization ---")
handle_gemini_call_categorization(200)  # Success
handle_gemini_call_categorization(400)  # Client Error (Halt)
handle_gemini_call_categorization(403)  # Permission Error (Critical)
handle_gemini_call_categorization(503)  # Server Error (Retry)


# ====================================================================
# SOLUTION 2: Implementing Bounded Exponential Backoff for Rate Limits
# ====================================================================

# Helper function to simulate a transient 429 failure
class RateLimitSimulator:
    def __init__(self, failure_count=3):
        self.attempts = 0
        self.failure_count = failure_count

    def call_api(self):
        self.attempts += 1
        if self.attempts <= self.failure_count:
            # Simulate 429 RESOURCE_EXHAUSTED
            raise MockAPIError(429, "RESOURCE_EXHAUSTED: Exceeded the rate limit.")
        else:
            return f"Success on attempt {self.attempts}."

def query_with_backoff(max_retries=5):
    """
    Attempts an API call using exponential backoff (2^n + jitter) for 429 errors.
    """
    simulator = RateLimitSimulator(failure_count=3)
    
    for attempt in range(max_retries):
        try:
            logging.info(f"--- Starting API call attempt {attempt + 1} ---")
            result = simulator.call_api()
            logging.info(f"API Call Succeeded: {result}")
            return result
        
        except MockAPIError as e:
            if e.status_code == 429:
                if attempt == max_retries - 1:
                    logging.critical(f"All {max_retries} retries failed due to 429. Aborting.")
                    raise e

                # Exponential Backoff: 2^attempt
                # Add Jitter (uniform(0, 1)) to prevent stampeding
                delay = (2 ** attempt) + uniform(0, 1)
                
                logging.warning(f"Rate limit hit (429). Retrying in {delay:.2f} seconds (Attempt {attempt + 2}).")
                time.sleep(delay)
            else:
                # Re-raise non-retryable errors
                logging.error(f"Non-retryable error encountered (HTTP {e.status_code}): {e.message}")
                raise e
    
    raise Exception("Exited retry loop unexpectedly.")

print("\n--- Exercise 2: Exponential Backoff ---")
try:
    query_with_backoff(max_retries=5)
except Exception as e:
    print(f"Final Outcome: Backoff process failed. {e}")


# ====================================================================
# SOLUTION 3: Graceful Fallback for Context Window Failures
# ====================================================================

# Helper function to simulate a context failure only for the Pro model
class ContextFailureSimulator:
    def __init__(self):
        self.pro_failed = False

    def generate_content(self, model_name, prompt):
        if model_name == "gemini-2.5-pro":
            if not self.pro_failed:
                self.pro_failed = True
                logging.warning(f"Attempting {model_name}...")
                # Simulating 500 INTERNAL error due to context length
                raise MockAPIError(500, "INTERNAL: Input context is too long for this model.")
            else:
                # If the Pro model is re-called, it succeeds (e.g., because input was reduced)
                return f"PRO Model Success (Reduced Context)"
        
        elif model_name == "gemini-2.5-flash":
            logging.info(f"Attempting {model_name}...")
            return f"FLASH Model Success (Fallback)"
        
        else:
            raise ValueError("Unknown model.")

def adaptive_generation(prompt):
    """
    Attempts generation with a high-end model and falls back to a faster model 
    if a context/internal error (500) occurs, as suggested by the official docs.
    """
    simulator = ContextFailureSimulator()
    
    primary_model = "gemini-2.5-pro"
    fallback_model = "gemini-2.5-flash"
    
    # 1. Attempt with Primary Model
    try:
        logging.info(f"Phase 1: Attempting complex task using {primary_model}.")
        result = simulator.generate_content(primary_model, prompt)
        logging.info(f"Successfully generated content using: {primary_model}")
        return result
        
    except MockAPIError as e:
        if e.status_code == 500:
            # 500 INTERNAL error handling: Trigger graceful fallback
            logging.warning(f"Context/Internal Error detected (HTTP 500): {e.message}. Implementing graceful fallback.")
            
            # 2. Fallback to Secondary Model
            try:
                logging.info(f"Phase 2: Switching to smaller model: {fallback_model}.")
                result = simulator.generate_content(fallback_model, prompt)
                logging.info(f"Successfully generated content using: {fallback_model}")
                return result
            
            except Exception as fallback_e:
                logging.error(f"Fallback attempt failed: {fallback_e}")
                raise Exception("Both primary and fallback models failed.")
        
        else:
            # Handle other non-retryable errors
            logging.error(f"Non-context error encountered (HTTP {e.status_code}): {e.message}")
            raise e

print("\n--- Exercise 3: Graceful Fallback ---")
try:
    adaptive_generation("Generate a 500-page novel outline.")
except Exception as e:
    print(f"Final Outcome: {e}")


# ====================================================================
# SOLUTION 4: Production Asynchronous Error Handling and Timeout Management
# ====================================================================

# Helper function to simulate an async API call that sometimes times out (504)
async def async_mock_gemini_call(operation_id, timeout_duration, should_timeout=False):
    """Simulates an API call that respects an internal timeout."""
    
    if should_timeout:
        # Simulate a process that takes slightly longer than the client timeout
        await asyncio.sleep(timeout_duration + 0.1) 
        # Note: We rely on asyncio.wait_for to raise the TimeoutError, 
        # which we then map to the 504 DEADLINE_EXCEEDED concept.
        # If the API itself returned 504, it would be raised as MockAPIError(504)
        
    else:
        # Simulate successful, fast response
        await asyncio.sleep(0.5) 
        return f"Query {operation_id} completed successfully."

async def async_production_query(operation_id, prompt, client_timeout=5.0, max_attempts=2):
    """
    Asynchronous handler with strict client-side timeout and retry logic for 504 errors.
    """
    for attempt in range(max_attempts):
        start_time = time.time()
        
        # Simulation control: Fail the first attempt (attempt 0)
        should_fail = (attempt == 0)
        
        try:
            logging.info(f"[{operation_id}] Attempt {attempt + 1}: Starting query with client_timeout={client_timeout}s.")
            
            # Enforce client-side timeout using asyncio.wait_for
            result = await asyncio.wait_for(
                async_mock_gemini_call(operation_id, client_timeout, should_fail),
                timeout=client_timeout
            )
            
            duration = time.time() - start_time
            logging.info(f"[{operation_id}] SUCCESS in {duration:.2f}s. Result: {result}")
            return result

        except asyncio.TimeoutError:
            # This catches the client-side enforcement of the timeout (504 concept)
            error_code = 504
            error_msg = "DEADLINE_EXCEEDED (Client Timeout)"
            
            logging.error(f"[{operation_id}] PRODUCTION FAILURE (HTTP {error_code}): {error_msg}. Request exceeded {client_timeout}s.")
            
            if attempt < max_attempts - 1:
                # Retry logic for transient timeout issues
                retry_delay = 1.0 
                logging.warning(f"[{operation_id}] Retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
            else:
                logging.critical(f"[{operation_id}] Final attempt failed after {max_attempts} tries. Aborting task.")
                return f"Task failed after {max_attempts} attempts."

        except MockAPIError as e:
            # Handle API-side errors (e.g., 429 or 500)
            logging.error(f"[{operation_id}] API ERROR (HTTP {e.status_code}): {e.message}")
            return f"Task failed due to API Error: {e.status_code}"

        except Exception as e:
            logging.error(f"[{operation_id}] UNHANDLED EXCEPTION: {e}")
            return f"Task failed due to unexpected error."

async def run_async_production_test():
    """Simulates running multiple concurrent tasks."""
    logging.info("--- Starting Async Production Test ---")
    
    # Task 1: Fails once with 504 timeout, then succeeds on retry
    task1 = async_production_query("ID_001", "Complex Report", client_timeout=2.0, max_attempts=2)
    
    # Task 2: Succeeds immediately (max_attempts=1, should_fail=False for attempt 0)
    task2 = async_production_query("ID_002", "Simple Summary", client_timeout=10.0, max_attempts=1)

    results = await asyncio.gather(task1, task2)
    logging.info(f"All tasks completed.")


print("\n--- Exercise 4: Async Production Handling & Timeout ---")
if __name__ == '__main__':
    # Running the asyncio event loop
    asyncio.run(run_async_production_test())

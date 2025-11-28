
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

# Source File: theory_theoretical_foundations_part2.py
# Description: Theoretical Foundations
# ==========================================

import time
import random
import logging
from typing import Optional, Dict, Any, Callable

# 1. Setup Logging for Production Visibility
# Production systems often use structured logging (e.g., JSON logs) piped to a service (e.g., Splunk, Elastic)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. Define Custom Exceptions based on Gemini API Status Codes (from Official Docs)
class GeminiAPIException(Exception):
    """Base exception for all Gemini API errors (Permanent or Transient)."""
    def __init__(self, status_code: int, status_name: str, message: str):
        self.status_code = status_code
        self.status_name = status_name
        super().__init__(f"[{status_code} {status_name}]: {message}")

class InvalidArgumentError(GeminiAPIException):
    """400 INVALID_ARGUMENT - Permanent error, check request format."""
    pass

class PermissionDeniedError(GeminiAPIException):
    """403 PERMISSION_DENIED - Permanent error, check API key/Auth."""
    pass

class ResourceExhaustedError(GeminiAPIException):
    """429 RESOURCE_EXHAUSTED - Transient error: Rate limit exceeded."""
    pass

class InternalServerError(GeminiAPIException):
    """500 INTERNAL - Transient/Permanent error: Server issue, or context too long."""
    pass

class TransientUnavailableError(GeminiAPIException):
    """503 UNAVAILABLE - Transient error: Service temporarily overloaded/down."""
    pass

# 3. Core Strategy: Exponential Backoff with Jitter Implementation
# Note: In a real asyncio environment, time.sleep would be replaced by await asyncio.sleep
def exponential_backoff_retry(max_retries: int = 5, initial_delay: float = 1.0) -> Callable:
    """
    Decorator implementing exponential backoff for recognized transient errors (429, 500, 503).
    """
    TRANSIENT_ERRORS = (ResourceExhaustedError, InternalServerError, TransientUnavailableError)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except TRANSIENT_ERRORS as e:
                    # 429, 500, 503 caught here
                    if attempt == max_retries - 1:
                        logging.error(f"Final attempt failed for {func.__name__}. Error: {e}")
                        raise # Re-raise the exception if max retries reached

                    # Calculate exponential delay (Base * 2^Attempt)
                    exponential_delay = initial_delay * (2 ** attempt)
                    # Add Full Jitter (random delay between 0 and exponential_delay)
                    delay = random.uniform(0, exponential_delay) 
                    
                    logging.warning(
                        f"Transient error detected ({e.status_code} {e.status_name}). "
                        f"Retrying in {delay:.2f}s (Attempt {attempt + 1}/{max_retries})."
                    )
                    time.sleep(delay)
                
                except (InvalidArgumentError, PermissionDeniedError) as e:
                    # Handle permanent errors (400, 403) immediately
                    logging.critical(f"Permanent API Error encountered: {e}")
                    raise # Do not retry permanent errors
                
                except GeminiAPIException as e:
                    # Catch other specific API exceptions (e.g., 404 NOT_FOUND)
                    logging.error(f"Uncategorized API Error: {e}")
                    raise
            
            # This line should ideally not be reached
            raise Exception("Retry loop completed without success or final failure.")
            
        return wrapper
    return decorator

# 4. Simulation of a core Gemini API Call
# This simulates the SDK mapping HTTP status codes to our custom exceptions.
class RequestSimulator:
    """Manages state for simulating transient failures."""
    def __init__(self):
        self.counter = 0
        self.fail_until_attempt = 3 # Fails on attempts 1 and 2, succeeds on 3

    def simulate_request(self, prompt: str, model: str) -> Dict[str, Any]:
        self.counter += 1
        
        # Simulation of a successful response
        if self.counter > self.fail_until_attempt:
            # Defensive Programming using dict.get() (Reference Injection)
            return {
                "response": f"Successful generation using {model} on attempt {self.counter}", 
                "tokens_used": 150,
                # 'metadata' key is intentionally missing sometimes, handled below
            }

        # Simulation of a Permanent Error (400)
        if len(prompt) < 10:
             raise InvalidArgumentError(400, "INVALID_ARGUMENT", "Prompt is too short and malformed (400).")

        # Simulation of Transient Failures (429, 503, 500)
        error_code = random.choice([429, 503, 500])
        
        if error_code == 429:
            raise ResourceExhaustedError(429, "RESOURCE_EXHAUSTED", "Rate limit exceeded (429).")
        elif error_code == 503:
            raise TransientUnavailableError(503, "UNAVAILABLE", "Service temporarily overloaded (503).")
        elif error_code == 500:
            # Simulate context window issue after 1st attempt
            if self.counter == 1:
                raise InternalServerError(500, "INTERNAL", "Server encountered an unexpected error (500).")
            else:
                # Simulate a different 500 error that might be context related
                raise InternalServerError(500, "INTERNAL", f"Input context too long for {model} (500).")

        # This should not be reached
        raise Exception("Simulator logic error.")

SIMULATOR = RequestSimulator() # Global simulator instance

# 5. Application of the Strategy with Fallback Logic
@exponential_backoff_retry(max_retries=3)
def generate_content_with_retry(prompt: str, model: str) -> Dict[str, Any]:
    """Tries to generate content, retrying transient errors up to 3 times."""
    # In a real application, this would call the actual SDK:
    # client.models.generate_content(model=model, contents=prompt)
    
    # We use the simulator here:
    result = SIMULATOR.simulate_request(prompt, model) 

    # Defensive check: Ensure we get a response key, defaulting to empty string if missing.
    response_text = result.get('response', '') 
    if not response_text:
        logging.error("API call succeeded but returned empty 'response' field.")
        # Raise a custom error if the structure is invalid, even if HTTP was 200
        raise Exception("Malformed response structure from API.")
        
    return result

def primary_generation_pipeline(prompt: str) -> str:
    """
    Implements the full production pipeline including retry, fallback, and graceful failure.
    """
    # Reset simulator for clean run
    SIMULATOR.counter = 0 
    SIMULATOR.fail_until_attempt = 3 # Ensure initial transient failure simulation
    
    try:
        # --- Attempt 1: Primary Model (gemini-1.5-pro) with Retries ---
        logging.info("Starting primary generation pipeline (Pro model)...")
        response_data = generate_content_with_retry(prompt, model="gemini-1.5-pro")
        
        # Successful execution
        return f"Primary Success: {response_data['response']}"

    except (ResourceExhaustedError, TransientUnavailableError) as e:
        # --- Fallback Trigger: Transient errors exhausted retries (429, 503) ---
        logging.warning(f"Pro model failed after retries ({e.status_name}). Initiating fallback to Flash model.")
        
        try:
            # Temporarily switch to the faster/cheaper model (gemini-1.5-flash)
            # Note: We must define a separate retry strategy or manually handle retries for the fallback call
            # For simplicity, we manually call the simulator here and force immediate success (fail_until_attempt=0)
            SIMULATOR.counter = 0 
            SIMULATOR.fail_until_attempt = 0 
            
            # The fallback model usually has slightly different parameters or rate limits
            fallback_response = generate_content_with_retry(prompt, model="gemini-1.5-flash")
            
            return f"Fallback Success (Flash Model): {fallback_response['response']}"
            
        except Exception as fallback_e:
            logging.critical(f"Fallback also failed after retries. System is under severe load.")
            # Graceful Failure: Return a standardized, user-friendly message
            return "System Error: The AI service is currently unavailable. Please try again shortly."
            
    except InternalServerError as e:
        # --- Specific Handling for 500 Errors (Context Window) ---
        logging.error(f"Internal Server Error (500) after retries. Possible context window overflow.")
        # In a real system, context reduction or summarization logic would be triggered here before a final attempt.
        return "Error: Input context too large for the model. Please shorten your request."

    except InvalidArgumentError as e:
        # --- Handling Permanent 400 Errors ---
        return f"Configuration Error: {e.status_name}. Check request formatting."
        
    except Exception as e:
        # Catch all unforeseen system errors (e.g., network timeout outside the API wrapper)
        logging.critical(f"Unforeseen System Failure: {e}")
        return "A critical, unexpected system error occurred."


# --- Execution Demonstration ---

print("\n-------------------------------------------------------------------------------------------------")
print("DEMO 1: Successful Retry (Simulating 2 failures, success on attempt 3)")
print("-------------------------------------------------------------------------------------------------")
result_1 = primary_generation_pipeline("Write a detailed technical summary of exponential backoff.")
print(f"\nFINAL RESULT 1: {result_1}")


print("\n-------------------------------------------------------------------------------------------------")
print("DEMO 2: Permanent Error (Simulating 400 INVALID_ARGUMENT)")
print("-------------------------------------------------------------------------------------------------")
result_2 = primary_generation_pipeline("A") # Prompt too short triggers 400 immediately
print(f"\nFINAL RESULT 2: {result_2}")

# Note: To observe the fallback logic (Demo 3), the simulator would need to be configured 
# to fail all 3 retries, leading to the ResourceExhaustedError, which triggers the fallback block.

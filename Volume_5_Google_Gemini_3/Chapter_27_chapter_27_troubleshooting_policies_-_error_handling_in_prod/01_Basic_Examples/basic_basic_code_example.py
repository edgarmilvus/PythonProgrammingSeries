
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
from google.generativeai.types import APIError

# --- Configuration ---
# Define the maximum number of times we will attempt the API call.
MAX_RETRIES = 3
# Define the base delay between retries (in seconds).
BASE_RETRY_DELAY = 5
# Define the model we are targeting.
MODEL_NAME = 'gemini-2.5-flash'

def safe_generate_content(prompt: str) -> str:
    """
    Attempts to call the Gemini API, implementing a basic retry mechanism
    for transient server errors (like 429, 500, or 503).
    """
    
    # 1. Initialize the Client (Assumes GEMINI_API_KEY is set in environment)
    try:
        client = genai.Client()
    except Exception as e:
        # Handle client initialization failure (e.g., API key missing)
        print(f"FATAL SETUP ERROR: Could not initialize Gemini client. Check API key. Details: {e}")
        raise

    # 2. Start the Retry Loop
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"--- Attempt {attempt} of {MAX_RETRIES} ---")
        
        try:
            # 3. The Core API Call
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            
            # If successful, return immediately
            print("API call successful.")
            return response.text

        # 4. Catch Specific Gemini API Errors
        except APIError as e:
            # The SDK wraps the HTTP status code and details within the APIError object.
            # We must inspect the error to determine if it is retriable.

            # Simple inspection of the error message for status codes (often embedded)
            error_message = str(e)
            
            # Check for retriable errors: 429 (Rate Limit), 500 (Internal), 503 (Unavailable)
            # According to the official documentation, these are the primary transient issues.
            if "429" in error_message or "500" in error_message or "503" in error_message:
                
                # Calculate the delay. In a real system, this would be exponential backoff.
                # Here, we use a simple linear increase for clarity.
                current_delay = BASE_RETRY_DELAY * attempt
                
                print(f"Transient error detected (e.g., Rate Limit or Server Overload).")
                print(f"Error details: {error_message}")
                
                # If this is the last attempt, we don't sleep, we just break and raise the final error.
                if attempt < MAX_RETRIES:
                    print(f"Waiting {current_delay} seconds before retrying...")
                    time.sleep(current_delay)
                else:
                    print("Maximum retries reached. Raising final exception.")
                    break # Exit loop to execute the final 'raise' block
            
            # 5. Handle Non-Retriable Errors (Client Errors)
            elif "400" in error_message or "404" in error_message or "403" in error_message:
                # 400 (INVALID_ARGUMENT), 404 (NOT_FOUND), 403 (PERMISSION_DENIED)
                # These are usually caused by bad input, incorrect parameters, or wrong keys.
                # Retrying immediately will not fix the problem. We fail fast.
                print(f"CRITICAL CLIENT ERROR detected (HTTP 4xx). Retrying is futile.")
                print(f"Error details: {error_message}")
                raise
            
            # 6. Handle Unexpected Errors (Catch-all for APIError)
            else:
                # Any other APIError that doesn't fit the retriable/non-retriable pattern
                print(f"UNHANDLED API ERROR. Error details: {error_message}")
                raise

        # 7. Catch General Exceptions (e.g., network timeout before reaching the API)
        except Exception as e:
            print(f"A non-API related exception occurred (e.g., network issue): {e}")
            if attempt < MAX_RETRIES:
                print(f"Waiting {BASE_RETRY_DELAY} seconds before retrying...")
                time.sleep(BASE_RETRY_DELAY)
            else:
                print("Maximum retries reached for general exception.")
                raise e # Re-raise the original exception
                
    # 8. Final Failure Point
    # If the loop completes without returning (i.e., it hit the 'break' in step 4 or 5),
    # we raise the last known API error to signal failure.
    # Note: In a production system, you would raise a custom exception here.
    raise APIError(f"Gemini API failed after {MAX_RETRIES} attempts due to persistent transient issues.")

# --- Example Usage ---
if __name__ == "__main__":
    # Ensure the API key is set before running
    if 'GEMINI_API_KEY' not in os.environ:
        print("WARNING: GEMINI_API_KEY environment variable not set.")
        print("The script will likely fail with a 403 or client initialization error.")
        # We will simulate a successful run if the key is present, 
        # but the mechanism is ready for errors.
        # For demonstration purposes, we use a benign prompt.
        
    try:
        # Example 1: A prompt that should succeed normally
        result = safe_generate_content("Explain the difference between a context manager and an event loop in Python.")
        print("\n--- Final Successful Result ---")
        print(result[:200] + "...")
        
        # Example 2: To test the failure path, you would need to simulate a 429 error
        # (e.g., by rapidly spamming the API or using a mock object, which is beyond this basic scope).
        
    except APIError as final_e:
        print(f"\nFATAL: The API call failed completely after all retries. Details: {final_e}")
    except Exception as final_e:
        print(f"\nFATAL: A non-API error stopped the process. Details: {final_e}")

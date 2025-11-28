
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

import sys
import string

# --- Module-Level Documentation ---
"""
SLUG_GENERATOR.PY: A utility for creating clean, URL-friendly text slugs.

This script takes a string input from the command line and converts it into 
a standardized format: lowercase, spaces replaced by hyphens, and most 
punctuation removed. It prioritizes readability and clear commenting 
over complex string manipulation methods (like regular expressions) 
to align with foundational concepts.

Usage: python slug_generator.py "Your long title here"
"""

# --- Configuration Constants (Improving Readability) ---
# Constants are named in ALL_CAPS with underscores, adhering to standard Python conventions.
EXIT_CODE_SUCCESS = 0
EXIT_CODE_ERROR = 1
HYPHEN_REPLACEMENT = '-'
MAX_SLUG_LENGTH = 50 

# Define characters that are explicitly allowed in the final slug.
# Note: We include digits and letters, but explicitly exclude common punctuation.
ALLOWED_CHARS = string.ascii_letters + string.digits + ' '

def display_usage():
    """
    Displays the correct usage instructions for the script and exits.
    
    This function ensures that if the user runs the script incorrectly, 
    they receive immediate, helpful feedback, improving the user experience.
    """
    # Use multi-line triple quotes for clear, formatted instructional text.
    usage_message = f"""
----------------------------------------------------------------------
Usage Error: Missing Input Text

Please provide the text you wish to standardize as a command-line argument.

Example:
    python {sys.argv[0]} "The Foundations of Python: Chapter Five"
    
This will generate a slug like: 'the-foundations-of-python-chapter-five'
----------------------------------------------------------------------
"""
    print(usage_message)
    # Exit with an error code to signal failure to the operating system.
    sys.exit(EXIT_CODE_ERROR)


def create_slug(raw_text: str) -> str:
    """
    Core function to convert raw text into a standardized slug.

    Parameters:
        raw_text (str): The input string to be processed.

    Returns:
        str: The cleaned, hyphenated, and length-limited slug.
    """
    
    # 1. Standardization: Convert the entire string to lowercase.
    # This step ensures uniformity, adhering to the principle that 
    # consistency is key for readability and searchability.
    lower_text = raw_text.lower()
    
    # 2. Character Filtering Loop
    # We build the slug character by character, only including allowed elements.
    # This approach is clear and easy to debug (Readability counts!).
    filtered_chars = []
    
    for char in lower_text:
        # Check if the character is in our predefined set of allowed characters.
        if char in ALLOWED_CHARS:
            filtered_chars.append(char)
        # Note: We intentionally skip all other characters (e.g., #, $, !, ?, etc.)
        # This is simpler and safer than trying to explicitly list all forbidden characters.
        
    # Rejoin the list of characters back into a string.
    semi_cleaned_text = "".join(filtered_chars)
    
    # 3. Space Replacement and Trimming
    # Replace all remaining spaces with the defined hyphen replacement.
    normalized_slug = semi_cleaned_text.strip().replace(' ', HYPHEN_REPLACEMENT)
    
    # 4. Cleanup: Handle redundant hyphens.
    # If the original text had multiple spaces or leading/trailing punctuation 
    # that was filtered out, we might have double hyphens (e.g., 'a--b').
    # We loop to replace double hyphens until none are left.
    while HYPHEN_REPLACEMENT * 2 in normalized_slug:
        normalized_slug = normalized_slug.replace(HYPHEN_REPLACEMENT * 2, HYPHEN_REPLACEMENT)

    # 5. Length Enforcement
    # Ensure the slug does not exceed the defined maximum length.
    if len(normalized_slug) > MAX_SLUG_LENGTH:
        # Truncate the string and ensure we don't end on a hyphen if we cut mid-word.
        normalized_slug = normalized_slug[:MAX_SLUG_LENGTH].rstrip(HYPHEN_REPLACEMENT)
        
    return normalized_slug


def main():
    """
    The main execution flow of the script.
    
    Handles command-line argument parsing and coordinates the slug generation.
    """
    
    # sys.argv is a list containing command-line arguments.
    # sys.argv[0] is the script name itself.
    # We expect at least two elements: [script_name, input_text].
    if len(sys.argv) < 2:
        # If input is missing, display help and terminate.
        display_usage()
        
    # Retrieve the raw text input from the command line.
    # The input text is the second element in the list (index 1).
    raw_input_text = sys.argv[1]
    
    # Verify that the input text is not empty or just whitespace.
    if not raw_input_text.strip():
        print("Error: Input text cannot be empty.")
        sys.exit(EXIT_CODE_ERROR)
        
    # Call the core function to perform the transformation.
    final_slug = create_slug(raw_input_text)
    
    # Output the result clearly to the user.
    print(f"\nOriginal Input: '{raw_input_text}'")
    print(f"Generated Slug: '{final_slug}'\n")
    
    # Exit successfully.
    sys.exit(EXIT_CODE_SUCCESS)


# --- Execution Guard ---
# This standard construct ensures that the 'main()' function only runs 
# when the script is executed directly, not when it is imported as a module.
if __name__ == "__main__":
    main()


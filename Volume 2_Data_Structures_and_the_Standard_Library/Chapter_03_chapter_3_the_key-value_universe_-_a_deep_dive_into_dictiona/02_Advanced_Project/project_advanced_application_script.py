
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

# prompt_manager.py
import json
from datetime import datetime

# --- 1. Core Dictionary Definitions ---

# DEFAULT_SETTINGS: Provides baseline configuration values.
# This dictionary ensures consistency across all workflows.
DEFAULT_SETTINGS = {
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 2048,
    "timestamp_format": "%Y-%m-%d %H:%M:%S" # Used for logging with strftime
}

# PROMPT_TEMPLATES: A dictionary of dictionaries defining specific workflow structures.
# This structure maps template names (keys) to their operational details (values).
PROMPT_TEMPLATES = {
    "summarizer_chain": {
        "system_instruction": "You are an expert summarization engine.",
        "user_input_format": "Summarize the following text efficiently: {text}",
        "required_keys": ["text"]
    },
    "translator_chain": {
        "system_instruction": "You are a precise language translator.",
        "user_input_format": "Translate this phrase into French: {phrase}",
        "required_keys": ["phrase"]
    }
}

# Global tracking mechanism: A list to hold configuration log dictionaries.
config_history = []

# --- 2. Utility Functions ---

def get_timestamp(format_str: str) -> str:
    """Uses strftime to format the current time into a string."""
    return datetime.now().strftime(format_str)

def initialize_config(template_name: str) -> dict | None:
    """
    Initializes configuration by safely merging defaults and template settings.
    Uses dict.get() for safe template retrieval (Read operation).
    """
    # Attempt to retrieve the template safely. Returns None if key is missing.
    template = PROMPT_TEMPLATES.get(template_name)
    if template is None:
        print(f"Error: Template '{template_name}' not found.")
        return None

    # Dictionary merging: Combines DEFAULT_SETTINGS with template-specific data.
    # This demonstrates the efficient creation of a new dictionary object.
    config = {
        **DEFAULT_SETTINGS,
        "template_name": template_name,
        "system_prompt": template["system_instruction"],
        "user_format": template["user_input_format"],
        "required_keys": template["required_keys"]
    }
    return config

def generate_prompt(config: dict, user_data: dict) -> dict:
    """
    Generates the final nested Prompt Template structure and validates user data.
    """
    # 1. Validate required keys using set operations for efficiency.
    required = set(config["required_keys"])
    provided = set(user_data.keys())
    missing = required - provided
    if missing:
        # Raises ValueError if critical user inputs are missing.
        raise ValueError(f"Missing required data fields: {missing}")

    # 2. Format the user input string using dictionary unpacking for dynamic arguments.
    formatted_user_input = config["user_format"].format(**user_data)

    # 3. Build the final prompt structure (a deeply nested dictionary).
    final_prompt = {
        "messages": [
            {"role": "system", "content": config["system_prompt"]},
            {"role": "user", "content": formatted_user_input}
        ],
        "metadata": {
            # Dictionary comprehension: Efficiently filters specific keys from 'config'.
            k: config[k] for k in ["model", "temperature", "max_tokens"]
        }
    }
    return final_prompt

def execute_chain(template_name: str, user_data: dict, custom_settings: dict = None) -> dict | None:
    """
    Main driver function simulating the execution of an LLM Chain.
    Manages initialization, updating, and logging.
    """
    print(f"\n--- Starting Chain: {template_name} ---")

    # 1. Initialize configuration
    config = initialize_config(template_name)
    if config is None:
        return None

    # 2. Apply custom settings (Update operation)
    if custom_settings:
        # .update() modifies the existing 'config' dictionary in place.
        config.update(custom_settings)

    try:
        # 3. Generate the final structured prompt
        final_prompt_structure = generate_prompt(config, user_data)

        # 4. Log the configuration history using dynamic dictionary creation
        log_entry = {
            "template": template_name,
            "model_used": config["model"],
            "timestamp": get_timestamp(config["timestamp_format"]),
            "status": "Success"
        }
        config_history.append(log_entry)

        print(f"[{log_entry['timestamp']}] Prompt generated successfully using {config['model']}.")
        return final_prompt_structure

    except ValueError as e:
        # 5. Handle errors and log failure
        # .setdefault() is used here to ensure 'status' is recorded even if the chain fails later.
        # Although less critical here, it demonstrates its use for guaranteeing key presence.
        log_failure = {
            "template": template_name,
            "model_used": config.get("model", "Unknown"),
            "timestamp": get_timestamp(DEFAULT_SETTINGS["timestamp_format"]),
            "status": "Failure",
            "error": str(e)
        }
        config_history.append(log_failure)
        print(f"Chain execution failed due to data validation error: {e}")
        return None

# --- EXECUTION EXAMPLE ---

# A. Run a successful summarization Chain with custom overrides
summary_data = {"text": "Python dictionaries are implemented as hash tables, offering O(1) average time complexity for lookups, insertions, and deletions. Keys must be hashable, meaning they must be immutable."}
custom_temp_setting = {"temperature": 0.9, "model": "llama-3"}

result_summary = execute_chain(
    template_name="summarizer_chain",
    user_data=summary_data,
    custom_settings=custom_temp_setting
)

if result_summary:
    print("\n--- Generated Prompt Structure (Nested Dict) ---")
    print(json.dumps(result_summary, indent=2))

# B. Run a failing translation Chain (Missing required key 'phrase')
translation_data_fail = {"word": "Hello", "lang": "French"}
execute_chain(
    template_name="translator_chain",
    user_data=translation_data_fail
)

# C. Display the final history view
print("\n--- Configuration History (Audit Log) ---")
for entry in config_history:
    # Iterating over the list of dictionaries
    status = entry.get('status', 'N/A')
    error_msg = f" ({entry.get('error', 'No Error')})" if status == 'Failure' else ""
    print(f"[{entry['timestamp']}] TEMPLATE: {entry['template']:<20} | STATUS: {status:<8} | MODEL: {entry['model_used']}{error_msg}")

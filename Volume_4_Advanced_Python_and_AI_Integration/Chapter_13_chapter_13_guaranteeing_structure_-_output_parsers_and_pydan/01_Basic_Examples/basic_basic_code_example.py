
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
import json
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

# --- 1. Define the Desired Output Structure using Pydantic ---
class ContactInfo(BaseModel):
    """
    Pydantic model defining the required structure for extracted contact data.
    The Field descriptions are crucial for guiding the LLM's output.
    """
    name: str = Field(description="The full name of the contact person, e.g., 'Dr. Evelyn Reed'.")
    email: str = Field(description="The primary email address, strictly following standard email format.")
    phone_number: str = Field(description="The primary contact phone number, including country code if available.")

# --- 2. Initialize the Parser and Generate Instructions ---
# We instantiate the parser, linking it directly to our defined Pydantic class.
parser = PydanticOutputParser(pydantic_object=ContactInfo)

# The parser generates the specific instructions the LLM needs to follow.
format_instructions = parser.get_format_instructions()

# --- 3. Define the Prompt Template ---
# The template must contain a placeholder for the format instructions.
template = """
You are an expert data extraction AI. Your task is to analyze the user input
and extract the required contact details into a strict JSON format.
Only output the JSON object.

INPUT TEXT:
---
{input_text}
---

FORMAT INSTRUCTIONS:
{format_instructions}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["input_text"],
    # We use partial_variables to inject the static format instructions
    # before the user input is provided.
    partial_variables={"format_instructions": format_instructions}
)

# --- 4. Define Input Data and LLM Setup ---
unstructured_data = (
    "I just met with Dr. Evelyn Reed, who handles our compliance issues. "
    "You can reach her best at evelyn.reed@compliancecorp.com, or "
    "if it's urgent, call her office line at +1-555-888-9000. Follow up next week."
)

# Initialize the LLM (requires OPENAI_API_KEY environment variable)
# Using temperature=0 ensures deterministic, structured output.
try:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
except Exception:
    print("Warning: LLM initialization failed. Ensure OPENAI_API_KEY is set.")
    exit()

# --- 5. Execute the Chain ---
print("--- 1. Preparing and Sending Request to LLM ---")

# 5a. Format the final prompt payload
formatted_prompt_payload = prompt.format(input_text=unstructured_data)

# 5b. Invoke the LLM
# The LLM returns a raw string, hopefully formatted as JSON.
raw_output_message = llm.invoke(formatted_prompt_payload)
raw_output = raw_output_message.content

print(f"Raw LLM Output (String):\n{raw_output}\n")

# --- 6. Parse and Validate the Output ---
print("--- 2. Parsing and Validation via PydanticOutputParser ---")
try:
    # This crucial step attempts to load the raw JSON string and map it
    # onto the ContactInfo Pydantic model. If types or fields are missing,
    # Pydantic raises a ValidationError.
    validated_object = parser.parse(raw_output)

    # --- 7. Utilize the Structured Data ---
    print("--- 3. Structured Pydantic Object Output (Guaranteed Structure) ---")
    print(f"Type of Result: {type(validated_object)}")
    print(f"Name (Access via object property): {validated_object.name}")
    print(f"Email (Access via object property): {validated_object.email}")
    print(f"Phone (Access via object property): {validated_object.phone_number}")

    # Pydantic objects are easy to serialize for storage or API responses
    print("\n--- 4. Serialization Check (Converted back to clean JSON) ---")
    print(validated_object.model_dump_json(indent=2))

except Exception as e:
    print(f"Parsing failed due to validation error: {e}")
    print("The LLM likely failed to adhere to the strict JSON schema provided.")


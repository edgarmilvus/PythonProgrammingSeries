
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

#!/usr/bin/env python3
# concept_explainer.py
# A command-line utility to generate tailored technical explanations using LLMChain.

import os
import sys
from typing import Dict, Any

# Ensure necessary LangChain components are available
try:
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    # We use the Chat model wrapper as it is optimized for instruction following
    from langchain_openai import ChatOpenAI
except ImportError:
    print("Error: Required libraries (langchain-openai, langchain) not found.")
    print("Please install them using: pip install langchain-openai langchain")
    sys.exit(1)

# --- Configuration Constants ---
MODEL_NAME = "gpt-3.5-turbo-0125" # A fast, capable model for instruction tasks
TEMPERATURE = 0.4 # Lower temperature for factual, less creative output

def setup_llm_chain() -> LLMChain:
    """
    Initializes the LLM and defines the core PromptTemplate, combining them
    into a functional LLMChain object ready for execution.
    """
    # 1. Defensive Environment Check: Mandatory API Key
    if "OPENAI_API_KEY" not in os.environ:
        print("FATAL ERROR: The OPENAI_API_KEY environment variable must be set.")
        sys.exit(1)

    # 2. Initialize the Model (LLM)
    # The temperature is set low to prioritize accuracy and adherence to the prompt structure.
    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    # 3. Define the Prompt Template (The Contract)
    # This multi-line template acts as the instruction set, defining the agent's persona
    # and forcing a specific, structured output format.
    template = """
    You are an expert technical communication specialist specializing in translating
    complex Python concepts into simple, relatable language for diverse audiences.

    --- ROLE AND INSTRUCTIONS ---
    1. Analyze the requested Concept and the Target Audience's assumed knowledge level.
    2. Generate a concise, tailored explanation using analogies appropriate for the audience.
    3. Immediately follow the explanation with a concrete, runnable Python code example.
    4. You MUST adhere strictly to the OUTPUT FORMAT specified below.

    --- INPUT VARIABLES ---
    Concept: {concept}
    Target Audience: {audience}

    --- OUTPUT FORMAT ---
    # Explanation for {audience}
    [Your tailored explanation here, maximum 3 paragraphs.]

    # Concrete Python Example
    
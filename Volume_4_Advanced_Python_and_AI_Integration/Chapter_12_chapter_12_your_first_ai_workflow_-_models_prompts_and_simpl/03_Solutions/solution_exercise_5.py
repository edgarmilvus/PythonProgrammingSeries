
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Configuration and Setup ---
if 'OPENAI_API_KEY' not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")

# Sample Feature List (The only variable supplied at runtime)
FEATURES = [
    "Implemented caching layer using Redis.",
    "Fixed critical bug where user sessions expired prematurely.",
    "Added dark mode support for the dashboard UI."
]
features_input = "\n".join([f"- {f}" for f in FEATURES])

# 1. Master Template
master_template = (
    "Generate release notes based on the following features list. "
    "The tone must be '{tone}' and the target audience is '{audience}'. "
    "Ensure the notes are compelling and accurate."
    "\n\n--- FEATURES ---\n{features_list}"
    "\n\n--- RELEASE NOTES ---"
)

master_prompt = PromptTemplate(
    input_variables=["features_list", "tone", "audience"],
    template=master_template
)

# 2. Partial Configuration

# Dev Environment Prompt: Informal and internal
dev_prompt = master_prompt.partial(
    tone="Informal and direct",
    audience="Internal Engineering Team"
)

# Production Environment Prompt: Professional and external
prod_prompt = master_prompt.partial(
    tone="Professional and marketing-focused",
    audience="End Users and Stakeholders"
)

# 3. Chain Creation
dev_chain = LLMChain(llm=llm, prompt=dev_prompt)
prod_chain = LLMChain(llm=llm, prompt=prod_prompt)

# --- Execution and Comparison ---

print("--- Running Development Release Notes Chain ---")
# Only 'features_list' needs to be supplied now
dev_response = dev_chain.invoke({"features_list": features_input})
print(dev_response['text'])

print("\n" + "=" * 60 + "\n")

print("--- Running Production Release Notes Chain ---")
prod_response = prod_chain.invoke({"features_list": features_input})
print(prod_response['text'])

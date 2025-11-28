
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

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Configuration and Setup ---

# Ensure OPENAI_API_KEY is set
if 'OPENAI_API_KEY' not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

# Initialize LLM
llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

# 1. Define Prompt Template with dynamic variables
template = (
    "You are an expert {role}. Your responses must be professional, "
    "detailed, and adhere strictly to the conventions and terminology of your field. "
    "Address the following query: {query}"
)

prompt = PromptTemplate(
    input_variables=["role", "query"],
    template=template
)

# 2. Create LLMChain
persona_chain = LLMChain(llm=llm, prompt=prompt)

# --- Test 1: Agile Scrum Master ---
role_1 = "Agile Scrum Master"
query_1 = "Explain the risks of technical debt in a two-week sprint cycle."
print(f"--- Test 1: Role: {role_1} ---")
print(f"Query: {query_1}\n")

response_1 = persona_chain.invoke({"role": role_1, "query": query_1})
print(response_1['text'])
print("-" * 50 + "\n")


# --- Test 2: 19th Century Romantic Poet ---
role_2 = "19th Century Romantic Poet"
query_2 = "Describe the feeling of debugging a complex asynchronous task."
print(f"--- Test 2: Role: {role_2} ---")
print(f"Query: {query_2}\n")

response_2 = persona_chain.invoke({"role": role_2, "query": query_2})
print(response_2['text'])
print("-" * 50)

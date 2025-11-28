
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Configuration and Setup ---
if 'OPENAI_API_KEY' not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")

# Example Input Data
ABSTRACT = """
The Python Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, 
preventing multiple native threads from executing Python bytecodes at once. This means 
that while Python is excellent for I/O-bound tasks where threads spend time waiting, 
it limits the effectiveness of multi-core processors for CPU-bound tasks. Developers 
often bypass the GIL using multiprocessing or by rewriting critical sections in C/C++ extensions.
"""
LANGUAGE = "German"
LENGTH = "two concise sentences"

# 1. Define Prompt Template with structured output requirements
template = (
    "You are a technical documentation specialist. Your task is to analyze the "
    "following technical abstract and provide a structured output. "
    "Failure to adhere to the requested length will result in an immediate termination of the task. "
    "\n\n--- INSTRUCTIONS ---"
    "\n1. Summarize the abstract into exactly {summary_length}."
    "\n2. Translate that summary into the target language: {target_language}."
    "\n3. Identify 5-7 key technical terms from the original abstract."
    "\n\n--- ABSTRACT ---"
    "\n{abstract_text}"
    "\n\n--- REQUIRED OUTPUT FORMAT ---"
    "\n\n## SECTION A: English Summary"
    "\n[Insert English Summary Here]"
    "\n\n## SECTION B: Translated Summary ({target_language})"
    "\n[Insert Translated Summary Here]"
    "\n\n## SECTION C: Key Technical Terms"
    "\n* [Term 1]"
    "\n* [Term 2]"
    "\n* ..."
)

prompt = PromptTemplate(
    input_variables=["abstract_text", "target_language", "summary_length"],
    template=template
)

# 2. Create LLMChain
summarizer_chain = LLMChain(llm=llm, prompt=prompt)

# 3. Execution and Output
print(f"--- Running Multilingual Summarizer (Target: {LANGUAGE}, Length: {LENGTH}) ---")

inputs = {
    "abstract_text": ABSTRACT,
    "target_language": LANGUAGE,
    "summary_length": LENGTH
}

response = summarizer_chain.invoke(inputs)

print("\n" + response['text'])

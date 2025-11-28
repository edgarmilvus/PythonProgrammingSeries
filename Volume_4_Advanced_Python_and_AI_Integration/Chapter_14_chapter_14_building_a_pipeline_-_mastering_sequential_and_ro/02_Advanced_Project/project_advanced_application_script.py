
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

import os
from langchain.chains import SequentialChain, LLMChain, MultiPromptChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, Route
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

# --- Configuration and Initialization ---
# NOTE: Replace with actual key handling in production environments
# For this example, we assume OPENAI_API_KEY is set in the environment.
try:
    llm = ChatOpenAI(temperature=0.4, model="gpt-3.5-turbo")
except Exception as e:
    print(f"Error initializing LLM: {e}. Ensure API key is set.")
    llm = None # Placeholder for execution environment where key might be missing

if llm:
    # --- Stage 1: Initial Analysis Chain (Sequential) ---
    # This chain analyzes the input topic and extracts key variables for the router.

    # 1. Audience Identification Template
    audience_template = """
    Analyze the following topic: '{topic}'. 
    Identify the single most appropriate primary target audience (e.g., 'Technical Developers', 'Executive Leadership', 'Marketing Professionals'). 
    Output ONLY the audience name.
    """
    prompt_audience = PromptTemplate(input_variables=["topic"], template=audience_template)
    chain_audience = LLMChain(llm=llm, prompt=prompt_audience, output_key="audience")

    # 2. Tone Suggestion Template
    tone_template = """
    Given the topic: '{topic}' and the identified audience: '{audience}', 
    suggest the best content tone for a successful strategy. 
    Choose strictly one of the following categories: 'TECHNICAL', 'EXECUTIVE', or 'MARKETING'.
    Output ONLY the chosen category word in uppercase.
    """
    prompt_tone = PromptTemplate(input_variables=["topic", "audience"], template=tone_template)
    chain_tone = LLMChain(llm=llm, prompt=prompt_tone, output_key="tone_category")

    # Combine the two analysis chains into a SequentialChain
    analysis_chain = SequentialChain(
        chains=[chain_audience, chain_tone],
        input_variables=["topic"],
        output_variables=["audience", "tone_category"],
        verbose=False
    )

    # --- Stage 2: Dynamic Strategy Generation (Router/MultiPromptChain) ---
    
    # Define specialized destination chains based on the tone_category output.

    # 1. Technical Strategy Chain
    technical_template = """
    You are a Senior Technical Architect. Generate a detailed, code-focused content strategy 
    for the topic: {topic}. The target audience is {audience}. 
    Focus on implementation details, best practices, and performance benchmarks.
    """
    technical_prompt = PromptTemplate(template=technical_template, input_variables=["topic", "audience"])
    technical_chain = LLMChain(llm=llm, prompt=technical_prompt)

    # 2. Executive Strategy Chain
    executive_template = """
    You are a Strategic Advisor. Generate a high-level executive briefing (max 5 bullet points) 
    on the topic: {topic}. The target audience is {audience}. 
    Focus on ROI, risk assessment, and strategic alignment.
    """
    executive_prompt = PromptTemplate(template=executive_template, input_variables=["topic", "audience"])
    executive_chain = LLMChain(llm=llm, prompt=executive_prompt)

    # 3. Marketing Strategy Chain
    marketing_template = """
    You are a Growth Marketer. Generate a compelling headline and three core selling points 
    for content about the topic: {topic}. The target audience is {audience}. 
    Focus on pain points and value propositions.
    """
    marketing_prompt = PromptTemplate(template=marketing_template, input_variables=["topic", "audience"])
    marketing_chain = LLMChain(llm=llm, prompt=marketing_prompt)

    # Define the destination chain dictionary for the MultiPromptChain
    destination_chains = {
        "TECHNICAL": technical_chain,
        "EXECUTIVE": executive_chain,
        "MARKETING": marketing_chain,
    }

    # Define the router chain (The MultiPromptChain uses an internal LLMRouterChain)
    # The router uses the 'tone_category' output from the analysis chain to decide the route.
    router_chain = MultiPromptChain(
        router_chain=LLMRouterChain.from_llm(llm, destination_chains.keys()),
        destination_chains=destination_chains,
        default_chain=technical_chain, # Fallback if routing fails
        verbose=False
    )

    # --- Stage 3: The Master Pipeline (Orchestration) ---

    # The final SequentialChain links the Analysis output to the Router input.
    # Note: The router chain expects 'input' (the topic) but also needs 'audience'
    # which is passed through the SequentialChain's memory/context.
    master_pipeline = SequentialChain(
        chains=[analysis_chain, router_chain],
        input_variables=["topic"],
        # The final output is the result of the routed chain execution
        output_variables=["output"], 
        verbose=True 
    )

    # --- Execution ---
    input_topic = "Implementing large-scale serverless functions using Python and AWS Lambda"
    print(f"--- Running Strategy Pipeline for Topic: {input_topic} ---\n")
    
    # The SequentialChain manages the flow: 
    # topic -> analysis_chain (outputs audience, tone_category) -> router_chain (uses tone_category to route)
    result = master_pipeline.invoke({"topic": input_topic})

    print("\n--- Pipeline Execution Summary ---")
    print(f"Identified Audience: {result.get('audience', 'N/A')}")
    print(f"Determined Tone: {result.get('tone_category', 'N/A')}")
    print(f"\nFINAL CONTENT STRATEGY:\n{result['output']}")


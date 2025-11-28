
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
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import (
    LLMChain,
    SimpleSequentialChain,
    SequentialChain,
    MultiPromptChain
)
from langchain.chains.router.multi_prompt_init import get_multi_prompt_chain

# --- Configuration ---
# Ensure OPENAI_API_KEY is set in your environment variables
try:
    llm = ChatOpenAI(temperature=0.1) 
except Exception as e:
    print(f"Warning: LLM initialization failed. Ensure API key is set. Error: {e}")
    # Placeholder for execution environment where API key might be missing
    llm = None 


## Exercise 1: The Technical Content Summarizer and Tagger

def create_summarizer_tagger_chain(llm):
    """
    Implements a SimpleSequentialChain to summarize text and then extract tags.
    """
    if not llm:
        raise ValueError("LLM is not initialized.")

    # Chain 1: Summarizer
    summarizer_template = """
    You are an expert technical writer. Summarize the following text into 
    exactly three concise sentences.
    TEXT: {long_text}
    SUMMARY:
    """
    summarizer_prompt = PromptTemplate(input_variables=["long_text"], template=summarizer_template)
    # Output key must be the input key of the next chain ('summary')
    summarizer_chain = LLMChain(llm=llm, prompt=summarizer_prompt, output_key="summary")

    # Chain 2: Tagger
    tagger_template = """
    Based on the summary provided below, extract exactly 5 crucial technical terms 
    or concepts. Output them only as a comma-separated list, nothing else.
    SUMMARY: {summary}
    TAGS:
    """
    tagger_prompt = PromptTemplate(input_variables=["summary"], template=tagger_template)
    tagger_chain = LLMChain(llm=llm, prompt=tagger_prompt, output_key="tags")

    # SimpleSequentialChain setup (automatically maps the single output to the next single input)
    pipeline = SimpleSequentialChain(
        chains=[summarizer_chain, tagger_chain],
        verbose=True
    )
    return pipeline

# Example Input for Exercise 1
tech_article = (
    "Asynchronous programming in Python, centered around the asyncio library, "
    "relies heavily on the event loop. The event loop manages and schedules "
    "concurrent tasks, which are typically defined using the 'async def' syntax "
    "for coroutines. When a coroutine encounters an 'await' expression, it yields "
    "control back to the event loop, allowing other tasks to run. This non-blocking "
    "I/O model is fundamentally different from traditional multi-threading. "
    "Futures and Awaitables represent the eventual result of an asynchronous operation, "
    "acting as the low-level mechanism for managing state transitions in concurrent code."
)

if llm:
    print("--- Exercise 1: Simple Sequential Chain Results ---")
    summarizer_tagger_pipeline = create_summarizer_tagger_chain(llm)
    result_1 = summarizer_tagger_pipeline.run(tech_article)
    print(f"\nFinal Tags (Raw Output from Tagger Chain):\n{result_1}")
    print("-" * 50)


## Exercise 2: Structured Product Review Analysis Pipeline

def create_review_analysis_chain(llm):
    """
    Implements a robust SequentialChain managing multiple input and output variables.
    """
    if not llm:
        raise ValueError("LLM is not initialized.")

    # Chain 1: Sentiment Analyzer
    sentiment_template = """
    Analyze the following review for the product: {product_name}. 
    Determine the overall sentiment. Respond with ONLY one word: 'Positive' or 'Negative'.
    REVIEW: {review_text}
    """
    sentiment_prompt = PromptTemplate(input_variables=["review_text", "product_name"], template=sentiment_template)
    sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt, output_key="sentiment")

    # Chain 2: Contextual Critic (Requires review_text, product_name, and sentiment)
    critic_template = """
    Product: {product_name}. Sentiment: {sentiment}. Review: {review_text}.
    Based on the review and sentiment, provide a single, actionable suggestion. 
    If Positive, suggest a marketing angle. If Negative, suggest a specific development fix.
    """
    critic_prompt = PromptTemplate(input_variables=["review_text", "product_name", "sentiment"], template=critic_template)
    critic_chain = LLMChain(llm=llm, prompt=critic_prompt, output_key="actionable_suggestion")

    # Chain 3: Formatter (Requires product_name, sentiment, and actionable_suggestion)
    formatter_template = """
    You are a JSON formatting expert. Take the following data and structure it into a single JSON object.
    Include the fields: product, overall_sentiment, and recommendation.
    Product Name: {product_name}
    Sentiment: {sentiment}
    Suggestion: {actionable_suggestion}
    """
    formatter_prompt = PromptTemplate(input_variables=["product_name", "sentiment", "actionable_suggestion"], template=formatter_template)
    formatter_chain = LLMChain(llm=llm, prompt=formatter_prompt, output_key="final_json_report")

    # SequentialChain setup
    pipeline = SequentialChain(
        chains=[sentiment_chain, critic_chain, formatter_chain],
        input_variables=["product_name", "review_text"],
        output_variables=["sentiment", "actionable_suggestion", "final_json_report"],
        verbose=True
    )
    return pipeline

# Example Input for Exercise 2
review_input = {
    "product_name": "QuantuMage Python Toolkit v3.1",
    "review_text": "The new asynchronous logging feature is incredibly fast, but the documentation for setting up the custom middleware was confusing and led to several deployment crashes."
}

if llm:
    print("\n--- Exercise 2: Robust Sequential Chain Results ---")
    review_analysis_pipeline = create_review_analysis_chain(llm)
    result_2 = review_analysis_pipeline(review_input)
    
    print(f"\nPipeline Inputs: {review_analysis_pipeline.input_variables}")
    print(f"Pipeline Outputs: {review_analysis_pipeline.output_variables}")
    print(f"\nSentiment: {result_2['sentiment']}")
    print(f"Suggestion: {result_2['actionable_suggestion']}")
    print(f"Final Report:\n{result_2['final_json_report']}")
    print("-" * 50)


## Exercise 3: Dynamic Customer Support Router

def create_destination_chains(llm):
    """Defines the three specialized destination chains for the router."""
    # Billing Chain
    billing_template = "You are a specialized billing support agent. Respond to the user's query about payments or subscriptions: {input}"
    billing_chain = LLMChain(llm=llm, prompt=PromptTemplate(template=billing_template, input_variables=["input"]))

    # Technical Chain
    tech_template = "You are a specialized technical support engineer. Provide detailed, step-by-step diagnostic advice for this bug report: {input}"
    tech_chain = LLMChain(llm=llm, prompt=PromptTemplate(template=tech_template, input_variables=["input"]))

    # General Chain
    general_template = "You are a friendly general Q&A assistant. Answer the user's question conversationally: {input}"
    general_chain = LLMChain(llm=llm, prompt=PromptTemplate(template=general_template, input_variables=["input"]))

    # Dictionary format required by get_multi_prompt_chain
    return [
        {"name": "billing", "description": "Good for questions about subscriptions, payments, refunds, and account cancellation.", "chain": billing_chain},
        {"name": "technical", "description": "Good for questions about code errors, bugs, API keys, and version compatibility issues.", "chain": tech_chain},
        {"name": "general", "description": "Good for simple greetings, company information, or general conversational topics.", "chain": general_chain}
    ]

def create_support_router(llm):
    """
    Constructs the MultiPromptChain using the specialized destination chains.
    """
    if not llm:
        raise ValueError("LLM is not initialized.")
        
    destination_info = create_destination_chains(llm)
    
    # Prepare the input structure for get_multi_prompt_chain
    destination_prompts = [
        {"name": d["name"], "description": d["description"], "prompt_template": d["chain"].prompt.template}
        for d in destination_info
    ]
    
    # Map names to chains for the router
    destination_chains_map = {d["name"]: d["chain"] for d in destination_info}

    # Use the helper function to build the full router chain structure
    full_router_chain = get_multi_prompt_chain(
        llm=llm, 
        destination_prompts=destination_prompts, 
        default_chain=destination_chains_map["general"], # Fallback chain
        verbose=True
    )
    return full_router_chain

if llm:
    print("\n--- Exercise 3: Dynamic Customer Support Router Results ---")
    router_chain_3 = create_support_router(llm)
    
    # Test A: Billing Query
    query_a = "I need to know how to cancel my recurring subscription and request a refund."
    print(f"\nQuery A (Billing):\nInput: {query_a}")
    print(f"Response: {router_chain_3.run(query_a)}\n")
    
    # Test B: Technical Query
    query_b = "My API key suddenly stopped working after I updated to Python 3.12. What logs should I check?"
    print(f"Query B (Technical):\nInput: {query_b}")
    print(f"Response: {router_chain_3.run(query_b)}\n")
    
    # Test C: General Query
    query_c = "What is the mission statement of your company?"
    print(f"Query C (General):\nInput: {query_c}")
    print(f"Response: {router_chain_3.run(query_c)}\n")
    print("-" * 50)


## Exercise 4: Interactive Challenge - Integrating Routing into a RAG Pipeline

def create_expert_rag_chain(llm):
    """
    Simulated Expert RAG Chain (Sequential Chain). 
    Input must be 'input', output must be 'text' for MultiPromptChain compatibility.
    """
    # Step 1: Simulated Retrieval (Generates context from the query)
    retrieval_template = "Based on the user query: '{input}', generate detailed technical context (4 sentences) that would be retrieved from a database."
    retrieval_prompt = PromptTemplate(input_variables=["input"], template=retrieval_template)
    retrieval_chain = LLMChain(llm=llm, prompt=retrieval_prompt, output_key="context")

    # Step 2: Synthesis (Answers using the context and original query)
    synthesis_template = "Using the following context, answer the user query: '{input}'. CONTEXT: {context}"
    synthesis_prompt = PromptTemplate(input_variables=["input", "context"], template=synthesis_template)
    # Output key must be 'text' for MultiPromptChain compatibility
    synthesis_chain = LLMChain(llm=llm, prompt=synthesis_prompt, output_key="text") 

    # Sequential RAG Pipeline
    expert_rag_chain = SequentialChain(
        chains=[retrieval_chain, synthesis_chain],
        input_variables=["input"], # Must be 'input' for router
        output_variables=["text"], # Must be 'text' for router
        verbose=False,
    )
    return expert_rag_chain

def create_integrated_router_system(llm):
    """
    Builds the MultiPromptChain routing between the RAG pipeline and a Chat bypass.
    """
    if not llm:
        raise ValueError("LLM is not initialized.")
        
    # 1. Define Destinations
    rag_pipeline = create_expert_rag_chain(llm)
    
    # Conversational Bypass Chain (ChatChain)
    chat_template = "You are a friendly assistant. Answer the user's question conversationally: {input}"
    chat_chain = LLMChain(llm=llm, prompt=PromptTemplate(template=chat_template, input_variables=["input"]))
    
    # 2. Structure Destinations for MultiPromptChain
    destination_prompts = [
        {
            "name": "ExpertRAGChain", 
            "description": "Handles complex, technical, or knowledge-intensive questions requiring context retrieval.", 
            "prompt_template": rag_pipeline.chains[0].prompt.template # Use retrieval prompt template for description
        },
        {
            "name": "ChatChain", 
            "description": "Handles simple greetings, jokes, or purely conversational small talk that does not require external knowledge.", 
            "prompt_template": chat_chain.prompt.template
        }
    ]
    
    # 3. Define the Chain Map
    destination_chains_map = {
        "ExpertRAGChain": rag_pipeline,
        "ChatChain": chat_chain
    }
    
    # 4. Build the final MultiPromptChain
    integrated_router = MultiPromptChain.from_prompts(
        llm=llm,
        chain_names=["ExpertRAGChain", "ChatChain"],
        destination_prompts=destination_prompts,
        default_chain=chat_chain,
        verbose=True
    )
    
    return integrated_router

if llm:
    print("\n--- Exercise 4: Integrated Router (RAG Bypass) Results ---")
    router_chain_4 = create_integrated_router_system(llm)

    # Test 1: Knowledge Query (Should route to RAG)
    query_1 = "Explain the role of futures and awaitables in asynchronous Python programming."
    print(f"\nTest 1 (Knowledge Query):\nInput: {query_1}")
    print(f"Response: {router_chain_4.run(query_1)}\n")

    # Test 2: Conversational Query (Should route to Bypass)
    query_2 = "Tell me a fun fact about the number 42."
    print(f"Test 2 (Bypass Query):\nInput: {query_2}")
    print(f"Response: {router_chain_4.run(query_2)}\n")
    print("-" * 50)

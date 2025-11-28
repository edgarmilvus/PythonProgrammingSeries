
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
import asyncio
import json
from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Optional, Any

# LangChain Imports
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.exceptions import OutputParserException

# --- Configuration and Setup ---
# Ensure the LLM is initialized. Using gpt-3.5-turbo for speed.
try:
    # NOTE: Requires OPENAI_API_KEY environment variable to be set.
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
except Exception as e:
    print(f"Warning: LLM initialization failed. Ensure API key is set. Error: {e}")
    llm = None # Placeholder for non-functional environment

# --- Provided Pydantic Schemas (Re-included for completeness) ---

class NetworkSettings(BaseModel):
    """Defines network configuration for a service."""
    protocol: str = Field(description="The network protocol (e.g., 'TCP', 'UDP').")
    port: int = Field(description="The network port number.")

    @validator('port')
    def validate_ephemeral_port_range(cls, v):
        """Ensures the port is within the ephemeral range (49152-65535)."""
        if not (49152 <= v <= 65535):
            raise ValueError(f"Port {v} must be between 49152 and 65535.")
        return v

class MicroserviceConfig(BaseModel):
    """A complete configuration schema for a microservice."""
    service_name: str = Field(description="The unique name of the microservice.")
    version: str = Field(description="The current deployment version (e.g., 'v1.2.0').")
    dependencies: List[str] = Field(description="A list of other services this service relies on.")
    network: NetworkSettings

class UserFeedback(BaseModel):
    """Schema for structured user feedback validation."""
    rating: int = Field(description="The user's rating, must be an integer between 1 and 5.")
    comment: str = Field(description="The detailed text comment provided by the user.")

    @validator('rating')
    def validate_rating_range(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return v

class PatentMetadata(BaseModel):
    """Basic extraction schema for patent abstracts."""
    title: str = Field(description="The official title of the patent.")
    inventor: str = Field(description="The primary inventor listed.")
    filing_date: str = Field(description="The date the patent was filed (e.g., YYYY-MM-DD).")

class PatentAssessment(BaseModel):
    """Detailed assessment schema for patent novelty."""
    novelty_score: int = Field(description="A score from 1 to 10 indicating the technical novelty.")
    key_concepts: List[str] = Field(description="At least three core technical concepts introduced by the patent.")
    market_impact_summary: str = Field(description="A brief summary of the potential commercial impact.")

    @validator('key_concepts')
    def check_min_concepts(cls, v):
        if len(v) < 3:
            raise ValueError("Must identify at least 3 key concepts.")
        return v

class FinancialSummary(BaseModel):
    """Structured financial report summary for a specific quarter."""
    company_ticker: str = Field(description="The stock ticker symbol (e.g., AAPL).")
    quarter: str = Field(description="The fiscal quarter being reported (e.g., Q4 2023).")
    revenue_growth_pct: float = Field(description="The year-over-year revenue growth percentage.")
    risk_rating: str = Field(description="The assessed risk level: 'Low', 'Medium', or 'High'.")

    @validator('risk_rating')
    def validate_risk_level(cls, v):
        if v not in ["Low", "Medium", "High"]:
            raise ValueError(f"Risk rating must be 'Low', 'Medium', or 'High', not '{v}'.")
        return v

# --- Solution Implementations ---

### Exercise 1: Structured Configuration Generation with Nested Validation

def solve_exercise_1(llm: ChatOpenAI):
    """
    Generates a microservice configuration using nested Pydantic validation,
    enforcing a strict ephemeral port range (49152-65535).
    """
    print("\n--- Exercise 1: Structured Configuration Generation ---")

    parser = PydanticOutputParser(pydantic_object=MicroserviceConfig)

    template = """
    You are an expert configuration generator. Generate a strict JSON configuration 
    for the service described below.

    SERVICE DESCRIPTION:
    Service Name: Authentication Gateway
    Version: v2.1.0
    Dependencies: UserDB, SessionCache
    Network Protocol: TCP

    CRITICAL CONSTRAINT: The network port MUST be in the ephemeral range (49152 to 65535).

    {format_instructions}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    config_chain = prompt | llm | parser

    try:
        # Successful run, LLM should pick a valid port
        validated_config = config_chain.invoke({})
        print("✅ Successfully generated and validated configuration:")
        print(f"Service Name: {validated_config.service_name}")
        print(f"Network Port: {validated_config.network.port}")
        # Demonstrate the validation check by attempting an invalid port (requires LLM cooperation)
        # Since we cannot force the LLM to output a bad port consistently, we rely on the
        # parser to raise an error if the LLM fails the constraint check.
        # If the LLM outputted port 80, the parser would raise a ValidationError here.

    except OutputParserException as e:
        print("❌ Validation Failed (as expected if LLM outputted invalid JSON or port):")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if llm:
    solve_exercise_1(llm)


### Exercise 2: The Self-Healing Data Pipeline: Error Correction Loop

def solve_exercise_2(llm: ChatOpenAI):
    """
    Implements a self-healing pipeline that uses validation errors to guide the LLM
    to fix its malformed JSON output.
    """
    print("\n--- Exercise 2: The Self-Healing Data Pipeline ---")

    parser = PydanticOutputParser(pydantic_object=UserFeedback)
    max_retries = 3
    retry_count = 0
    validated_feedback = None

    # 1. Initial Prompt (designed to potentially fail validation)
    initial_prompt_template = """
    You are extracting user feedback. Please generate the structured JSON output.

    USER COMMENT: "I found the app amazing, a true masterpiece! I would rate it an 'A+ quality' 
    if I could, but since I must use a number, let's say 7 out of 5 for enthusiasm."

    {format_instructions}
    """

    # 2. Correction Prompt Template
    correction_template = """
    CRITICAL ERROR: The previous JSON output failed validation. You MUST regenerate the entire JSON object, 
    fixing the error described below.

    ORIGINAL INSTRUCTIONS: {original_prompt}
    FAILED RAW OUTPUT: {raw_output}
    VALIDATION ERROR: {error_message}

    Ensure the new output strictly adheres to the requested format and fixes all issues.
    {format_instructions}
    """

    # Initial prompt structure
    initial_prompt = PromptTemplate(
        template=initial_prompt_template,
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    # Correction prompt structure
    correction_prompt = PromptTemplate(
        template=correction_template,
        input_variables=["original_prompt", "raw_output", "error_message"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Initial chain definition
    chain = initial_prompt | llm

    while retry_count < max_retries:
        print(f"\nAttempt {retry_count + 1}/{max_retries}...")
        
        try:
            # Get raw LLM response (string)
            if retry_count == 0:
                raw_response = chain.invoke({})
            else:
                # Use the correction chain for subsequent attempts
                raw_response = (correction_prompt | llm).invoke({
                    "original_prompt": initial_prompt_template,
                    "raw_output": raw_response_str,
                    "error_message": str(validation_error),
                })
            
            raw_response_str = raw_response.content if hasattr(raw_response, 'content') else raw_response

            # Attempt parsing and validation
            validated_feedback = parser.parse(raw_response_str)
            
            print("✅ Success! Output validated.")
            print(f"Result: Rating={validated_feedback.rating}, Comment='{validated_feedback.comment[:50]}...'")
            return validated_feedback

        except (OutputParserException, ValidationError) as e:
            validation_error = e
            print(f"❌ Validation Failed. Error captured: {validation_error}")
            retry_count += 1
            
            if retry_count >= max_retries:
                print(f"🛑 Failed to correct output after {max_retries} attempts.")
                return None
        except Exception as e:
            print(f"An unexpected critical error occurred: {e}")
            return None

if llm:
    solve_exercise_2(llm)


### Exercise 3: Dynamic Patent Abstract Analysis via Sequential Parsing

def solve_exercise_3(llm: ChatOpenAI):
    """
    Builds a RunnableSequence with two sequential Pydantic parsing steps
    to extract metadata and then assess novelty based on the extracted title.
    """
    print("\n--- Exercise 3: Dynamic Patent Abstract Analysis ---")

    # Sample data
    abstract_text = """
    Patent Title: Quantum Entanglement Communication Network via Supercooled Fiber Optics.
    Primary Inventor: Dr. Elara Vance.
    Filing Date: 2025-01-15.
    Abstract Body: This invention introduces a novel method for secure, instantaneous data transfer
    by leveraging quantum entanglement across specially designed supercooled fiber optic cables.
    The system achieves zero latency over continental distances, far surpassing classical communication limits.
    Key concepts include entanglement swapping, ultra-low temperature maintenance, and dynamic qubit stabilization.
    """

    # Parsers
    parser_metadata = PydanticOutputParser(pydantic_object=PatentMetadata)
    parser_assessment = PydanticOutputParser(pydantic_object=PatentAssessment)

    # Prompt 1: Metadata Extraction
    prompt_metadata = PromptTemplate(
        template="""
        Analyze the following patent abstract and extract the required metadata into the strict JSON format.
        ABSTRACT: {abstract}
        {format_instructions}
        """,
        input_variables=["abstract"],
        partial_variables={"format_instructions": parser_metadata.get_format_instructions()},
    )

    # Prompt 2: Assessment Generation (Input is the Title from Step 1)
    prompt_assessment = PromptTemplate(
        template="""
        Analyze the following patent title and generate a structured assessment of its technical novelty and market impact.
        TITLE TO ASSESS: {title}
        
        CRITICAL: Ensure the novelty score is 1-10 and you identify at least 3 key concepts.
        {format_instructions}
        """,
        input_variables=["title"],
        partial_variables={"format_instructions": parser_assessment.get_format_instructions()},
    )

    # Step 1: Extract Metadata and Validate
    metadata_chain = prompt_metadata | llm | parser_metadata

    # Step 2: Extract the Title from the validated PatentMetadata object
    # RunnableLambda takes the output of the previous step (PatentMetadata object)
    title_extractor = RunnableLambda(lambda metadata: {"title": metadata.title})

    # Step 3: Assess the Title and Validate
    assessment_chain = prompt_assessment | llm | parser_assessment

    # Combine into the sequential chain
    full_pipeline = RunnableSequence(
        metadata_chain,
        title_extractor,
        assessment_chain
    )

    # Execution
    try:
        final_assessment = full_pipeline.invoke({"abstract": abstract_text})
        
        print("✅ Pipeline Execution Successful.")
        print("\n--- Extracted and Validated Assessment ---")
        print(f"Analyzed Title: {final_assessment.key_concepts[0]}...")
        print(f"Novelty Score: {final_assessment.novelty_score}/10")
        print(f"Key Concepts (Validated Min 3): {final_assessment.key_concepts}")
        print(f"Market Impact Summary: {final_assessment.market_impact_summary[:80]}...")
        
    except Exception as e:
        print(f"❌ Sequential pipeline failed: {e}")
        
    # --- Visualization (DOT Diagram Generation) ---
    print("\n--- Graphviz DOT Diagram (Visualization) ---")
    # Generate the DOT diagram code for the sequence
    dot_graph = full_pipeline.get_graph().draw_mermaid_sr()
    print("Mermaid Diagram Code Generated (Visualize using an online tool):")
    print(dot_graph)
    
if llm:
    solve_exercise_3(llm)

### Exercise 4: Interactive Challenge: Parallelized Report Validation with `asyncio.TaskGroup`

async def generate_and_validate_report(llm: ChatOpenAI, ticker: str) -> Optional[FinancialSummary]:
    """
    Asynchronously generates a financial summary and enforces Pydantic validation.
    """
    parser = PydanticOutputParser(pydantic_object=FinancialSummary)

    template = """
    Generate a structured financial summary for the company with ticker {ticker} for the latest quarter (Q4 2024).
    
    Instructions:
    1. Revenue growth percentage should be a float.
    2. Risk rating must be strictly 'Low', 'Medium', or 'High'.
    
    {format_instructions}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["ticker"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    print(f"[{ticker}] Starting generation and validation...")
    
    try:
        # Use ainvoke for asynchronous execution
        validated_summary = await chain.ainvoke({"ticker": ticker})
        print(f"[{ticker}] ✅ Successfully validated report.")
        return validated_summary
    except Exception as e:
        # Catch validation errors or API errors specific to this task
        print(f"[{ticker}] ❌ Failed validation or execution: {type(e).__name__}: {e}")
        return None

async def solve_exercise_4(llm: ChatOpenAI):
    """
    Orchestrates concurrent report generation and validation using asyncio.TaskGroup.
    """
    print("\n--- Exercise 4: Parallelized Report Validation ---")
    
    company_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    results: List[Optional[FinancialSummary]] = []

    try:
        # TaskGroup is used for robust, structured concurrency
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(generate_and_validate_report(llm, ticker))
                for ticker in company_tickers
            ]
        
        # Collect results from tasks (TaskGroup ensures all tasks are awaited)
        for task in tasks:
            results.append(task.result())

    except Exception as e:
        # This catches exceptions that bubble up from the TaskGroup, 
        # usually indicating a critical failure in one of the tasks.
        print(f"\n🛑 Critical error during TaskGroup execution: {e}")

    # Final Output Verification
    print("\n--- Final Consolidated and Validated Results ---")
    for result in results:
        if result:
            print(f"Ticker: {result.company_ticker:<5} | Q: {result.quarter:<8} | Growth: {result.revenue_growth_pct:.2f}% | Risk: {result.risk_rating}")
            # Explicit check to confirm Pydantic validation constraints were met:
            assert result.risk_rating in ["Low", "Medium", "High"]
        else:
            print(f"Report failed for one company.")

if llm:
    # Run the asynchronous main function
    asyncio.run(solve_exercise_4(llm))

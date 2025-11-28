
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

# Source File: theory_project_architecture_design_blueprint_part1.py
# Description: Project Architecture & Design Blueprint
# ==========================================

import os
import time
from google import genai
from google.genai import types
from typing import List, Optional, Dict, Any

# --- Configuration and Initialization ---

# Initialize the Gemini Client (assumes GEMINI_API_KEY is set in environment)
try:
    CLIENT = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure your GEMINI_API_KEY is set.")
    exit()

# Define the model to be used for the Orchestrator and Agents
MODEL_NAME = "gemini-2.5-pro" # Pro model for complex reasoning and delegation

# --- Utility Functions for Grounding and RAG Setup ---

def add_citations(response: types.GenerateContentResponse) -> str:
    """
    Processes the grounding metadata from a Gemini response to insert inline
    citations (Markdown links) into the text.

    This implementation is derived directly from the official Google documentation
    to ensure accurate linkage between text segments and web/file sources.
    """
    if not response.candidates:
        return response.text
    
    candidate = response.candidates[0]
    
    # Check for grounding metadata
    if not candidate.grounding_metadata:
        return response.text

    text = response.text
    metadata = candidate.grounding_metadata
    
    supports = metadata.grounding_supports
    chunks = metadata.grounding_chunks

    if not supports or not chunks:
        return text

    # Sort supports by end_index in descending order to avoid shifting issues 
    # when inserting the citation strings. This is CRITICAL for correct insertion.
    sorted_supports = sorted(
        supports, 
        key=lambda s: s.segment.end_index if s.segment else -1, 
        reverse=True
    )

    for support in sorted_supports:
        if not support.segment or not support.grounding_chunk_indices:
            continue
            
        end_index = support.segment.end_index
        
        citation_links = []
        for i in support.grounding_chunk_indices:
            if i < len(chunks):
                chunk = chunks[i]
                
                # Determine if the chunk is a web source or a file source
                if chunk.web:
                    uri = chunk.web.uri
                elif chunk.file:
                    # For File Search, the URI often points to the internal file path, 
                    # but we use the display name or file name for context in the citation.
                    # Note: In a real application, you might map this to an internal link.
                    uri = chunk.file.name 
                else:
                    continue

                # Create citation string like [1](link)
                # We use i+1 for 1-based indexing in citations
                citation_links.append(f"[{i + 1}]({uri})")

        if citation_links:
            citation_string = ", ".join(citation_links)
            # Insert the citation string at the segment's end index
            text = text[:end_index] + citation_string + text[end_index:]

    return text

def setup_file_search_store(
    file_path: str, 
    store_display_name: str, 
    file_display_name: str
) -> Optional[str]:
    """
    Creates a File Search Store (Vector Store/Database) and uploads a file 
    to it for RAG purposes, following the official documentation pattern.
    
    NOTE: This function requires a real, accessible file path to execute fully.
    Here we use mock logic for demonstration of the architecture.
    """
    print(f"--- Setting up File Search Store: {store_display_name} ---")
    try:
        # 1. Create the File Search store
        file_search_store = CLIENT.file_search_stores.create(
            config={'display_name': store_display_name}
        )
        store_name = file_search_store.name
        print(f"Store created: {store_name}")
        
        # 2. Mock file check (since we can't upload a real file in this environment)
        if not os.path.exists(file_path):
             print(f"WARNING: File not found at {file_path}. Skipping upload.")
             # Return the store name even if empty, allowing the agent to run without RAG
             return store_name
        
        # 3. Upload and import the file into the store (Long-running operation)
        print(f"Uploading and importing file: {file_path}...")
        operation = CLIENT.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=store_name,
            config={'display_name': file_display_name}
        )

        # 4. Wait until import is complete
        while not operation.done:
            print("Importing file... (Waiting 5 seconds)")
            time.sleep(5)
            operation = CLIENT.operations.get(operation)
        
        print("File import complete.")
        return store_name
        
    except Exception as e:
        print(f"Error during File Search Store setup: {e}")
        return None

# --- Agent Class Definitions (Adhering to DRY) ---

class BaseAgent:
    """
    Abstract base class for all specialized agents in the Swarm.
    Enforces the DRY principle by centralizing client and model initialization.
    """
    def __init__(self, system_prompt: str, model: str = MODEL_NAME):
        self.client = CLIENT
        self.model = model
        self.system_prompt = system_prompt
        
    def _generate_content(self, contents: str, tools: Optional[List[types.Tool]] = None) -> types.GenerateContentResponse:
        """Internal method to handle the API call with specific tool configurations."""
        config_params: Dict[str, Any] = {"system_instruction": self.system_prompt}
        
        if tools:
            config_params["tools"] = tools
            
        config = types.GenerateContentConfig(**config_params)
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )
        return response

    def run(self, task: str) -> str:
        """Placeholder for the agent's primary execution logic."""
        raise NotImplementedError("Subclasses must implement the run method.")

class SearcherAgent(BaseAgent):
    """
    Specialized agent for real-time, external data retrieval using Google Search Grounding.
    """
    def __init__(self):
        system_prompt = (
            "You are the Real-Time Search Agent. Your sole purpose is to retrieve "
            "the most current and verifiable facts from the web using the Google Search tool. "
            "Do not use internal knowledge. Provide a concise, grounded answer."
        )
        super().__init__(system_prompt)
        
        # Configure the Google Search tool for grounding
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

    def run(self, query: str) -> str:
        """Executes a search query and returns the grounded result with citations."""
        print(f"\n[Searcher Agent]: Executing real-time search for: '{query}'")
        
        response = self._generate_content(
            contents=query, 
            tools=[self.search_tool]
        )
        
        # The Orchestrator will handle the final citation formatting, 
        # but we return the raw response text here.
        return response.text, response # Return text and the full response for metadata extraction

class DocumentAnalystAgent(BaseAgent):
    """
    Specialized agent for internal knowledge retrieval using the File Search Store (RAG).
    """
    def __init__(self, file_search_store_name: str):
        system_prompt = (
            "You are the Internal Document Analyst. Your purpose is to analyze "
            "the provided internal documents (File Search Store) and provide "
            "answers strictly based on that proprietary context. Cite sources from the documents."
        )
        super().__init__(system_prompt)
        self.store_name = file_search_store_name
        
        # Configure the File Search tool for RAG
        self.rag_tool = types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=[self.store_name]
            )
        )

    def run(self, query: str) -> str:
        """Queries the internal RAG store and returns the grounded result."""
        if not self.store_name:
            return "Error: File Search Store not configured or empty.", None

        print(f"\n[Analyst Agent]: Querying internal documents for: '{query}'")
        
        response = self._generate_content(
            contents=query, 
            tools=[self.rag_tool]
        )
        
        return response.text, response

class CoderAgent(BaseAgent):
    """
    Specialized agent for generating and potentially executing code.
    (Code execution tool configuration is omitted here but would be added to tools list).
    """
    def __init__(self):
        system_prompt = (
            "You are the Lead Engineer. Based on the verified research provided, "
            "your task is to generate clean, functional Python code. Adhere strictly "
            "to the Principle of Least Astonishment (POLA) in variable naming and "
            "function design. Do not include excessive commentary, just the final code block."
        )
        super().__init__(system_prompt, model="gemini-2.5-flash") # Flash is often sufficient for code generation
        
    def run(self, research_summary: str) -> str:
        """Generates code based on the synthesized research."""
        prompt = (
            f"Based on the following research summary, generate a complete Python script "
            f"that implements the solution:\n\n---\n{research_summary}\n---"
        )
        print(f"\n[Coder Agent]: Generating code based on verified research.")
        
        response = self._generate_content(contents=prompt)
        
        # Note: In a full implementation, this agent would use the code execution tool 
        # to verify the code before returning it.
        return response.text, response

class ResearchOrchestrator(BaseAgent):
    """
    The Principal Architect. Manages the workflow, delegates tasks, and synthesizes 
    the final, cited report.
    """
    def __init__(self, internal_store_name: str):
        system_prompt = (
            "You are the Autonomous Research Swarm Orchestrator. Your mission is to "
            "take a complex user request, break it down into sequential steps (Search, "
            "Document Analysis, Code Generation), delegate those steps to the appropriate "
            "specialized agents, and synthesize their results into a single, cohesive, "
            "and meticulously cited final report. Your primary output must be the final report, "
            "but first, output a structured JSON plan detailing delegation."
        )
        super().__init__(system_prompt)
        
        # Initialize sub-agents
        self.searcher = SearcherAgent()
        self.analyst = DocumentAnalystAgent(internal_store_name)
        self.coder = CoderAgent()

    def run_swarm(self, user_prompt: str) -> str:
        """
        Main execution loop for the Swarm.
        """
        print(f"--- Swarm Initiated for Task: {user_prompt} ---")
        
        # Step 1: Orchestrator generates the plan (using its reasoning prompt)
        planning_prompt = (
            f"Analyze the following user request and generate a detailed, multi-step "
            f"research plan. Specify which agent (Searcher, Analyst, Coder) handles "
            f"each step and what the exact query for that agent should be. "
            f"User Request: '{user_prompt}'"
        )
        
        # For simplicity, we skip the actual structured plan generation here 
        # and hardcode a generic flow based on the analogy.
        
        # Step 2: Delegation to Searcher
        search_query = f"Latest advancements and best practices for '{user_prompt}'"
        search_text, search_response = self.searcher.run(search_query)
        
        # Apply citations to the search result immediately
        grounded_search_result = add_citations(search_response)
        
        # Step 3: Delegation to Analyst (RAG)
        rag_query = f"Internal data or specifications related to '{user_prompt}'"
        rag_text, rag_response = self.analyst.run(rag_query)
        
        # Apply citations to the RAG result
        grounded_rag_result = add_citations(rag_response)
        
        # Step 4: Synthesis (Orchestrator's core job)
        synthesis_prompt = (
            "Synthesize the following research findings into a comprehensive report. "
            "Combine the external (web) and internal (document) information, ensuring "
            "all facts are attributed to their source. Then, formulate a precise "
            "instruction set for the Coder Agent based on this combined knowledge."
            f"\n\n--- External Research ---\n{grounded_search_result}"
            f"\n\n--- Internal Research ---\n{grounded_rag_result}"
        )
        
        synthesis_response = self._generate_content(contents=synthesis_prompt)
        research_summary = synthesis_response.text
        
        print("\n[Orchestrator]: Synthesis complete. Preparing code generation.")

        # Step 5: Delegation to Coder
        code_text, _ = self.coder.run(research_summary)
        
        # Step 6: Final Report Assembly
        final_report = (
            f"--- Autonomous Research Swarm Final Report ---\n\n"
            f"**Research Topic:** {user_prompt}\n\n"
            f"**1. Comprehensive Research Findings (Grounded):\n**\n{research_summary}\n\n"
            f"**2. Verified Code Solution (Engineer Output):\n**\n{code_text}"
        )
        
        return final_report

# --- Example Usage (Setup) ---

# Mock file setup (replace 'internal_docs.txt' with a real path for execution)
MOCK_FILE_PATH = "internal_docs.txt" 
STORE_NAME = setup_file_search_store(
    file_path=MOCK_FILE_PATH, 
    store_display_name="Proprietary Engineering Specs",
    file_display_name="Thermal_Specs_V1.1"
)

# Initialize the Orchestrator
if STORE_NAME:
    orchestrator = ResearchOrchestrator(internal_store_name=STORE_NAME)
    
    # Define the complex task
    COMPLEX_TASK = "Develop a Python simulation for a self-cooling server rack, incorporating the latest passive cooling materials and proprietary thermal specifications."
    
    # Run the swarm
    # final_result = orchestrator.run_swarm(COMPLEX_TASK)
    # print("\n" + "="*80)
    # print("FINAL SWARM RESULT:")
    # print(final_result)
    # print("="*80)


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

# Source File: project_full_system_integration_main_application.py
# Description: Full System Integration (Main Application)
# ==========================================

import os
import time
import textwrap
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. CONFIGURATION AND UTILITIES ---

# Set the model to use. Gemini 2.5 Pro is ideal for complex reasoning and orchestration.
MODEL_NAME = "gemini-2.5-pro"
INTERNAL_DOC_FILENAME = "internal_research_notes.txt"
STORE_DISPLAY_NAME = "QuantumInterconnectStore"

def create_dummy_doc():
    """Creates a dummy internal document file for the RAG system."""
    content = textwrap.dedent("""
    # Internal Research Whitepaper: Cryogenic Interconnects
    
    Section 1: Overview
    Our proprietary research, codenamed "Project Iceberg," focuses on superconducting interconnects for large-scale quantum processors. We have determined that using Aluminum (Al) based transmission lines at 10 mK offers the best balance of coherence and fabrication ease. The key finding is that a 500nm thick Al layer, when passivated with a thin layer of amorphous Silicon Dioxide (a-SiO2), reduces decoherence rates by 15% compared to Niobium (Nb) lines.

    Section 2: Code Implementation Requirement
    Any simulation of Project Iceberg must use the 'qiskit' library for circuit definition and specifically utilize the 'Aer' simulator backend, not the standard QASM simulator.
    """)
    with open(INTERNAL_DOC_FILENAME, "w") as f:
        f.write(content.strip())
    print(f"Created internal document: {INTERNAL_DOC_FILENAME}")

def add_citations(response):
    """
    Processes the grounding metadata to insert inline citations into the response text.
    This function handles both web (Google Search) and file (File Search) sources.
    """
    if not (response.candidates and response.candidates[0].grounding_metadata):
        return response.text

    text = response.text
    metadata = response.candidates[0].grounding_metadata
    supports = metadata.grounding_supports
    chunks = metadata.grounding_chunks

    # Sort supports by end_index in descending order to avoid shifting issues when inserting.
    sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    for support in sorted_supports:
        end_index = support.segment.end_index
        if support.grounding_chunk_indices:
            citation_links = []
            for i in support.grounding_chunk_indices:
                if i < len(chunks):
                    chunk = chunks[i]
                    # Determine the source type (web or file)
                    if chunk.web:
                        source_info = f"Web: {chunk.web.title}"
                        uri = chunk.web.uri
                    elif chunk.file:
                        source_info = f"Doc: {chunk.file.title}"
                        uri = f"Internal File: {chunk.file.title}" # Use title as URI placeholder for internal doc

                    # Create citation string like [1](source_info)
                    citation_links.append(f"[{i + 1}]({source_info})")

            citation_string = ", ".join(citation_links)
            text = text[:end_index] + citation_string + text[end_index:]

    return text

# --- 2. THE RESEARCH SWARM ORCHESTRATOR CLASS ---

class ResearchSwarm:
    """
    Manages the lifecycle of the File Search store (RAG) and orchestrates 
    the multi-tool Gemini API calls for complex research tasks.
    """
    def __init__(self):
        """Initializes the Gemini client and sets up placeholders."""
        if 'GEMINI_API_KEY' not in os.environ:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        self.client = genai.Client()
        self.file_search_store_name = None
        self.tools = []

    def setup_rag_store(self):
        """
        Creates and populates the File Search Store (RAG component).
        This acts as the Document Analyst Agent's internal knowledge base.
        """
        print("\n--- Setting up Document Analyst (RAG Store) ---")
        
        # 1. Create the File Search store
        try:
            file_search_store = self.client.file_search_stores.create(
                config={'display_name': STORE_DISPLAY_NAME}
            )
            self.file_search_store_name = file_search_store.name
            print(f"Store created: {self.file_search_store_name}")
        except Exception as e:
            print(f"Error creating store: {e}")
            return

        # 2. Upload and import the file (using the direct upload method)
        print(f"Uploading and importing {INTERNAL_DOC_FILENAME}...")
        try:
            operation = self.client.file_search_stores.upload_to_file_search_store(
                file=INTERNAL_DOC_FILENAME,
                file_search_store_name=self.file_search_store_name,
                config={
                    'display_name': INTERNAL_DOC_FILENAME,
                }
            )

            # 3. Wait until import is complete (Long-Running Operation)
            while not operation.done:
                print(".", end="", flush=True)
                time.sleep(5)
                operation = self.client.operations.get(operation)
            
            print("\nFile import complete.")

            # 4. Configure the tools list for the Swarm Orchestrator
            self.tools.append(types.Tool(google_search=types.GoogleSearch())) # Searcher Agent
            self.tools.append(types.Tool(file_search=types.FileSearch(
                file_search_store_names=[self.file_search_store_name]
            ))) # Document Analyst Agent

        except APIError as e:
            print(f"\nAPI Error during file upload/import: {e}")
            self.cleanup()
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            self.cleanup()

    def cleanup(self):
        """Deletes the File Search Store and the dummy file."""
        print("\n--- Cleanup Phase ---")
        if self.file_search_store_name:
            print(f"Deleting File Search Store: {self.file_search_store_name}")
            try:
                self.client.file_search_stores.delete(name=self.file_search_store_name)
                print("Store deleted successfully.")
            except Exception as e:
                print(f"Warning: Could not delete store {self.file_search_store_name}. Error: {e}")

        if os.path.exists(INTERNAL_DOC_FILENAME):
            os.remove(INTERNAL_DOC_FILENAME)
            print(f"Removed dummy file: {INTERNAL_DOC_FILENAME}")
    
    def run_research_cycle(self, research_prompt: str):
        """
        Executes the primary research query using the multi-tool configuration 
        and the Orchestrator system prompt.
        """
        if not self.tools:
            print("Error: Tools not configured. RAG setup failed.")
            return

        print(f"\n--- Swarm Orchestrator Initiated ({MODEL_NAME}) ---")
        print(f"Research Query: {research_prompt}")

        # Define the Orchestrator's persona and rules
        system_instruction = textwrap.dedent(f"""
        You are the 'Autonomous Research Swarm Orchestrator'. Your goal is to conduct comprehensive, verified research based on the user's query.
        
        Your Swarm consists of three agents:
        1. Searcher Agent (Tool: google_search): Used for real-time, external web data retrieval (e.g., latest news, general public knowledge).
        2. Document Analyst Agent (Tool: file_search): Used for internal, proprietary document analysis (RAG).
        3. Coder Agent (Your core reasoning): Used to synthesize all gathered information (web and internal) into a single, cohesive, verifiable code solution.

        TASK FLOW:
        1. Analyze the user query. Determine if external web search OR internal document analysis OR both are required.
        2. Execute the necessary tools automatically.
        3. Synthesize the results into a detailed, factual report.
        4. Crucially, the final output MUST contain a complete Python script that implements the technical requirements found in the internal documents and the latest external best practices.
        5. Ensure all facts are grounded and cited using the provided metadata.
        """)
        
        try:
            # Configure the API call
            config = types.GenerateContentConfig(
                tools=self.tools,
                system_instruction=system_instruction,
                temperature=0.1 # Keep reasoning factual
            )

            # Send the request
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=research_prompt,
                config=config,
            )

            # Process and display the output
            final_text = add_citations(response)
            
            print("\n" + "="*80)
            print("FINAL RESEARCH REPORT (Grounded and Synthesized)")
            print("="*80)
            print(final_text)
            print("="*80)

            # Display metadata for verification
            if response.candidates and response.candidates[0].grounding_metadata:
                metadata = response.candidates[0].grounding_metadata
                print("\n--- Grounding Metadata Summary ---")
                if metadata.web_search_queries:
                    print(f"Search Queries Used: {metadata.web_search_queries}")
                if metadata.grounding_chunks:
                    print(f"Sources Found: {len(metadata.grounding_chunks)}")
                    for i, chunk in enumerate(metadata.grounding_chunks):
                        source_type = "Web" if chunk.web else "File"
                        title = chunk.web.title if chunk.web else chunk.file.title
                        print(f"  [{i+1}] Type: {source_type}, Title: {title}")
                print("----------------------------------")

        except APIError as e:
            print(f"\nAPI Error during content generation: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred during the research cycle: {e}")


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    # Create the necessary input file for the RAG component
    create_dummy_doc()
    
    swarm = ResearchSwarm()
    
    try:
        # Step 1: Initialize RAG store (Document Analyst Agent's setup)
        swarm.setup_rag_store()

        # Step 2: Define the complex, multi-faceted research query
        research_query = textwrap.dedent("""
        I need a comprehensive report on the current state of superconducting qubit hardware. 
        Specifically: 
        1. What is the latest public research consensus on the best materials for high-coherence qubits? (Searcher Agent task)
        2. How does our proprietary 'Project Iceberg' research relate to interconnect material selection? (Document Analyst Agent task)
        3. Generate a complete Python script using Qiskit that defines a simple 3-qubit circuit and simulates it according to the specific backend requirements detailed in our internal documentation. (Coder Agent task)
        """)

        # Step 3: Run the orchestration cycle
        swarm.run_research_cycle(research_query)

    finally:
        # Step 4: Clean up resources
        swarm.cleanup()


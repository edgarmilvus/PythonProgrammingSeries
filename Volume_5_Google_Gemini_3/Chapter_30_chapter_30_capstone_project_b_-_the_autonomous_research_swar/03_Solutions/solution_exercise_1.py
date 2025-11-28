
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
import time
import tempfile
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. AgentManager: Core Utilities and File Search Management (DRY Principle) ---

class AgentManager:
    """
    Manages the Gemini client, handles file search store operations (RAG),
    and provides citation processing utility.
    """
    def __init__(self, model: str = "gemini-2.5-flash"):
        """Initializes the Gemini client and sets the default model."""
        try:
            # The Python Interpreter requires the GEMINI_API_KEY environment variable.
            self.client = genai.Client()
        except Exception as e:
            print(f"Error initializing Gemini client. Ensure API Key is set: {e}")
            raise
        
        self.model = model
        self.file_search_store_name = None
        self.temp_file_path = None
        
        # Define base configuration (no tools enabled by default)
        self.base_config = types.GenerateContentConfig()

    @staticmethod
    def add_citations(response: types.GenerateContentResponse) -> str:
        """
        Processes the grounding metadata to insert inline, clickable citations
        into the model's text response. This function uses the logic provided
        in the official documentation.
        """
        text = response.text
        
        # Check if grounding metadata exists
        if not response.candidates or not response.candidates[0].grounding_metadata:
            return text

        supports = response.candidates[0].grounding_metadata.grounding_supports
        chunks = response.candidates[0].grounding_metadata.grounding_chunks

        # Sort supports by end_index in descending order to avoid shifting issues
        # when inserting citation strings into the text.
        sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

        for support in sorted_supports:
            end_index = support.segment.end_index
            
            if support.grounding_chunk_indices:
                citation_links = []
                for i in support.grounding_chunk_indices:
                    if i < len(chunks) and chunks[i].web:
                        # For web search grounding
                        uri = chunks[i].web.uri
                        citation_links.append(f"[{i + 1}](Source: Web)") # Simplified link text for terminal output
                    elif i < len(chunks) and chunks[i].file:
                        # For file search grounding (RAG)
                        # The file name provides the source context
                        uri = chunks[i].file.name
                        citation_links.append(f"[{i + 1}](Source: Docs)") 

                citation_string = ", ".join(citation_links)
                # Insert the citation string at the segment's end index
                text = text[:end_index] + " " + citation_string + text[end_index:]

        return text

    # --- File Search Store Management Methods ---

    def create_and_upload_document(self, content: str, file_name: str, store_name: str):
        """
        Creates a temporary file, uploads it to a new File Search Store,
        and waits for the indexing operation to complete.
        """
        print(f"\n[RAG Setup] Creating File Search Store: {store_name}...")
        
        # 1. Create temporary local file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(content)
            self.temp_file_path = tmp_file.name
            
        # 2. Create the persistent File Search store
        try:
            file_search_store = self.client.file_search_stores.create(
                config={'display_name': store_name}
            )
            self.file_search_store_name = file_search_store.name
        except APIError as e:
            print(f"Error creating store. Ensure file search is enabled on your project: {e}")
            raise

        # 3. Upload and import the file to the store (long-running operation)
        print(f"[RAG Setup] Uploading {file_name} to store {self.file_search_store_name}...")
        operation = self.client.file_search_stores.upload_to_file_search_store(
            file=self.temp_file_path,
            file_search_store_name=self.file_search_store_name,
            config={'display_name': file_name}
        )

        # Wait until import is complete
        while not operation.done:
            print("[RAG Setup] Waiting for file indexing (5s)...")
            time.sleep(5)
            operation = self.client.operations.get(operation)
        
        print(f"[RAG Setup] File indexing complete. Store ready: {self.file_search_store_name}")

    def cleanup_store(self):
        """Deletes the File Search Store and the temporary local file."""
        if self.file_search_store_name:
            print(f"\n[Cleanup] Deleting File Search Store: {self.file_search_store_name}")
            self.client.file_search_stores.delete(name=self.file_search_store_name)
            self.file_search_store_name = None
        
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)
            print("[Cleanup] Removed temporary local file.")


# --- 2. Specialized Agents ---

class SearcherAgent(AgentManager):
    """
    Specialized agent for real-time web research using the Google Search tool.
    """
    def __init__(self):
        super().__init__()
        print("[Agent Init] SearcherAgent activated (Google Search Grounding).")
        
        # Configuration for web grounding
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        self.search_config = types.GenerateContentConfig(
            tools=[grounding_tool]
        )

    def conduct_search(self, task_prompt: str) -> dict:
        """Executes a real-time web search and returns grounded text and metadata."""
        print(f"\n--- Searcher Agent Executing Task ---\nQuery: {task_prompt}")
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=task_prompt,
            config=self.search_config,
        )
        
        # Use the utility function to add citations
        grounded_text = self.add_citations(response)
        
        search_queries = []
        if response.candidates and response.candidates[0].grounding_metadata:
            search_queries = response.candidates[0].grounding_metadata.web_search_queries
        
        print(f"Search Queries Used: {search_queries}")
        return {
            "text": grounded_text,
            "queries": search_queries,
            "raw_response": response
        }


class DocumentAgent(AgentManager):
    """
    Specialized agent for internal document analysis using the File Search RAG tool.
    Requires a File Search Store name to be set in the manager.
    """
    def __init__(self, store_name: str):
        super().__init__()
        self.store_name = store_name
        print(f"[Agent Init] DocumentAgent activated (File Search RAG on {store_name}).")
        
        # Configuration for File Search RAG
        self.rag_config = types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[store_name]
                    )
                )
            ]
        )

    def analyze_docs(self, task_prompt: str, context: str) -> str:
        """
        Analyzes the internal documents based on the prompt and external context.
        """
        print("\n--- Document Agent Executing Task ---")
        full_prompt = (
            f"CONTEXT FROM WEB SEARCH:\n{context}\n\n"
            f"INTERNAL DOCUMENT ANALYSIS TASK:\n{task_prompt}"
        )
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=self.rag_config,
        )
        
        # Add citations for RAG sources
        grounded_text = self.add_citations(response)
        return grounded_text


class CoderAgent(AgentManager):
    """
    Specialized agent for generating clean, verified code solutions.
    """
    def __init__(self):
        super().__init__()
        print("[Agent Init] CoderAgent activated (Code Generation).")
        # No special tools required, uses base_config

    def generate_code(self, task_prompt: str, research_context: str) -> str:
        """
        Generates Python code based on the accumulated research context.
        """
        print("\n--- Coder Agent Executing Task ---")
        system_instruction = (
            "You are an expert Python developer. Your only output must be a single, "
            "complete, executable Python script enclosed in a markdown block. "
            "Ensure the code is clean, well-commented, and follows the DRY principle."
        )
        
        full_prompt = (
            f"RESEARCH CONTEXT:\n{research_context}\n\n"
            f"CODING TASK:\n{task_prompt}"
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Content(role="user", parts=[types.Part.from_text(full_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        return response.text


# --- 3. The Orchestrator: ResearchSwarm ---

class ResearchSwarm:
    """
    Manages the overall research workflow, delegating tasks to specialized agents.
    """
    def __init__(self, research_topic: str):
        self.topic = research_topic
        self.manager = AgentManager()
        self.internal_store_name = "Capstone_Research_Store"
        self.internal_file_name = "Proprietary_AI_Policy.txt"
        self.research_context = ""
        self.final_report = ""

    def _setup_internal_rag(self):
        """Sets up the RAG environment before the research begins."""
        # Define a proprietary document content for the Document Agent to reference
        internal_doc_content = (
            "Proprietary AI Policy Document 2025:\n\n"
            "Section 4.1: All external web retrieval must be grounded with verifiable citations.\n"
            "Section 4.2: For all new Python code, the recommended library for asynchronous operations "
            "is 'asyncio', specifically utilizing the 'gather' function for concurrent tasks. "
            "Standard multi-threading is deprecated for high-performance I/O operations."
        )
        
        # Use the manager to create the store and upload the document
        self.manager.create_and_upload_document(
            content=internal_doc_content,
            file_name=self.internal_file_name,
            store_name=self.internal_store_name
        )

    def run_research(self):
        """Executes the full, multi-stage research lifecycle."""
        
        print("\n=======================================================")
        print(f"STARTING AUTONOMOUS RESEARCH SWARM: {self.topic}")
        print("=======================================================")
        
        try:
            # Stage 1: RAG Setup
            self._setup_internal_rag()
            
            # Stage 2: External Search (Searcher Agent)
            searcher = SearcherAgent()
            search_task = f"Find the latest information on the Python 'asyncio' library performance benchmarks compared to traditional threading for I/O operations."
            search_result = searcher.conduct_search(search_task)
            
            self.research_context += f"## 1. Web Search Results (Grounded)\n{search_result['text']}\n\n"
            print("\n--- Searcher Agent Report (Grounded) ---")
            print(search_result['text'])
            
            # Stage 3: Internal Document Analysis (Document Agent)
            document_agent = DocumentAgent(store_name=self.manager.file_search_store_name)
            doc_task = (
                "Based on the proprietary policy document, confirm the preferred concurrency "
                "method for high-performance Python I/O operations. Use the web search context "
                "to provide a brief summary of the 'asyncio' library's main function."
            )
            doc_analysis = document_agent.analyze_docs(doc_task, search_result['text'])
            
            self.research_context += f"## 2. Internal Document Analysis (RAG)\n{doc_analysis}\n\n"
            print("\n--- Document Agent Report (RAG Grounded) ---")
            print(doc_analysis)
            
            # Stage 4: Code Generation (Coder Agent)
            coder = CoderAgent()
            code_task = (
                "Generate a minimal, complete Python script that demonstrates how to use "
                "the 'asyncio.gather' function to concurrently fetch data from three "
                "hypothetical web endpoints. Ensure the code adheres to the principles derived "
                "from the internal document analysis."
            )
            generated_code = coder.generate_code(code_task, self.research_context)
            
            self.research_context += f"## 3. Generated Code Solution\n{generated_code}\n"
            
            # Stage 5: Final Report Compilation
            self.final_report = (
                f"Autonomous Research Swarm Final Report: {self.topic}\n"
                "----------------------------------------------------\n\n"
                f"{self.research_context}"
            )
            
            print("\n=======================================================")
            print("RESEARCH COMPLETE. Final Code Output:")
            print("=======================================================")
            print(generated_code)

        except Exception as e:
            print(f"\n[CRITICAL ERROR] Swarm failed during execution: {e}")
        finally:
            # Stage 6: Cleanup
            self.manager.cleanup_store()


# --- Main Execution Block ---
if __name__ == "__main__":
    # Ensure your GEMINI_API_KEY is set in your environment variables
    
    research_topic = "Python Asynchronous I/O using asyncio.gather"
    swarm = ResearchSwarm(research_topic)
    swarm.run_research()

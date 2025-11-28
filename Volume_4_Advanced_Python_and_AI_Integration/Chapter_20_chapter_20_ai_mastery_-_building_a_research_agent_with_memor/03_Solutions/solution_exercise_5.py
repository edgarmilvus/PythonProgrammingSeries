
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

from typing import Type, Optional
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- 1. Simulated Metadata & Indexing ---
docs_with_metadata = [
    Document(
        page_content="The Q3 launch utilized the new quantum encryption standard, detailed in section 4.1.",
        metadata={"source": "Internal Report", "date": "2024-09-01"}
    ),
    Document(
        page_content="Public opinion on the Q3 launch was generally positive, highlighting the speed improvements.",
        metadata={"source": "Public News", "date": "2024-09-05"}
    ),
    Document(
        page_content="A detailed technical analysis of the quantum encryption implementation is available in the internal repository.",
        metadata={"source": "Internal Report", "date": "2024-09-02"}
    ),
    Document(
        page_content="Market analysts noted that the Q3 launch boosted stock prices by 5%.",
        metadata={"source": "Public News", "date": "2024-09-06"}
    )
]

embeddings_filter = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store_filter = Chroma.from_documents(
    docs_with_metadata, 
    embeddings_filter, 
    collection_name="filtered_rag_data"
)

# --- 2. The Retrieval Tool Modification ---
class FilteredRetrievalInput(BaseModel):
    """Input schema for retrieving documents with an optional source filter."""
    query: str = Field(description="The technical question or topic to search for.")
    source_filter: Optional[str] = Field(
        default=None, 
        description="Optional filter for the document source (e.g., 'Internal Report', 'Public News')."
    )

@tool(args_schema=FilteredRetrievalInput)
def get_filtered_context(query: str, source_filter: Optional[str] = None) -> str:
    """
    Retrieves relevant document context from the knowledge base, optionally filtered
    by the document source metadata (e.g., 'Internal Report').
    """
    if source_filter:
        # Construct the filter dictionary for Chroma where clause
        filter_criteria = {"source": source_filter}
        print(f"\n--- Tool Execution: Applying Filter: {filter_criteria} ---")
        docs = vector_store_filter.similarity_search(
            query=query, 
            k=5, 
            where=filter_criteria
        )
    else:
        print("\n--- Tool Execution: Running Unfiltered Search ---")
        docs = vector_store_filter.similarity_search(query=query, k=5)
    
    if not docs:
        return "No relevant documents found matching the query and filter criteria."
    
    # Format the retrieved documents, including source metadata
    context = "\n\n".join([f"Source: {d.metadata['source']}\nContent: {d.page_content}" for d in docs])
    return context

# --- 3. Agent Adaptation ---
llm_filter_agent = ChatOpenAI(temperature=0, model="gpt-4o-mini")
tools_filter = [get_filtered_context]

prompt_filter = ChatPromptTemplate.from_messages([
    ("system", "You are a precise Research Agent. Use the 'get_filtered_context' tool. If the user specifies a source (e.g., 'Internal Report'), you MUST use the 'source_filter' parameter."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent_filter = create_openai_tools_agent(llm_filter_agent, tools_filter, prompt_filter)
agent_executor_filter = AgentExecutor(
    agent=agent_filter, 
    tools=tools_filter, 
    verbose=True, 
    handle_parsing_errors=True
)

# --- 4. Verification of Filtering ---

# Scenario A (Unfiltered)
q_unfiltered = "What information is available about the Q3 launch?"
print("\n=======================================================")
print(f"SCENARIO A: UNFILTERED QUERY: {q_unfiltered}")
agent_executor_filter.invoke({"input": q_unfiltered})

# Scenario B (Filtered)
q_filtered = "Find information about the Q3 launch, but only using Public News."
print("\n=======================================================")
print(f"SCENARIO B: FILTERED QUERY: {q_filtered}")
agent_executor_filter.invoke({"input": q_filtered})

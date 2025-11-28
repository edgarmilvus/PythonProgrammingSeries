
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

print("--- Exercise 4: Interactive Challenge (Source Citation) ---")

# 1. Define Custom Prompt
citation_template = """You are an expert RAG system. Use ONLY the following context to answer the question.
If the context does not contain the answer, state explicitly that the information is not available in the source documents.
After providing your answer, list the exact source text you used under the heading 'Sources Used:'.

Context: {context}
Question: {question}

Answer:"""

CITATION_PROMPT = PromptTemplate(
    template=citation_template, input_variables=["context", "question"]
)

# 2. Enable Source Return & Chain Construction
qa_chain_citation = RetrievalQA.from_chain_type(
    llm=LLM,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True, # CRITICAL: Enables source document return
    chain_type_kwargs={"prompt": CITATION_PROMPT} # Inject custom prompt
)

# 3. Execution and Parsing
query_citation = "How does Python handle memory-efficient iteration?"
print(f"\nQuery requiring citation: {query_citation}")

response_citation = qa_chain_citation.invoke({"query": query_citation})

print("\n--- LLM Result with Citation Prompt ---")
# The LLM's response should contain both the answer and the source text, 
# as dictated by the custom prompt.
print(response_citation['result'])

# 4. Source Extraction (Programmatic Verification)
print("\n--- Extracted Source Documents (Verification) ---")
if 'source_documents' in response_citation:
    for i, doc in enumerate(response_citation['source_documents']):
        print(f"Source Document {i+1} Content:\n{doc.page_content}\n---")
else:
    print("Source documents were not returned. Check 'return_source_documents=True'.")

print("-" * 60)

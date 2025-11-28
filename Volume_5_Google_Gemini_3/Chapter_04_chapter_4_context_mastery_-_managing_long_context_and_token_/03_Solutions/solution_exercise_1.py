
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
import random
from google import genai
from google.genai import types

# --- Configuration and Setup (Using Dummy Client for Simulation) ---

# NOTE: In a real environment, you would initialize the client normally:
# client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Define placeholder objects to simulate API responses for Exercise 3
class FileReference:
    def __init__(self, file_id, path):
        self.name = file_id
        self.path = path

class CachedContentReference:
    def __init__(self, cache_id):
        self.name = cache_id

# Dummy Client Implementation
class DummyClient:
    def __init__(self):
        self.files = self.FileManager()
        self.cached_content = self.CacheManager()
        self.models = self.ModelManager()

    class FileManager:
        def upload(self, file_path):
            # Simulated API Call: Uploading a large file
            print(f"-> [File API] Uploading {file_path}. This takes time...")
            time.sleep(0.1)
            # Returns a File object with an ID
            # Use a deterministic hash for simulation stability
            file_id = f"files/{abs(hash(file_path))}"
            return types.File(name=file_id, display_name=file_path)

    class CacheManager:
        def create(self, content_parts: list, model: str):
            # Simulated API Call: Creating a cached content object
            # Estimate token count based on typical large document size
            simulated_tokens = random.randint(450000, 550000)
            print(f"-> [Cache API] Creating cache for {model}. Estimated tokens: {simulated_tokens}...")
            time.sleep(0.5)
            
            # The cache ID is derived from the content (simulated)
            cache_id = f"cached_content/{abs(hash(str(content_parts)))}"
            return types.CachedContent(
                name=cache_id, 
                model=model, 
                usage_metadata={'total_token_count': simulated_tokens}
            )

    class ModelManager:
        def generate_content(self, model, contents):
            # Simulated API Call: Generating content
            
            # Calculate input length based on the string representation of all parts
            input_length = len(str(contents))
            
            response_text = f"[[SIMULATED RESPONSE: Model processed ~{input_length // 4} tokens of context.]]"
            
            # Simulate core reasoning for the exercises
            contents_str = str(contents)
            
            if "Project Chimera" in contents_str:
                response_text += "\n\nAnswer: The project codename is Project Chimera."
            
            if "contradictions" in contents_str:
                response_text += (
                    "\n\nSynthesis Summary: The unified summary highlights a key conflict in retention policies: "
                    "Technical Spec requires 90 days (T-102), while the Policy Manual requires 120 days (P-30.2). "
                    "The model synthesizes the strict requirement (120 days) for compliance."
                )
            
            if "Legacy Log Format" in contents_str and "E-999" in contents_str:
                response_text += "\n\nExtracted JSON: {'id': 101, 'user': 'test_user', 'error_code': 'E-999', 'description': 'Final production test event'}"
                
            return types.GenerateContentResponse(text=response_text)

client = DummyClient()
LONG_CONTEXT_MODEL = 'gemini-2.5-pro' # Model capable of 1M+ tokens
    
print(f"Using simulated client and target model: {LONG_CONTEXT_MODEL}")

# --- Exercise 1: The Long-Form Synthesis Challenge ---

def generate_massive_context(token_target: int = 500000) -> str:
    """Generates a large block of text to simulate a massive context window input."""
    
    # Estimate: 4 characters per token
    char_target = token_target * 4
    
    # Simulate technical document with specific requirements
    tech_spec_chunk = (
        "## Technical Specification v1.5: Data Handling Protocol. "
        "All user data must be encrypted using AES-256 (Requirement T-101). "
        "Log files must be retained for a minimum of 90 days (Requirement T-102). "
        "Access is limited to level 3 engineers. "
    )
    
    # Simulate policy manual with conflicting requirements
    policy_manual_chunk = (
        "## Policy Manual P-30: Corporate Compliance. "
        "All sensitive customer information must be secured via industry-standard encryption (Policy P-30.1). "
        "Audit logs must be preserved for a minimum of 120 days to meet external regulatory requirements (Policy P-30.2). "
        "Access is granted to all compliance officers. "
    )
    
    # Repeat chunks to reach the massive token target
    repetition_factor = char_target // (len(tech_spec_chunk) + len(policy_manual_chunk))
    
    return (tech_spec_chunk + policy_manual_chunk) * repetition_factor

def run_long_form_synthesis():
    """Executes the massive context analysis task."""
    print("\n" + "="*50)
    print("--- Exercise 1: Long-Form Synthesis Challenge ---")
    
    massive_text = generate_massive_context(token_target=500000)
    
    # The prompt structure: Context first, Query last (Optimal placement)
    system_instruction = (
        "You are an expert compliance analyst. Your task is to analyze the following "
        "massive corpus of documents and synthesize the required information."
    )
    
    query = (
        f"\n\n--- ANALYSIS QUERY (Place at End for Optimal Retrieval) ---\n"
        f"1. Identify three potential contradictions (e.g., retention periods, access roles, encryption methods) "
        f"between the Technical Specification and the Policy Manual based solely on the provided text. "
        f"2. Generate a single, 500-word executive summary of the unified compliance requirements."
    )
    
    # The Gemini API uses a list of contents (parts)
    full_prompt_parts = [
        system_instruction,
        massive_text,
        query
    ]
    
    print(f"Sending request with approximately {len(massive_text) // 4} tokens...")
    
    response = client.models.generate_content(
        model=LONG_CONTEXT_MODEL,
        contents=full_prompt_parts
    )
    
    print("Response received (Demonstrates cross-document reasoning):")
    print(response.text)


# --- Exercise 2: Many-Shot In-Context Learning Accelerator ---

def generate_many_shot_examples(num_examples: int = 100) -> str:
    """Generates structured input/output pairs for many-shot learning."""
    
    examples = []
    
    # The template for the proprietary log format
    log_template = "LOG_ID: {id} | USER: {user}@{domain} | STATUS: {status} | TIME: 2024-08-15 14:{minute:02d}:00 | PAYLOAD: \"{payload}\""
    
    for i in range(1, num_examples + 1):
        log_id = 90000 + i
        user = f"user_{i}"
        status = f"E-{i % 10 + 100}"
        payload = f"System event {i} triggered in module {random.choice(['Alpha', 'Beta', 'Gamma'])}"
        
        input_log = log_template.format(
            id=log_id, 
            user=user, 
            domain="corp", 
            status=status, 
            minute=i % 60, 
            payload=payload
        )
        
        # The complex, proprietary output structure the model must learn
        output_json = (
            f'{{"id": {log_id}, "user": "{user}", "error_code": "{status}", '
            f'"description": "{payload}"}}'
        )
        
        examples.append(f"INPUT:\n{input_log}\nOUTPUT:\n{output_json}\n---")

    return "\n".join(examples)

def run_many_shot_extraction():
    """Tests the model's ability to learn a complex format from 100 examples."""
    print("\n" + "="*50)
    print("--- Exercise 2: Many-Shot In-Context Learning Accelerator ---")
    
    example_set = generate_many_shot_examples(100)
    
    system_instruction = (
        "You are a specialized log parser. Your task is to learn the exact conversion "
        "rules from the proprietary 'Legacy Log Format' (shown in 100 examples below) "
        "to the required clean JSON structure. Apply the learned format strictly."
        "\n\n--- 100 LEARNING EXAMPLES ---\n"
    )
    
    # The final unseen test case (must be processed based on the 100 shots)
    test_input = (
        "\n\n--- TEST CASE ---\n"
        "INPUT:\nLOG_ID: 101 | USER: test_user@prod | STATUS: E-999 | TIME: 2024-08-16 09:00:00 | PAYLOAD: \"Final production test event\""
        "\nOUTPUT:\n"
    )
    
    full_prompt_parts = [
        system_instruction,
        example_set,
        test_input
    ]

    print(f"Sending request with {100} structured examples...")
    
    response = client.models.generate_content(
        model=LONG_CONTEXT_MODEL,
        contents=full_prompt_parts
    )
    
    print("Model response (Should successfully apply the complex, learned JSON transformation):")
    print(response.text)


# --- Exercise 3: The Advanced Challenge: RAG Replacement via Context Caching ---

def simulate_file_upload(file_path: str) -> FileReference:
    """Simulates the upload of a large source document (e.g., 10MB PDF)."""
    # Uses the DummyClient's FileManager
    file_ref = client.files.upload(file_path)
    return FileReference(file_ref.name, file_path)

def cache_content(file_ref: FileReference) -> CachedContentReference:
    """Simulates creating a CachedContent object from the uploaded file."""
    
    # Crucial step: Reference the uploaded file using its URI/name
    content_parts = [
        # The API knows how to process the file content from this reference
        types.Part.from_uri(uri=f"file://{file_ref.name}", mime_type="application/pdf"),
        "Please cache this entire document for fast retrieval and querying."
    ]
    
    # Uses the DummyClient's CacheManager
    cache_ref = client.cached_content.create(
        content_parts=content_parts,
        model=LONG_CONTEXT_MODEL
    )
    
    print(f"Cache created successfully. Cached content ID: {cache_ref.name}")
    print(f"Initial Cost Incurred for Caching: {cache_ref.usage_metadata.get('total_token_count', 'Unknown')} tokens.")
    return CachedContentReference(cache_ref.name)

def query_cached_content(cache_ref: CachedContentReference, user_query: str):
    """Queries the model using the CachedContent ID instead of raw tokens."""
    
    # The input structure leverages the cached content reference
    contents = [
        # This part tells the model to use the massive, pre-processed context
        types.Part.from_cached_content(name=cache_ref.name),
        user_query # The actual query is small, minimizing I/O cost
    ]
    
    print(f"\nSending query using cached content ID: {cache_ref.name}.")
    print("Optimization: Only the small query tokens are billed for input, not the massive document.")
    
    response = client.models.generate_content(
        model=LONG_CONTEXT_MODEL,
        contents=contents
    )
    
    print(f"Query Response:\n{response.text}")

def run_context_caching_challenge():
    """Orchestrates the RAG replacement workflow."""
    print("\n" + "="*50)
    print("--- Exercise 3: Context Caching Challenge (RAG Replacement) ---")
    
    SOURCE_DOCUMENT_PATH = "project_alpha_spec_v1.pdf"
    
    # 1. Simulate initial file upload (Done once)
    file_ref = simulate_file_upload(SOURCE_DOCUMENT_PATH)
    
    # 2. Cache the content (Done once - pays the large input token cost once)
    cached_ref = cache_content(file_ref)
    
    # 3. Simulate multiple user queries (Done repeatedly - pays minimal input cost)
    print("\n--- Simulating Repeated Queries (Cost Savings Applied) ---")
    query_1 = "What is the primary security requirement for external data access?"
    query_2 = "Summarize the section on disaster recovery procedures."
    
    query_cached_content(cached_ref, query_1)
    query_cached_content(cached_ref, query_2)

# --- Exercise 4: Positional Bias and Optimal Query Placement ---

def create_long_haystack(length_tokens: int = 150000) -> str:
    """Generates a long string of filler text."""
    # Ensure the filler text is long enough to simulate a massive context
    filler_text = "The quick brown fox jumps over the lazy dog. Programming is fun. Context mastery is key. "
    # Target character count based on token estimate
    return filler_text * (length_tokens * 4 // len(filler_text))

def run_positional_bias_test():
    """Tests the impact of query placement (needle-in-a-haystack)."""
    print("\n" + "="*50)
    print("--- Exercise 4: Positional Bias Test ---")
    
    HAYSTACK_LENGTH = 150000 # Tokens
    NEEDLE = "The project codename for this initiative is Project Chimera."
    QUERY = "What is the project codename for this initiative? (Answer based ONLY on the context provided.)"
    
    haystack = create_long_haystack(HAYSTACK_LENGTH)
    haystack_len_chars = len(haystack)
    
    # Test 1: Needle at the Start
    # The query is still placed at the end, testing retrieval accuracy
    prompt_start = [
        f"--- START OF CONTEXT ---\n{NEEDLE}\n{haystack}",
        QUERY
    ]
    
    print("\nTest 1: Needle at START (Length: ~150k tokens)")
    response_start = client.models.generate_content(
        model=LONG_CONTEXT_MODEL,
        contents=prompt_start
    )
    print(f"Result: {response_start.text.splitlines()[-1]}")
    
    # Test 2: Needle in the Middle
    middle_index = haystack_len_chars // 2
    prompt_middle = [
        f"--- START OF CONTEXT ---\n{haystack[:middle_index]}\n{NEEDLE}\n{haystack[middle_index:]}",
        QUERY
    ]
    
    print("\nTest 2: Needle in MIDDLE (Length: ~150k tokens)")
    response_middle = client.models.generate_content(
        model=LONG_CONTEXT_MODEL,
        contents=prompt_middle
    )
    print(f"Result: {response_middle.text.splitlines()[-1]}")

    # Test 3: Needle at the End (Recommended Optimal Position)
    prompt_end = [
        f"--- START OF CONTEXT ---\n{haystack}\n{NEEDLE}",
        QUERY
    ]
    
    print("\nTest 3: Needle at END (Length: ~150k tokens) - RECOMMENDED")
    response_end = client.models.generate_content(
        model=LONG_CONTEXT_MODEL,
        contents=prompt_end
    )
    print(f"Result: {response_end.text.splitlines()[-1]}")

    print("\n--- Positional Bias Conclusion ---")
    print("Gemini models are highly capable of retrieval across the entire context.")
    print("However, placing the query/question (the final instruction) at the end, after all context, is the official recommendation for best performance and lowest latency.")


# --- Execution Block ---
if __name__ == "__main__":
    run_long_form_synthesis()
    run_many_shot_extraction()
    run_context_caching_challenge()
    run_positional_bias_test()

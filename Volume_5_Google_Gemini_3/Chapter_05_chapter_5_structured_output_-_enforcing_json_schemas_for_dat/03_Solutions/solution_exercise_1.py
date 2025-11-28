
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
import json
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

# --- Configuration ---
# Initialize the Gemini client. Ensure your GEMINI_API_KEY is available in the environment.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Google GenAI Client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set.")
    exit()

MODEL_NAME = "gemini-2.5-flash"

# ====================================================================
# EXERCISE 1: Advanced Data Extraction - Parsing a Complex Purchase Order
# ====================================================================

# 1. Define the nested schema for a line item
class LineItem(BaseModel):
    """Represents a single item in the purchase order."""
    item_name: str = Field(description="The name of the product purchased.")
    quantity: int = Field(description="The number of units ordered (must be an integer).")
    unit_price: float = Field(description="The price per unit (must be a floating-point number).")

# 2. Define the root schema for the purchase order
class PurchaseOrder(BaseModel):
    """The complete structured data for a purchase order."""
    vendor_name: str = Field(description="The name of the vendor (e.g., Acme Hardware).")
    order_date: str = Field(
        description="The date of the order, formatted strictly as YYYY-MM-DD."
    )
    line_items: List[LineItem] = Field(description="A list of all items ordered.")

print("--- Exercise 1: Purchase Order Extraction ---")

prompt_e1 = """
This confirms Purchase Order #4592 for Acme Hardware, dated 2024-11-15.
We are ordering 15 units of the 'Heavy Duty Wrench Set' at a price of 45.99 USD each.
Additionally, please include 200 units of 'Standard Bolt Kit' priced at 1.50 USD per kit.
The total order value is not required in the output.
"""

# Generate content with structured output configuration
response_e1 = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt_e1,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": PurchaseOrder.model_json_schema(),
    },
)

# Validate and parse the JSON string into the Pydantic object
order_data = PurchaseOrder.model_validate_json(response_e1.text)

print(f"Extracted Order Data (Vendor: {order_data.vendor_name}):")
print(json.dumps(order_data.model_dump(), indent=4))
print("-" * 50)


# ====================================================================
# EXERCISE 2: Conditional Output using Union and Literal
# ====================================================================

# 1. Define schema for a Bug Report
class BugReport(BaseModel):
    """Details specific to a software bug report."""
    type: Literal["BugReport"] = "BugReport"
    severity: Literal["critical", "major", "minor"] = Field(description="The impact level of the bug.")
    steps_to_reproduce: List[str] = Field(description="A sequential list of steps required to see the bug.")

# 2. Define schema for a Feature Request
class FeatureRequest(BaseModel):
    """Details specific to a new feature suggestion."""
    type: Literal["FeatureRequest"] = "FeatureRequest"
    priority: Literal["high", "medium", "low"] = Field(description="The suggested priority for implementation.")
    business_impact: str = Field(description="A description of the value this feature brings.")

# 3. Define the root schema using Union
class FeedbackClassification(BaseModel):
    """The root model that holds either a BugReport or a FeatureRequest."""
    # The model will choose which schema to follow based on the prompt content
    details: Union[BugReport, FeatureRequest]

print("--- Exercise 2: Conditional Classification (Test 1: Bug Report) ---")

prompt_e2_bug = """
Please classify the following customer feedback:
'When I click the 'Save' button, the application crashes entirely and I lose all my work.
This happens every time I try to save. This is a high priority issue for me.'
"""

response_e2_bug = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt_e2_bug,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": FeedbackClassification.model_json_schema(),
    },
)

bug_result = FeedbackClassification.model_validate_json(response_e2_bug.text)
print(f"Extracted Classification Type: {bug_result.details.type}")
print(json.dumps(bug_result.model_dump(), indent=4))
print("-" * 50)

print("--- Exercise 2: Conditional Classification (Test 2: Feature Request) ---")

prompt_e2_feature = """
Please classify the following customer feedback:
'I would really appreciate it if you added a dark mode theme to the application.
It would make late-night work much easier on the eyes. This is a nice-to-have feature.'
"""

response_e2_feature = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt_e2_feature,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": FeedbackClassification.model_json_schema(),
    },
)

feature_result = FeedbackClassification.model_validate_json(response_e2_feature.text)
print(f"Extracted Classification Type: {feature_result.details.type}")
print(json.dumps(feature_result.model_dump(), indent=4))
print("-" * 50)


# ====================================================================
# EXERCISE 3: Recursive Data Structure for Organizational Mapping
# ====================================================================

# 1. Define the recursive schema using a string forward reference
class Consultant(BaseModel):
    """Represents an employee in an organization with recursive reporting structure."""
    name: str = Field(description="The full name of the consultant.")
    role: str = Field(description="The job title of the consultant.")
    direct_reports: List["Consultant"] = Field(
        default_factory=list,
        description="A list of consultants who report directly to this person."
    )

# Required for Pydantic to resolve the forward reference "Consultant" within the List
Consultant.model_rebuild()

print("--- Exercise 3: Organizational Chart (Recursive Structure) ---")

prompt_e3 = """
Generate an organization chart for a small consulting firm.
The firm is led by CEO Sarah Connor. She directly manages two VPs: John Smith (VP of Strategy) and Jane Doe (VP of Operations).
John manages two senior analysts: Alex Chen and Ben Wyatt.
Jane manages one team lead, Chris Evans, who in turn manages intern Emily White.
Create the full organizational chart starting with Sarah.
Assign appropriate roles based on the context.
"""

response_e3 = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt_e3,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Consultant.model_json_schema(),
    },
)

org_chart = Consultant.model_validate_json(response_e3.text)
print(f"Extracted Org Chart (Root: {org_chart.name}, Role: {org_chart.role}):")
print(json.dumps(org_chart.model_dump(), indent=4))
print("-" * 50)


# ====================================================================
# EXERCISE 4: Combining Structured Output with Streaming
# ====================================================================

# 1. Define the schema for the technical summary
class TechnicalSummary(BaseModel):
    """A structured summary of a technical document."""
    document_id: str = Field(description="The unique identifier of the document.")
    key_metrics: List[str] = Field(description="A list of 3-5 critical numerical findings or metrics.")
    abstract_summary: str = Field(description="A long, detailed, multi-paragraph abstract covering core findings.")

print("--- Exercise 4: Streaming Structured Output ---")

prompt_e4 = """
Analyze the provided 500-page report on 'Quantum Computing and Financial Modeling'.
The document identifier is QC-FM-2025-A.
Extract the three most critical key metrics, such as 'Entanglement stability reached 99.99%',
'Latency reduced by 400ms', and 'Error correction rate improved by 15%'.
Then, provide a very detailed, multi-paragraph abstract summary covering the core findings,
methodology, and future outlook of the report. This summary should be several sentences long
to ensure streaming occurs.
"""

# Use generate_content_stream for streaming structured output
response_stream = client.models.generate_content_stream(
    model=MODEL_NAME,
    contents=prompt_e4,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": TechnicalSummary.model_json_schema(),
    },
)

# 2. Collect and print streamed chunks
print("Streaming JSON Chunks (Partial output):")
full_json_string = ""
for chunk in response_stream:
    # Ensure chunk has content before trying to access parts[0].text
    if chunk.candidates and chunk.candidates[0].content.parts:
        chunk_text = chunk.candidates[0].content.parts[0].text
        print(f"Chunk Received: {chunk_text}")
        full_json_string += chunk_text

# 3. Final validation and parsing
print("\n--- Stream Complete. Validating Full JSON String ---")
try:
    final_summary = TechnicalSummary.model_validate_json(full_json_string)
    print(f"Successfully validated Pydantic object for Document ID: {final_summary.document_id}")
    
    # Displaying only the start of the summary for brevity
    snippet_length = min(len(final_summary.abstract_summary), 200)
    print("Abstract Summary Snippet:")
    print(final_summary.abstract_summary[:snippet_length] + ("..." if len(final_summary.abstract_summary) > snippet_length else ""))

except Exception as e:
    print(f"Error validating final JSON: {e}")
    print(f"Received JSON String:\n{full_json_string}")

print("-" * 50)

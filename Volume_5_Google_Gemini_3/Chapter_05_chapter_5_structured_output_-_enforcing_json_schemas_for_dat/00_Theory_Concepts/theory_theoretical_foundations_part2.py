
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

# Source File: theory_theoretical_foundations_part2.py
# Description: Theoretical Foundations
# ==========================================

import os
import json
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Union, Literal

# --- 1. Client Initialization ---
# Ensure your GEMINI_API_KEY is set in your environment variables
# client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
# For demonstration purposes, we assume the client is initialized correctly
# In a real scenario, this would require a valid API key.
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Could not initialize Gemini client. API key might be missing or invalid. {e}")
    # Create a mock client for demonstration if the real one fails
    class MockClient:
        def models(self):
            class MockModels:
                def generate_content(self, model, contents, config):
                    # Mock response based on the Recipe schema
                    if "Recipe" in str(config.get("response_json_schema")):
                        mock_text = """
                        {
                          "recipe_name": "Mock Chocolate Chip Cookies",
                          "prep_time_minutes": 15,
                          "ingredients": [
                            {
                              "name": "flour",
                              "quantity": "2 cups"
                            },
                            {
                              "name": "sugar",
                              "quantity": "1 cup"
                            }
                          ],
                          "instructions": [
                            "Mix dry ingredients.",
                            "Bake at 350F."
                          ]
                        }
                        """
                    # Mock response based on the Moderation schema
                    elif "ModerationResult" in str(config.get("response_json_schema")):
                        mock_text = """
                        {
                          "decision": {
                            "reason": "The content is safe.",
                            "summary": "A positive review about a product.",
                            "is_safe": true
                          }
                        }
                        """
                    # Mock response based on the Employee (Recursive) schema
                    elif "Employee" in str(config.get("response_json_schema")):
                        mock_text = """
                        {
                          "name": "Alice",
                          "employee_id": 101,
                          "reports": [
                            {
                              "name": "Bob",
                              "employee_id": 102,
                              "reports": []
                            }
                          ]
                        }
                        """
                    else:
                        mock_text = "{}"
                    
                    class MockResponse:
                        def __init__(self, text):
                            self.text = text
                    return MockResponse(mock_text)
            return MockModels()
    client = MockClient()
    print("Using MockClient for structured output demonstration.")


# --- 2. Example 1: Nested and List Structures (Recipe Extractor) ---
# This demonstrates how to handle arrays (List) and nested objects.

class Ingredient(BaseModel):
    """Defines a single ingredient for a recipe."""
    name: str = Field(description="The common name of the ingredient (e.g., 'all-purpose flour').")
    quantity: str = Field(description="The precise quantity of the ingredient, including units (e.g., '2 and 1/4 cups').")

class Recipe(BaseModel):
    """The main schema for extracting a complete recipe."""
    recipe_name: str = Field(description="The descriptive name of the recipe.")
    prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe. Must be an integer.")
    ingredients: List[Ingredient] = Field(description="A list of all ingredients required, each conforming to the Ingredient schema.")
    instructions: List[str] = Field(description="A sequential list of steps required to make the recipe.")

def extract_recipe_data(prompt_text: str):
    """Extracts structured recipe data using the Recipe schema."""
    print("\n--- Running Example 1: Recipe Extraction (Nested Objects) ---")
    
    # 1. Generate the JSON Schema from the Pydantic model
    recipe_schema_json = Recipe.model_json_schema()
    
    # 2. Call the Gemini API, enforcing the schema
    try:
        raw_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": recipe_schema_json,
            },
        )
        
        # 3. Validate and parse the raw JSON string into a Pydantic object
        # This step guarantees the data is now a reliable Python object.
        recipe_object = Recipe.model_validate_json(raw_response.text)
        
        print(f"Successfully extracted recipe: {recipe_object.recipe_name}")
        print(f"Preparation Time (minutes): {recipe_object.prep_time_minutes}")
        print(f"Number of Ingredients: {len(recipe_object.ingredients)}")
        print("\nFirst Instruction:")
        print(f"-> {recipe_object.instructions[0]}")
        
        # Demonstrate access to nested data
        print("\nFirst Ingredient Details:")
        first_ingredient = recipe_object.ingredients[0]
        print(f"Name: {first_ingredient.name}, Quantity: {first_ingredient.quantity}")
        
    except ValidationError as e:
        print(f"Pydantic Validation Error: The model output did not match the schema. {e}")
    except Exception as e:
        print(f"An API error occurred: {e}")

recipe_prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
The preparation time is estimated to be 15 minutes.
"""
extract_recipe_data(recipe_prompt)


# --- 3. Example 2: Conditional and Enumerated Structures (Content Moderation) ---
# This demonstrates using `Literal` (enums) and `Union` (anyOf) for complex classification.

class SpamDetails(BaseModel):
    """Details provided if the content is classified as spam."""
    reason: str = Field(description="The specific reason why the content violates policy.")
    # Literal enforces that the value must be one of these strings (JSON Schema enum)
    spam_type: Literal["phishing", "scam", "unsolicited promotion", "other"] = Field(description="The type of spam.")

class NotSpamDetails(BaseModel):
    """Details provided if the content is deemed safe."""
    summary: str = Field(description="A brief summary of the content's topic.")
    is_safe: bool = Field(description="Boolean indicating if the content is safe for all audiences.")

class ModerationResult(BaseModel):
    """The root model, using Union to allow for conditional output structures."""
    # Union translates to 'anyOf' in JSON Schema, meaning the 'decision' key
    # must match EITHER the SpamDetails OR the NotSpamDetails schema.
    decision: Union[SpamDetails, NotSpamDetails] = Field(description="The final moderation decision and its associated details.")

def moderate_content(prompt_text: str):
    """Classifies content using a conditional schema."""
    print("\n--- Running Example 2: Content Moderation (Union/AnyOf) ---")
    
    moderation_schema_json = ModerationResult.model_json_schema()
    
    try:
        raw_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": moderation_schema_json,
            },
        )
        
        result_object = ModerationResult.model_validate_json(raw_response.text)
        
        print("Moderation Complete.")
        
        # We can inspect the type of the 'decision' field to see which schema was used
        decision_data = result_object.decision
        
        if isinstance(decision_data, SpamDetails):
            print(f"Classification: SPAM ({decision_data.spam_type})")
            print(f"Reason: {decision_data.reason}")
        elif isinstance(decision_data, NotSpamDetails):
            print(f"Classification: SAFE")
            print(f"Summary: {decision_data.summary}")
            print(f"Is Safe: {decision_data.is_safe}")
        else:
            print("Unknown decision type returned.")
            
    except ValidationError as e:
        print(f"Pydantic Validation Error: {e}")
    except Exception as e:
        print(f"An API error occurred: {e}")

moderation_prompt = """
Please moderate the following content and provide a decision.
Content: 'This product review is amazing! The UI is incredibly intuitive and visually appealing. Great job.'
"""
moderate_content(moderation_prompt)


# --- 4. Example 3: Recursive Structures (Organization Chart) ---
# This demonstrates how a Pydantic model can reference itself, creating deep, nested structures.

class Employee(BaseModel):
    """Represents an employee in an organization, potentially managing others."""
    # Note: Forward referencing requires the model to be defined as a string ("Employee")
    # Pydantic handles the resolution automatically.
    name: str = Field(description="The full name of the employee.")
    employee_id: int = Field(description="A unique numeric identifier for the employee.")
    reports: List["Employee"] = Field(
        default_factory=list,
        description="A list of employees who report directly to this employee. This list is recursive."
    )

# Pydantic requires updating the forward references for recursive models
Employee.model_rebuild()

def generate_org_chart(prompt_text: str):
    """Generates a recursive organization chart."""
    print("\n--- Running Example 3: Organization Chart (Recursive Schema) ---")
    
    org_chart_schema_json = Employee.model_json_schema()
    
    try:
        raw_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": org_chart_schema_json,
            },
        )
        
        org_chart_object = Employee.model_validate_json(raw_response.text)
        
        print(f"Root Manager: {org_chart_object.name} (ID: {org_chart_object.employee_id})")
        
        # Helper function to print the structure recursively
        def print_reports(employee: Employee, level=0):
            indent = "  " * level
            for report in employee.reports:
                print(f"{indent}- Report: {report.name} (ID: {report.employee_id})")
                if report.reports:
                    print_reports(report, level + 1)

        print("--- Reporting Structure ---")
        print_reports(org_chart_object)
        
    except ValidationError as e:
        print(f"Pydantic Validation Error: {e}")
    except Exception as e:
        print(f"An API error occurred: {e}")

org_chart_prompt = """
Generate an organization chart for a small team.
The manager is Alice, who manages Bob and Charlie. Bob manages David.
Assign unique employee IDs starting from 101.
"""
generate_org_chart(org_chart_prompt)


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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

def exercise_2_sequential_chain(llm: ChatOpenAI):
    """
    Implements a two-stage analysis pipeline using SequentialChain.
    """
    if not llm:
        print("LLM not initialized. Skipping Exercise 2.")
        return

    print("\n--- EXERCISE 2: Sequential Chains ---")
    
    report_text = (
        "The Q3 report highlights significant risks. Firstly, our reliance on a single "
        "supplier in Southeast Asia poses a major supply chain disruption risk. "
        "Secondly, new environmental regulations in Europe will increase compliance "
        "costs by 15% next year. Finally, the company's debt-to-equity ratio has "
        "risen to 2.5, which limits future capital investment flexibility."
    )
    
    # Stage 1 Chain: Analysis (Input: report_text, Output: summary_of_risks)
    summary_prompt = PromptTemplate(
        template="Analyze the following financial report text and summarize the three primary risks mentioned:\n\n{report_text}",
        input_variables=["report_text"]
    )
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary_of_risks")
    
    # Stage 2 Chain: Critique (Input: summary_of_risks, Output: final_recommendation)
    recommendation_prompt = PromptTemplate(
        template="Based ONLY on the following summary of risks, provide a high-level recommendation (Hold, Buy, or Investigate Further) and a brief justification:\n\nRisks Summary: {summary_of_risks}",
        input_variables=["summary_of_risks"]
    )
    recommendation_chain = LLMChain(llm=llm, prompt=recommendation_prompt, output_key="final_recommendation")
    
    # Orchestration: Sequential Chain
    overall_chain = SequentialChain(
        chains=[summary_chain, recommendation_chain],
        input_variables=["report_text"],
        output_variables=["summary_of_risks", "final_recommendation"],
        verbose=False
    )
    
    print("--- Running Analysis Pipeline ---")
    result = overall_chain.invoke({"report_text": report_text})
    
    print("\n[Input Text Snippet]:", report_text[:80] + "...")
    print("\n[Stage 1 Output - Summary of Risks]:")
    print(result["summary_of_risks"].strip())
    print("\n[Stage 2 Output - Final Recommendation]:")
    print(result["final_recommendation"].strip())

# exercise_2_sequential_chain(llm)

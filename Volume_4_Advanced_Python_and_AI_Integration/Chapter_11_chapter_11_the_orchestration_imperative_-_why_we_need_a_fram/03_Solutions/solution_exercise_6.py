
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

# Source File: solution_exercise_6.py
# Description: Solution for Exercise 6
# ==========================================

def exercise_5_custom_chain_structure(llm: ChatOpenAI):
    """
    Implements a custom orchestration wrapper for conditional chain execution 
    based on a validation check.
    """
    if not llm:
        print("LLM not initialized. Skipping Exercise 5.")
        return

    print("\n--- EXERCISE 5: Custom Chain Structure and Error Handling ---")

    # 1. Define Chains
    
    # Primary Title Chain
    title_template = "Generate a concise, catchy title for a technical blog post about {topic}. Title:"
    title_prompt = PromptTemplate(input_variables=["topic"], template=title_template)
    title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key="raw_title")

    # Fallback Title Chain (Used if the raw title is too short)
    fallback_template = "Generate a safe, generic, but professional title for a blog post on {topic}. Title:"
    fallback_prompt = PromptTemplate(input_variables=["topic"], template=fallback_template)
    fallback_title_chain = LLMChain(llm=llm, prompt=fallback_prompt, output_key="fallback_title")
    
    # Content Generation Chain (Requires final_title and topic)
    content_template = "Write a short, engaging 100-word introduction for a blog post titled '{final_title}' on the topic of {topic}."
    content_prompt = PromptTemplate(input_variables=["final_title", "topic"], template=content_template)
    content_chain = LLMChain(llm=llm, prompt=content_prompt, output_key="content_body")

    # 3. Custom Orchestration Function
    def conditional_orchestrator(topic: str) -> Dict[str, Any]:
        """Runs the title chain, validates the output, and executes the content chain."""
        
        # Step 1: Execute Primary Title Chain
        title_result = title_chain.invoke({"topic": topic})
        raw_title = title_result["raw_title"].strip().strip('"')
        
        # Step 2: Validation Check (Title length)
        if len(raw_title) < 10:
            print(f"   [Validation Failed]: Title '{raw_title}' is too short ({len(raw_title)} chars). Triggering Fallback.")
            # Step 3a: Execute Fallback Chain
            fallback_result = fallback_title_chain.invoke({"topic": topic})
            final_title = fallback_result["fallback_title"].strip().strip('"')
        else:
            print(f"   [Validation Success]: Title '{raw_title}' is long enough ({len(raw_title)} chars). Proceeding.")
            final_title = raw_title
            
        # Step 4: Execute Content Chain with the selected title
        content_result = content_chain.invoke({
            "final_title": final_title,
            "topic": topic
        })
        
        return {
            "final_title": final_title,
            "content_body": content_result["content_body"]
        }

    # 4. Execution Case A: Validation Success (Long Topic -> Long Title)
    topic_a = "The complex challenges of implementing distributed ledger technology in global supply chains"
    print(f"\n--- Case A: Success (Topic: {topic_a[:50]}...) ---")
    result_a = conditional_orchestrator(topic_a)
    print(f"\nFinal Title Used: {result_a['final_title']}")
    print(f"Content Body Start: {result_a['content_body'][:150]}...")

    # 5. Execution Case B: Validation Failure (Short Topic -> Short Title)
    topic_b = "Cats"
    print(f"\n--- Case B: Failure/Fallback (Topic: {topic_b}) ---")
    result_b = conditional_orchestrator(topic_b)
    print(f"\nFinal Title Used: {result_b['final_title']}")
    print(f"Content Body Start: {result_b['content_body'][:150]}...")

# exercise_5_custom_chain_structure(llm)

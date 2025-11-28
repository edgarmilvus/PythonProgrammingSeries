
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

# 1. Tool Definition
PROJECT_CONFIGS = {
    "P101": "Project P101 is running on Python 3.10 and uses PostgreSQL.",
    "P102": "Project P102 is running on Node.js and uses MongoDB."
}

def get_project_config(project_id: str) -> str:
    """Accepts a project ID string (e.g., 'P101') and returns the full configuration details for that project."""
    config = PROJECT_CONFIGS.get(project_id.upper(), "Configuration not found for that project ID.")
    return config

config_tool = Tool.from_function(
    func=get_project_config,
    name="ProjectConfigLookup",
    description="Useful for retrieving the specific software and database configuration details for a given project ID."
)

def exercise_4_interactive_challenge(llm: ChatOpenAI):
    """
    Combines Memory and Tools in a multi-turn AgentExecutor.
    """
    if not llm:
        print("LLM not initialized. Skipping Exercise 4.")
        return

    print("\n--- EXERCISE 4: Interactive Challenge (Memory + Tools) ---")
    
    tools = [config_tool]
    
    # 2. Memory Integration
    # Using CHAT_CONVERSATIONAL_REACT_DESCRIPTION requires memory to return messages
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", 
        k=5, 
        return_messages=True,
        output_key="output" # Required for some older agent types, good practice
    )
    
    # 3. Agent Setup (CHAT_CONVERSATIONAL_REACT_DESCRIPTION is optimized for memory and tool use)
    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    
    # Turn 1 (Memory Setup)
    prompt_1 = "Hello, my project ID is P101. I need help with a deployment issue."
    print(f"\n[User 1]: {prompt_1}")
    agent_executor.invoke({"input": prompt_1})
    
    # Turn 2 (Tool + Memory Retrieval)
    prompt_2 = "What database is my project using?"
    print(f"\n[User 2]: {prompt_2}")
    agent_executor.invoke({"input": prompt_2})
    
    print("\n--- Final Memory State ---")
    # Verify that the conversation history contains the project ID setup
    print(memory.load_memory_variables({}))

# exercise_4_interactive_challenge(llm)

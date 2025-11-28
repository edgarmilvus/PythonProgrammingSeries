
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

# Source File: theory_theoretical_foundations_part5.py
# Description: Theoretical Foundations
# ==========================================

class CapabilityAwareRouter:
    """
    Production-grade router that automatically selects the optimal model
    based on measured capability thresholds.
    """
    
    def __init__(self, capability_threshold: int = 60):
        self.threshold = capability_threshold
        self.client = genai.Client()
        
        # Cost factors (relative, for decision-making)
        self.FLASH_COST = 1.0
        self.PRO_COST = 10.0
        
    def estimate_complexity(self, prompt: str) -> int:
        """
        Estimates the complexity of a prompt.
        
        In production, use:
        - Prompt length (longer = more complex)
        - Keyword analysis (legal terms, technical jargon)
        - A separate classifier model trained on labeled data
        """
        # Simple heuristic: length-based complexity
        word_count = len(prompt.split())
        
        if word_count < 50:
            return 20  # Simple
        elif word_count < 200:
            return 50  # Moderate
        elif word_count < 500:
            return 70  # Complex
        else:
            return 90  # Expert-level
    
    def route_request(self, prompt: str, user_tier: str = "standard") -> str:
        """
        Routes the request to the optimal model based on complexity and user tier.
        """
        complexity = self.estimate_complexity(prompt)
        
        print(f"\n[Router] Estimated Complexity: {complexity}")
        print(f"[Router] Capability Threshold: {self.threshold}")
        
        # Business logic: Premium users always get Pro
        if user_tier == "premium":
            print("[Router] Decision: PRO (Premium tier)")
            return "gemini-2.5-pro"
        
        # For standard users, check if complexity exceeds threshold
        if complexity >= self.threshold:
            print(f"[Router] Decision: PRO (Complexity {complexity} >= Threshold {self.threshold})")
            return "gemini-2.5-pro"
        else:
            print(f"[Router] Decision: FLASH (Complexity {complexity} < Threshold {self.threshold})")
            return "gemini-2.5-flash"
    
    def execute_request(self, prompt: str, user_tier: str = "standard") -> str:
        """
        Full pipeline: route, execute, return.
        """
        model = self.route_request(prompt, user_tier)
        
        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )
        
        return response.text

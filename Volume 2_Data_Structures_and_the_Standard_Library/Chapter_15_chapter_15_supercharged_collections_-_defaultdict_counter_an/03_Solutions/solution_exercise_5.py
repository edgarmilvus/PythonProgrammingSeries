
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

from collections import deque

def find_longest_word_chain(start_word, potential_words):
    """
    Uses BFS with a deque to find the longest valid word chain.
    """
    # Use a set for O(1) membership checking and removal efficiency
    potential_words_set = set(potential_words)
    
    # Ensure the start word is not included in the pool of remaining words
    if start_word in potential_words_set:
        potential_words_set.remove(start_word)

    # Queue stores tuples: (last_word_used, current_chain_list, remaining_words_set)
    queue = deque([
        (start_word, [start_word], potential_words_set)
    ])

    longest_chain = [start_word]
    max_length = 1

    while queue:
        # Pop the oldest chain state (BFS structure)
        last_word, current_chain, remaining_words = queue.popleft()
        
        # Determine the required starting letter (case-insensitive)
        required_start_char = last_word[-1].lower()

        # Iterate through the remaining words to find valid successors
        # Iterate over a list copy to avoid modifying the set during iteration
        for next_word in list(remaining_words):
            if next_word[0].lower() == required_start_char:
                
                # 1. Create the new chain list
                new_chain = current_chain + [next_word]
                
                # 2. Create the new set of remaining words (removing the word just used)
                new_remaining_words = remaining_words.copy()
                new_remaining_words.remove(next_word)
                
                # 3. Add the new state to the queue for further exploration
                queue.append((next_word, new_chain, new_remaining_words))

                # 4. Track the longest chain found
                if len(new_chain) > max_length:
                    max_length = len(new_chain)
                    longest_chain = new_chain
                    
    return longest_chain

# Simulated Input:
start_word = "Python"
potential_words = {"Network", "Programming", "Ninja", "Octopus", "Rope", "Noodle", "Hat"}

# Execute the function
longest_result = find_longest_word_chain(start_word, potential_words)

print("--- Exercise 5: Word Chain Validator (deque for BFS) ---")
print(f"Starting Word: {start_word}")
print(f"Potential Words: {potential_words}")
print(f"\nLongest Valid Word Chain Found (Length {len(longest_result)}):")
print(" -> ".join(longest_result))

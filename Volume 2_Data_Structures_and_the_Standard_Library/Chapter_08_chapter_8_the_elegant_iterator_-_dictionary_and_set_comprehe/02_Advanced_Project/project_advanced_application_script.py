
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import random
from collections import defaultdict, Counter

# --- 1. Simulated Input Data ---
# Structure: List of dictionaries representing individual feedback submissions.
RAW_FEEDBACK_DATA = [
    {"id": 101, "region": "North", "text": "The service was quick and effective, truly excellent."},
    {"id": 102, "region": "South", "text": "The product is slow and frustrating. Needs major fixes."},
    {"id": 103, "region": "East", "text": "It was fine, neither great nor terrible."},
    {"id": 104, "region": "North", "text": "I found the interface confusing and complex, a real disaster."},
    {"id": 105, "region": "West", "text": "Absolutely fantastic! Quick delivery and superb quality."},
    {"id": 106, "region": "South", "text": "The support team was helpful, but the core issue remains unsolved."},
    {"id": 107, "region": "East", "text": "Excellent features, but the price is too high."},
    {"id": 108, "region": "West", "text": "Frustrating experience, slow loading times."},
    {"id": 109, "region": "North", "text": "The app is quick, but the design is confusing."},
    {"id": 110, "region": "South", "text": "Superb support, fixed my slow issue immediately."},
]

# --- 2. Defining Sentiment Weights (Foundation for Comprehension) ---
# Base mapping: Keywords mapped to their corresponding sentiment scores.
BASE_SENTIMENT_MAP = {
    "excellent": 3, "fantastic": 3, "superb": 2, "quick": 1, "helpful": 1,
    "slow": -2, "frustrating": -3, "confusing": -2, "complex": -1, "disaster": -3,
    "high": -1, # Negative context for price
}

# Dictionary Comprehension: Normalize the map keys to ensure case-insensitivity.
SENTIMENT_MAP = {
    word.lower(): score for word, score in BASE_SENTIMENT_MAP.items()
}

# --- 3. Core Processing Logic ---

def analyze_response(text: str) -> tuple[int, set]:
    """Calculates total sentiment score and extracts relevant keywords."""
    # Simple tokenization and normalization
    words = text.lower().replace(",", "").replace(".", "").split()
    score = 0
    found_keywords = set()
    
    for word in words:
        if word in SENTIMENT_MAP:
            score += SENTIMENT_MAP[word]
            found_keywords.add(word)
            
    return score, found_keywords

# --- 4. Application of Comprehensions ---

MIN_SENTIMENT_THRESHOLD = 3  # Focus only on feedback with strong sentiment magnitude (>= 3 or <= -3)

# A. Dictionary Comprehension: Filtered and Scored Responses
# Creates a dictionary mapping {Response ID: Score} for only those responses
# whose score magnitude meets the defined threshold. Uses the walrus operator (:=) for efficiency.
CRITICAL_SCORES_BY_ID = {
    item['id']: score
    for item in RAW_FEEDBACK_DATA
    if (score := analyze_response(item['text'])[0]) and abs(score) >= MIN_SENTIMENT_THRESHOLD
}

# B. Set Comprehension: Unique Critical Keywords
# Gathers ALL unique keywords mentioned across the ENTIRE dataset, ensuring no duplicates.
ALL_UNIQUE_KEYWORDS = {
    keyword
    for item in RAW_FEEDBACK_DATA
    for keyword in analyze_response(item['text'])[1]
}

# C. Dictionary Comprehension: Regional Aggregation (Post-Processing)
# 1. Preparation: Group scores by region using defaultdict (standard accumulation)
regional_groupings = defaultdict(lambda: {'total_score': 0, 'count': 0})

# Iterate only over the filtered critical scores
for item in RAW_FEEDBACK_DATA:
    response_id = item['id']
    if response_id in CRITICAL_SCORES_BY_ID:
        score = CRITICAL_SCORES_BY_ID[response_id]
        region = item['region']
        
        regional_groupings[region]['total_score'] += score
        regional_groupings[region]['count'] += 1

# 2. Final Dictionary Comprehension: Calculate Averages
# Maps {Region: Average Sentiment Score}
REGIONAL_AVERAGE_SENTIMENT = {
    region: data['total_score'] / data['count']
    for region, data in regional_groupings.items()
    if data['count'] > 0
}

# D. Bonus Set/List Comprehension & Counter (Frequency Analysis)
# 1. List Comprehension: Flattens all extracted keywords into a single iterable list.
all_keywords_list = [
    keyword
    for item in RAW_FEEDBACK_DATA
    for keyword in analyze_response(item['text'])[1]
]

# 2. Use the specialized Counter class (defined in the glossary)
KEYWORD_FREQUENCY = Counter(all_keywords_list)

# --- 5. Output Results ---

print("--- Comprehensive Feedback Analysis Report ---")
print(f"\nProcessing {len(RAW_FEEDBACK_DATA)} total responses.")
print(f"Minimum Sentiment Threshold (Magnitude): {MIN_SENTIMENT_THRESHOLD}")

print("\n[A] Critical Responses (ID: Score) - Filtered using Dict Comp:")
if CRITICAL_SCORES_BY_ID:
    for rid, score in CRITICAL_SCORES_BY_ID.items():
        print(f"  ID {rid}: Score {score}")
else:
    print("  No responses met the critical threshold.")

print("\n[B] All Unique Critical Keywords - Generated using Set Comp:")
print(f"  Total unique keywords found: {len(ALL_UNIQUE_KEYWORDS)}")
print(f"  Keywords: {sorted(list(ALL_UNIQUE_KEYWORDS))}")

print("\n[C] Regional Average Sentiment (Based on Critical Responses) - Calculated using Dict Comp:")
for region, avg in REGIONAL_AVERAGE_SENTIMENT.items():
    print(f"  {region}: {avg:.2f}")

print("\n[D] Top 5 Most Frequent Keywords (Overall):")
for word, count in KEYWORD_FREQUENCY.most_common(5):
    print(f"  '{word}': {count} mentions")

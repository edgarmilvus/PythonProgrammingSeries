
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

import asyncio
import aiohttp
import time
import random
from typing import List, Dict, Any

# --- Configuration ---
TICKERS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
BASE_URL = "http://api.simulated-finance.com/"

# --- Helper Coroutines for Simulation ---

async def _simulate_network_delay(endpoint: str, ticker: str) -> float:
    """
    Simulates variable network latency for an API call.
    The time spent here is the time the event loop yields control.
    """
    delay = random.uniform(0.5, 2.0)
    print(f"[{ticker} | {endpoint}] Starting request. Expected delay: {delay:.2f}s")
    
    # CRITICAL: await yields control back to the event loop.
    await asyncio.sleep(delay)
    
    print(f"[{ticker} | {endpoint}] Request completed.")
    return delay

async def fetch_price(session: aiohttp.ClientSession, ticker: str) -> Dict[str, Any]:
    """
    Coroutine to fetch the current stock price.
    In a real application, 'session.get(url)' would be used.
    """
    delay = await _simulate_network_delay("Price", ticker)
    
    # Simulate data return
    price = round(random.uniform(100, 1000), 2)
    return {"ticker": ticker, "type": "Price", "value": price, "latency": delay}

async def fetch_sentiment(session: aiohttp.ClientSession, ticker: str) -> Dict[str, Any]:
    """
    Coroutine to fetch the news sentiment score.
    """
    delay = await _simulate_network_delay("Sentiment", ticker)
    
    # Simulate data return
    sentiment_score = random.randint(-100, 100)
    sentiment_status = "Positive" if sentiment_score > 10 else "Negative/Neutral"
    return {"ticker": ticker, "type": "Sentiment", "score": sentiment_score, 
            "status": sentiment_status, "latency": delay}

# --- Orchestration Coroutine ---

async def fetch_ticker_data(session: aiohttp.ClientSession, ticker: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Fetches all required data (Price and Sentiment) for a single ticker concurrently.
    This demonstrates nested concurrent execution using asyncio.gather().
    """
    print(f"\n--- Launching concurrent fetches for {ticker} ---")
    
    # CRITICAL: asyncio.gather runs both coroutines simultaneously.
    # The current coroutine (fetch_ticker_data) pauses until BOTH sub-coroutines complete.
    results = await asyncio.gather(
        fetch_price(session, ticker),
        fetch_sentiment(session, ticker)
    )
    
    print(f"--- All data collected for {ticker} ---")
    return {ticker: results}

# --- Main Entry Point ---

async def main():
    """
    The main asynchronous function that orchestrates all ticker fetching tasks.
    """
    start_time = time.time()
    
    # Use aiohttp.ClientSession for efficient resource management and connection pooling.
    # The 'async with' statement ensures the session is closed correctly.
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        
        # 1. Create a list of awaitable coroutines, one for each ticker.
        tasks = [fetch_ticker_data(session, ticker) for ticker in TICKERS]
        
        # 2. CRITICAL: Use asyncio.gather to run ALL ticker tasks concurrently.
        # The 'main' coroutine awaits the completion of the entire set of tasks.
        all_results = await asyncio.gather(*tasks)
        
    end_time = time.time()
    
    # Final data processing and summary
    total_time = end_time - start_time
    print("\n" + "="*50)
    print("CONCURRENT DATA AGGREGATION COMPLETE")
    print(f"Total Tickers Processed: {len(TICKERS)}")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    
    # A quick calculation to show the benefit:
    # If the max delay is 2.0s, sequential processing (5 tickers * 2 tasks/ticker * 2.0s max) 
    # would take ~20 seconds. Concurrent processing takes only ~2.0 seconds (the max single delay).
    print("="*50)
    
    # Optional: Print aggregated results
    # for result_set in all_results:
    #     print(result_set)

if __name__ == "__main__":
    # The standard synchronous entry point to start the asynchronous event loop.
    # This call blocks until the 'main()' coroutine and all its spawned tasks are complete.
    asyncio.run(main())

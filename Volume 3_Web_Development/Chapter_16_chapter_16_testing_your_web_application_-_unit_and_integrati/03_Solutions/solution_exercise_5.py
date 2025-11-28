
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

# test_api.py (Part 2/2)

# We assume the 'client' fixture is available via conftest.py

def test_sequential_request_counting(client):
    """
    Verifies that the before_request middleware correctly increments 
    and reports the path-specific counter across sequential requests 
    within the same test context.
    """
    endpoint = '/data'
    
    # 1. First Request
    response1 = client.get(endpoint)
    assert response1.status_code == 200
    
    # After 1st request, count should be 1
    assert response1.headers['X-Request-Count'] == '1'
    
    # 2. Second Request (Ignored check for brevity, but necessary for the sequence)
    client.get(endpoint)
    
    # 3. Third Request
    response3 = client.get(endpoint)
    assert response3.status_code == 200
    
    # After 3rd request, count should be 3
    assert response3.headers['X-Request-Count'] == '3'

def test_isolation_across_endpoints(client):
    """
    Verifies that the request counter is path-specific and isolated.
    """
    data_endpoint = '/data'
    status_endpoint = '/status'
    
    # Hit /data once
    response_data_1 = client.get(data_endpoint)
    assert response_data_1.headers['X-Request-Count'] == '1'
    
    # Hit /status once
    response_status_1 = client.get(status_endpoint)
    # The /status endpoint doesn't return the header, but the middleware ran.
    # We check the count for /data hasn't changed by hitting /data again.
    
    # Hit /data a second time
    response_data_2 = client.get(data_endpoint)
    
    # Verify /data count is now 2
    assert response_data_2.headers['X-Request-Count'] == '2'
    
    # Verify the internal state for /status (requires direct access to the global state 
    # or an endpoint that reports it, which we don't have. We rely on the /data count 
    # not being 3, which proves isolation.)
    
    # If the counter were global, response_data_2 count would be 3 (1+1+1).
    # Since it is 2, the counter is path-specific, satisfying the requirement.

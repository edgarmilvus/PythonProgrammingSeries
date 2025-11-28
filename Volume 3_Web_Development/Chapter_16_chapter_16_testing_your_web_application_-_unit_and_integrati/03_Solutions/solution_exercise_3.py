
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

# test_api.py (Part 1/2)

# We assume the 'client' fixture is available via conftest.py

def test_public_endpoint_access(client):
    """Verifies that the /public endpoint is accessible and returns expected content."""
    response = client.get('/public')
    
    # Requirement 1: Status code check
    assert response.status_code == 200
    
    # Requirement 2: Content check
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'Welcome to the public area' in data['message']

def test_admin_endpoint_unauthorized(client):
    """Verifies that accessing /admin without a key returns 401 Unauthorized."""
    response = client.get('/admin')
    
    # Requirement 3: Unauthorized status check
    assert response.status_code == 401
    
    data = response.get_json()
    assert data['error'] == 'Unauthorized access'

def test_admin_endpoint_authorized(client):
    """Verifies that accessing /admin with the correct key returns 200 OK."""
    admin_key = 'secret-admin-key'
    headers = {'X-API-KEY': admin_key}
    
    response = client.get('/admin', headers=headers)
    
    # Requirement 4: Authorized status check
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['message'] == 'Admin access granted'

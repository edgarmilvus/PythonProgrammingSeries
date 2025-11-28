
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

# Configuration data structure provided in the problem description
config_data = {
    "application_name": "DataProcessor",
    "version": "1.2.0",
    "environments": {
        "dev": {
            "databases": [
                {"type": "PostgreSQL", "host": "192.168.1.10", "port": 5432},
                {"type": "Redis", "host": "192.168.1.11", "port": 6379}
            ],
            "servers": [
                {"name": "web_dev_01", "ip": "10.0.0.1", "port": 8080},
                {"name": "api_dev_01", "ip": "10.0.0.2", "port": 8081}
            ]
        },
        "prod": {
            "databases": [
                {"type": "PostgreSQL", "host": "172.16.0.50", "port": 5432}
            ],
            "servers": [
                {"name": "web_prod_01", "ip": "10.1.0.1", "port": 8000},
                {"name": "web_prod_02", "ip": "10.1.0.2", "port": 8000},
                {"name": "api_prod_01", "ip": "10.1.0.3", "port": 8001}
            ]
        }
    }
}

def extract_all_ports(config_data: dict, environment_name: str) -> list[int]:
    """
    Requirement 1: Extracts all server and database ports for a given environment.
    Handles non-existent environments gracefully.
    """
    # Use .get() defensively to prevent KeyError if 'environments' or the specific environment is missing
    env_data = config_data.get('environments', {}).get(environment_name)
    
    if not env_data:
        return []

    all_ports = []

    # Iterate over the list of server dictionaries
    for server in env_data.get('servers', []):
        all_ports.append(server.get('port'))

    # Iterate over the list of database dictionaries
    for db in env_data.get('databases', []):
        all_ports.append(db.get('port'))
        
    return all_ports


def summarize_environment(config_data: dict, environment_name: str) -> tuple:
    """
    Requirement 2: Returns a tuple summarizing server and database counts.
    (environment_name, number_of_servers, number_of_databases)
    """
    env_data = config_data.get('environments', {}).get(environment_name)
    
    if not env_data:
        return (environment_name, 0, 0)
    
    # Use len() on the lists retrieved via .get() (defaulting to empty list if key is missing)
    num_servers = len(env_data.get('servers', []))
    num_databases = len(env_data.get('databases', []))
    
    return (environment_name, num_servers, num_databases)


def find_database_by_host(config_data: dict, environment_name: str, host_ip: str) -> str | None:
    """
    Requirement 3: Searches for a database by its host IP and returns its type.
    Returns None if the environment or host is not found.
    """
    env_data = config_data.get('environments', {}).get(environment_name)
    
    if not env_data:
        return None
    
    # Iterate through the list of database dictionaries
    for db in env_data.get('databases', []):
        if db.get('host') == host_ip:
            return db.get('type')
            
    return None

# --- Testing 20.4.4 ---
print("\n--- Configuration Analysis Test ---")

# Test 1: Port Extraction
dev_ports = extract_all_ports(config_data, 'dev')
prod_ports = extract_all_ports(config_data, 'prod')
print(f"Dev Environment Ports: {dev_ports}")
print(f"Prod Environment Ports: {prod_ports}")

# Test 2: Summarization
dev_summary = summarize_environment(config_data, 'dev')
prod_summary = summarize_environment(config_data, 'prod')
missing_summary = summarize_environment(config_data, 'test')
print(f"\nDev Summary: {dev_summary}")
print(f"Prod Summary: {prod_summary}")
print(f"Missing Summary: {missing_summary}")

# Test 3: Host Lookup
db_type_found = find_database_by_host(config_data, 'prod', '172.16.0.50')
db_type_missing = find_database_by_host(config_data, 'dev', '192.168.1.99')
print(f"\nDatabase type at 172.16.0.50 (prod): {db_type_found}")
print(f"Database type at 192.168.1.99 (dev): {db_type_missing}")

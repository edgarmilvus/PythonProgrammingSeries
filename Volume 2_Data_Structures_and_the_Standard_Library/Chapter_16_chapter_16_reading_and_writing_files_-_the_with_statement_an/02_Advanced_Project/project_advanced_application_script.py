
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
import datetime
import sys

# --- Configuration ---
LOG_FILE = "server_access.log"
REPORT_FILE = "analysis_summary.txt"
MOCK_ENTRIES = 150

def generate_mock_log(filename: str, entries: int):
    """
    Generates a mock server access log file for demonstration purposes.
    Uses the 'w' mode and ensures the file is closed via 'with'.
    """
    ip_prefixes = ["192.168.1.", "10.0.0.", "66.249.79."]
    status_codes = [200, 200, 200, 200, 404, 404, 500, 301]
    resources = ["/index.html", "/api/data", "/images/logo.png", "/admin/login", "/404_test"]
    
    print(f"Generating {entries} mock log entries...")
    
    # CRITICAL: Use 'with' for safe file writing (mode 'w')
    with open(filename, 'w') as f:
        for _ in range(entries):
            ip = random.choice(ip_prefixes) + str(random.randint(1, 254))
            status = random.choice(status_codes)
            resource = random.choice(resources)
            timestamp = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60))
            
            # Format the log line (simplified common log format)
            log_line = (
                f"{ip} - - [{timestamp.strftime('%d/%b/%Y:%H:%M:%S +0000')}] "
                f"\"GET {resource} HTTP/1.1\" {status} {random.randint(100, 5000)}\n"
            )
            f.write(log_line)
            
    print(f"Mock log created: {filename}")


def parse_log_line(line: str) -> tuple[str, int, str] | None:
    """
    Parses a single log line to extract IP, status code, and resource.
    Returns (ip, status, resource) or None if parsing fails.
    """
    try:
        # Split the line by space (simplified, real logs are more complex)
        parts = line.split()
        
        # Check if the line has the minimum expected structure
        if len(parts) < 10:
            return None
            
        ip = parts[0]
        status = int(parts[8]) # Status code is typically the 9th element (index 8)
        resource = parts[6]    # Resource path is typically the 7th element (index 6)
        
        return ip, status, resource
        
    except (ValueError, IndexError):
        # Handle malformed lines gracefully
        return None


def analyze_log_file(input_file: str, output_file: str):
    """
    Reads the input log, aggregates statistics, and writes the summary report.
    Ensures safe reading and writing using 'with' statements.
    """
    total_requests = 0
    successful_requests = 0
    unique_ips = set()
    error_counts = {} # Stores counts for 4xx and 5xx errors

    # --- Phase 1: Reading and Processing ---
    try:
        # CRITICAL: Use 'with' for safe file reading (mode 'r'). Iterates line by line.
        with open(input_file, 'r') as infile:
            print(f"\nAnalyzing log file: {input_file}...")
            
            for line in infile:
                total_requests += 1
                parsed_data = parse_log_line(line)
                
                if parsed_data:
                    ip, status, _ = parsed_data
                    unique_ips.add(ip)
                    
                    if 200 <= status < 300:
                        successful_requests += 1
                    elif status >= 400:
                        # Aggregate errors (4xx client, 5xx server)
                        error_counts[status] = error_counts.get(status, 0) + 1
                        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Cannot proceed.")
        sys.exit(1)
    
    # Calculate derived statistics
    if total_requests == 0:
        print("Log file is empty or unreadable.")
        return
        
    success_rate = (successful_requests / total_requests) * 100
    
    # --- Phase 2: Writing the Report ---
    
    report_content = [
        f"--- Server Log Analysis Report ({datetime.date.today()}) ---",
        f"Total Requests Processed: {total_requests}",
        f"Successful Requests (2xx): {successful_requests}",
        f"Success Rate: {success_rate:.2f}%",
        f"Unique Visitors (IPs): {len(unique_ips)}",
        "\n--- Error Distribution ---"
    ]
    
    # Sort and format error data
    if error_counts:
        for status, count in sorted(error_counts.items()):
            report_content.append(f"Status {status}: {count} occurrences")
    else:
        report_content.append("No 4xx or 5xx errors detected.")

    # CRITICAL: Use 'with' for safe file writing (mode 'w')
    try:
        with open(output_file, 'w') as outfile:
            for line in report_content:
                outfile.write(line + "\n")
        print(f"Analysis complete. Report written to {output_file}")
        
    except IOError as e:
        print(f"Error writing report file: {e}")


# --- Main Execution Block ---
if __name__ == "__main__":
    generate_mock_log(LOG_FILE, MOCK_ENTRIES)
    analyze_log_file(LOG_FILE, REPORT_FILE)

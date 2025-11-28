
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

import socket
import threading
import sys
from typing import Tuple, Optional

# --- 1. Global Configuration and Setup ---

# In-memory data store simulating configuration settings
CONFIG_STORE = {
    "SERVER_NAME": "RawPythonServer/1.0",
    "MAX_CONNECTIONS": "100",
    "DEBUG_MODE": "False"
}
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
BUFFER_SIZE = 1024
MAX_LISTENERS = 5


# --- 2. HTTP Request Parsing Utilities ---

def parse_request(request_data: bytes) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Manually parses raw HTTP request data into Method, Path, and Body.
    This function performs the critical task normally handled by a web framework's WSGI layer.
    """
    # Decode bytes and split the entire request by the HTTP line ending (\r\n)
    try:
        lines = request_data.decode('utf-8').split('\r\n')
    except UnicodeDecodeError:
        return None, None, None
        
    if not lines or not lines[0]:
        return None, None, None

    # Parse the Request Line (e.g., GET /config HTTP/1.1)
    try:
        method, path, _ = lines[0].split(' ')
    except ValueError:
        return None, None, None

    # Extract the request body, which follows the blank line separating headers and body
    body = ""
    try:
        # Find the index of the blank line (which is an empty string '')
        body_start_index = lines.index("")
        # The body is the line immediately following the blank line
        if body_start_index + 1 < len(lines):
            body = lines[body_start_index + 1]
    except ValueError:
        pass # No body found (typical for simple GET requests)

    return method, path, body

def build_response(status_code: str, content_type: str, body: str) -> bytes:
    """
    Constructs a complete, correctly formatted HTTP response string ready for transmission.
    """
    # 1. Status Line (e.g., HTTP/1.1 200 OK)
    status_line = f"HTTP/1.1 {status_code}\r\n"
    
    # 2. Headers
    # Calculate Content-Length based on the byte size of the body
    body_bytes = body.encode('utf-8')
    headers = [
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close", # Standard practice for non-persistent connections
        f"Server: {CONFIG_STORE['SERVER_NAME']}"
    ]
    
    # Combine status, headers, and body, separated by the required \r\n\r\n
    raw_response = (status_line + "\r\n".join(headers) + "\r\n\r\n" + body)
    return raw_response.encode('utf-8')


# --- 3. Application Logic and Routing ---

def handle_request(client_socket: socket.socket):
    """
    The core function executed by each thread to process a single client connection.
    It reads data, routes based on method/path, executes logic, and sends the response.
    """
    try:
        # 3.1. Read the raw request data from the socket
        request_data = client_socket.recv(BUFFER_SIZE)
        if not request_data:
            return

        method, path, body = parse_request(request_data)

        # Default response values (used for 404)
        response_body = "<h1>404 Not Found</h1><p>The requested resource was not found.</p>"
        status = "404 Not Found"
        content_type = "text/html"

        # 3.2. Routing Logic (The "view" functions)
        
        if method == 'GET' and path == '/config':
            # View Configuration Endpoint
            status = "200 OK"
            content_type = "text/html"
            
            # Generate dynamic HTML output based on the current CONFIG_STORE
            config_html = "<h2>Current Configuration Settings</h2><ul>"
            for k, v in CONFIG_STORE.items():
                config_html += f"<li><b>{k}:</b> {v}</li>"
            config_html += "</ul>"
            
            # Include a simple HTML form for testing the POST endpoint
            config_html += """
            <hr>
            <h3>Update Setting (POST Test)</h3>
            <form method="POST" action="/update">
                Key: <input type="text" name="key" value="DEBUG_MODE"><br>
                Value: <input type="text" name="value" value="True"><br>
                <input type="submit" value="Update Config">
            </form>
            """
            response_body = config_html

        elif method == 'POST' and path == '/update':
            # Update Configuration Endpoint
            try:
                # Manual parsing of the POST body (e.g., key=value)
                key, value = body.split('=')
                key = key.strip()
                value = value.strip()

                if key in CONFIG_STORE:
                    CONFIG_STORE[key] = value # Update the global dictionary
                    status = "200 OK"
                    response_body = f"<h1>Success</h1><p>Updated {key} to {value}. <a href='/config'>View Config</a></p>"
                else:
                    status = "400 Bad Request"
                    response_body = f"<h1>Error</h1><p>Key '{key}' not recognized in configuration.</p>"

            except (ValueError, AttributeError):
                status = "400 Bad Request"
                response_body = "<h1>Error</h1><p>Invalid POST body format. Expected 'key=value'.</p>"
        
        # 3.3. Construct and send the final response
        response = build_response(status, content_type, response_body)
        client_socket.sendall(response)

    except Exception as e:
        # Log unexpected errors
        print(f"Server runtime error: {e}", file=sys.stderr)
    finally:
        # Ensure the connection is closed after handling the request
        client_socket.close()


# --- 4. Server Initialization and Main Loop ---

def start_server():
    """Initializes the socket, binds to the host/port, and enters the listening loop."""
    
    # Create a TCP socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket option to allow reuse of the address quickly after shutdown
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(MAX_LISTENERS) # Queue up to 5 pending connections
        print(f"*** Raw Config Server running on http://{SERVER_HOST}:{SERVER_PORT} ***")
        
        while True:
            # 4.1. Block until a client connects
            client_conn, client_addr = server_socket.accept()
            print(f"Connection accepted from {client_addr[0]}:{client_addr[1]} - Handling...")
            
            # 4.2. Start a new thread to handle the client request concurrently
            client_thread = threading.Thread(target=handle_request, args=(client_conn,))
            client_thread.daemon = True # Allows the server to exit even if threads are running
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down gracefully...")
    except Exception as e:
        print(f"[CRITICAL] Server failure: {e}", file=sys.stderr)
    finally:
        # Clean up the main socket
        server_socket.close()

if __name__ == "__main__":
    start_server()

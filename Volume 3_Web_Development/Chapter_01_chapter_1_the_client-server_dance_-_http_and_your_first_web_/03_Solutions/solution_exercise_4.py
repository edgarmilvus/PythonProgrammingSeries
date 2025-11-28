
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

import socket
import sys

# --- Helper Functions (from Exercises 1, 2, 3) ---

def parse_request_line(raw_line):
    """ Parses the HTTP request line into (Method, Path, Version). """
    try:
        parts = raw_line.split(' ', 2)
        if len(parts) != 3:
            return None, None, None
        return parts[0], parts[1], parts[2]
    except Exception:
        return None, None, None

def parse_headers(raw_headers_string):
    """ Converts raw header string into a lowercase dictionary. """
    headers = {}
    lines = raw_headers_string.split('\r\n')
    for line in lines:
        if not line:
            continue
        try:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value.strip()
        except ValueError:
            continue
    return headers

ROUTER = {
    '/': {'GET': 200},
    '/api/users': {'GET': 200, 'POST': 201},
    '/admin': {'POST': 200}
}

def determine_response(method, path):
    """ Determines status code based on method and path. """
    if path not in ROUTER:
        return 404
    
    allowed_methods = ROUTER[path]
    if method in allowed_methods:
        return allowed_methods[method]
    else:
        return 405


# --- Exercise 4: Server Implementation with POST Body Handling ---

def handle_request(client_socket):
    """
    Handles a single client connection, including reading the full POST body
    based on the Content-Length header.
    """
    # 1. Read initial chunk (headers and potentially start of body)
    try:
        initial_data_bytes = client_socket.recv(4096)
        initial_data = initial_data_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return # Connection error

    if not initial_data:
        return

    # Find the separator between headers and body
    separator = '\r\n\r\n'
    separator_index = initial_data.find(separator)
    
    if separator_index == -1:
        # Malformed request or headers too large for initial read
        return 

    # Split request into header part and initial body part
    header_part = initial_data[:separator_index]
    # +4 to skip the length of '\r\n\r\n'
    body_part_initial = initial_data[separator_index + len(separator):]

    # Process request line
    lines = header_part.split('\r\n')
    request_line = lines[0]
    method, path, version = parse_request_line(request_line)

    if not method:
        response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n"
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
        return

    # Process headers
    raw_headers = '\r\n'.join(lines[1:])
    headers = parse_headers(raw_headers)
    
    request_body = body_part_initial
    response_status = 200
    response_body = ""

    # --- Core POST Handling Logic ---
    if method == 'POST':
        content_length_str = headers.get('content-length')
        
        if content_length_str:
            try:
                content_length = int(content_length_str)
            except ValueError:
                content_length = 0
            
            # Calculate how many bytes of the body were already read in the initial chunk
            # Note: We must use the byte length for accurate counting
            bytes_already_read = len(request_body.encode('utf-8'))
            bytes_to_read = content_length - bytes_already_read
            
            remaining_body_bytes = b''
            
            if bytes_to_read > 0:
                # Read the remaining body bytes
                while len(remaining_body_bytes) < bytes_to_read:
                    # Read only the necessary remaining amount
                    chunk = client_socket.recv(bytes_to_read - len(remaining_body_bytes))
                    if not chunk:
                        # Connection closed prematurely
                        break 
                    remaining_body_bytes += chunk
                
                # Append the newly read bytes (decoded) to the initial body part
                request_body += remaining_body_bytes.decode('utf-8', errors='ignore')
            
            # Log the received data
            print(f"\n--- RECEIVED POST DATA ({content_length} bytes) ---")
            print(f"Path: {path}")
            print(request_body)
            print("---------------------------------------------------\n")

            response_status = determine_response(method, path)
            response_body = f"POST received successfully. Status: {response_status}. Data snippet: {request_body[:50]}..."
        
        else:
            # 411 Length Required (POST must have Content-Length)
            response_status = 411 
            response_body = "Error 411: Content-Length header missing for POST request."

    # --- GET/Other Handling Logic ---
    else:
        response_status = determine_response(method, path)
        if response_status == 200:
            response_body = f"Requested path: {path}. Method: {method}. Server is running."
        elif response_status == 404:
            response_body = f"Error 404: Resource not found at {path}."
        elif response_status == 405:
            response_body = f"Error 405: Method {method} not allowed for path {path}."
        else:
            response_body = f"Status {response_status}."


    # 4. Construct and send final response
    status_text = "OK" if response_status in (200, 201) else "ERROR"
    response_line = f"HTTP/1.1 {response_status} {status_text}"
    response_body_bytes = response_body.encode('utf-8')
    
    response_headers = (
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body_bytes)}\r\n"
        f"Connection: close\r\n"
    )
    full_response = f"{response_line}\r\n{response_headers}\r\n".encode('utf-8') + response_body_bytes
    
    client_socket.sendall(full_response)
    client_socket.close()


def run_server(host='127.0.0.1', port=8080):
    """ Main server loop setup. """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows reuse of the address immediately after shutdown
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server running on http://{host}:{port}. Listening for connections...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established from {client_address}")
            handle_request(client_socket)
            
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    # Usage: python script.py [port]
    if len(sys.argv) > 1:
        try:
            custom_port = int(sys.argv[1])
            run_server(port=custom_port)
        except ValueError:
            print("Invalid port number provided. Using default port 8080.")
            run_server()
    else:
        run_server()

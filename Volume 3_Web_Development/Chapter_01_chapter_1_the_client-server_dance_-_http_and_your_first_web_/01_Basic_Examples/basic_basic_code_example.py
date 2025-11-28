
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

import socket
import sys

# 1. Configuration Constants
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080         # Port to listen on (non-privileged ports are >= 1024)
BUFFER_SIZE = 1024  # Maximum size of data chunk to receive at once

def run_basic_server():
    """
    Initializes and runs a single-threaded, blocking web server.
    """
    # 2. Socket Creation: AF_INET for IPv4, SOCK_STREAM for TCP
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Failed to create socket: {e}")
        sys.exit(1)

    # 3. Bind the socket to the defined address and port
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f"Failed to bind to {HOST}:{PORT}. Error: {e}")
        server_socket.close()
        sys.exit(1)

    # 4. Listen for incoming connections. The '1' is the backlog queue size.
    server_socket.listen(1)
    print(f"*** Server initialized. Listening on http://{HOST}:{PORT} ***")

    # 5. Main Server Loop: The server runs indefinitely
    while True:
        # 6. Accept Connection: This call blocks until a client connects
        print("\nWaiting for a connection...")
        
        # client_connection is a new socket object used for communication
        # client_address is the (IP, Port) of the client
        client_connection, client_address = server_socket.accept()
        print(f"Connection accepted from {client_address[0]}:{client_address[1]}")

        try:
            # 7. Receive Request: Read up to BUFFER_SIZE bytes of the request
            request_bytes = client_connection.recv(BUFFER_SIZE)
            
            # Decode the raw bytes into a readable string (HTTP is usually ASCII/UTF-8)
            request_data = request_bytes.decode('utf-8')
            
            # Display the raw request for educational purposes
            print("-" * 30)
            print("RAW HTTP REQUEST RECEIVED:")
            print(request_data.split('\n')[0]) # Print only the Request Line
            print("-" * 30)

            # 8. Craft the HTTP Response (Manual Construction)
            
            # 8a. Status Line (HTTP Version, Status Code, Reason Phrase)
            STATUS_LINE = "HTTP/1.1 200 OK\r\n"
            
            # 8b. Headers (Metadata about the response)
            HEADERS = (
                "Content-Type: text/html; charset=utf-8\r\n"
                "Content-Length: {length}\r\n"
                "Connection: close\r\n" # Tell the client we are closing the connection
            )
            
            # 8c. Body (The actual content)
            BODY_CONTENT = "<h1>Success!</h1><p>This page was served by a Python socket.</p>"
            
            # Format the Content-Length header dynamically
            HEADERS = HEADERS.format(length=len(BODY_CONTENT.encode('utf-8')))
            
            # 8d. Combine all parts, ensuring the crucial blank line separates headers and body
            # The structure is: Status Line + Headers + CRLF + Body
            RESPONSE = STATUS_LINE + HEADERS + "\r\n" + BODY_CONTENT
            
            # 9. Send the Response: Convert the final string back to bytes
            client_connection.sendall(RESPONSE.encode('utf-8'))

        except Exception as e:
            print(f"An error occurred during handling: {e}")

        finally:
            # 10. Close the Connection
            # Crucial step: release the socket resource for this specific client
            client_connection.close()
            print(f"Connection closed for {client_address[0]}")

if __name__ == "__main__":
    run_basic_server()

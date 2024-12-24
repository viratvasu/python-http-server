import threading
import socket  # noqa: F401
import sys
import os

def handle_request(client_socket, client_address):
    print(f"Connection received from {client_address}")
    # Read the request from the client
    request = client_socket.recv(4096).decode("utf-8")
    request_lines = request.split('\r\n')
    
    # Parse the request line
    request_line = request_lines[0]
    method, target, *_ = request_line.split()
    
    # Parse headers
    headers = {}
    current_line = 1
    while current_line < len(request_lines) and request_lines[current_line]:
        header_line = request_lines[current_line]
        key, value = header_line.split(': ', 1)
        headers[key.lower()] = value
        current_line += 1
    
    if method == "GET":
        if target == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif target.startswith("/echo/"):
            value = target.split("/echo/")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
        elif target.startswith("/user-agent"):
            value = headers.get('user-agent', '')
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
        elif target.startswith("/files/"):
            directory = sys.argv[2]
            filename = target[7:]
            try:
                with open(os.path.join(directory, filename), "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            except Exception as e:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    elif method == "POST" and target.startswith("/files/"):
        # Handle POST request for file creation
        filename = target[7:]
        directory = sys.argv[2]
        
        # Get content length from headers
        content_length = int(headers.get('content-length', 0))
        
        # Find the start of the request body (after the blank line)
        body_start = request.find('\r\n\r\n') + 4
        body = request[body_start:body_start + content_length]
        
        # Create the file in the specified directory
        try:
            with open(os.path.join(directory, filename), "w") as f:
                f.write(body)
            response = b"HTTP/1.1 201 Created\r\n\r\n"
        except Exception as e:
            response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
    
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    client_socket.sendall(response)
    client_socket.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, client_address = server_socket.accept()  # wait for client
        threading.Thread(target=handle_request, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
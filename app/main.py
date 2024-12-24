import threading
import socket
import sys

def handle_request(client_socket, client_address):
    print(f"Connection received from {client_address}")
    
    # Read the request from the client
    request = client_socket.recv(4096).decode("utf-8")
    print(f"Request received: {request}")

    lines = request.split("\r\n")
    
    # First line should contain the request method and target
    request_line = lines[0]
    try:
        method, target, _ = request_line.split(" ")
    except ValueError:
        print("Error parsing the request line")
        response = b"HTTP/1.1 400 Bad Request\r\n\r\n"
        client_socket.sendall(response)
        client_socket.close()
        return
    
    # Extract headers (skip the empty lines at the end)
    headers = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "":
        try:
            key, value = lines[i].split(": ", 1)
            headers[key] = value
        except ValueError:
            # Skip invalid headers
            pass
        i += 1

    print(f"Method: {method}, Target: {target}")
    print(f"Headers: {headers}")
    
    # Handling different types of requests
    if method == "GET":
        if target == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif target.startswith("/files/"):
            directory = sys.argv[2]
            filename = target[7:]
            try:
                with open(f"{directory}/{filename}", "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            except FileNotFoundError:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    elif method == "POST" and target.startswith("/files/"):
        # Handle POST method for /files/{filename}
        directory = sys.argv[2]
        filename = target.split("/files/")[1]
        content_length = int(headers.get("Content-Length", 0))

        if content_length > 0:
            print(f"Expecting {content_length} bytes of data from the body.")
            # Read the request body (expecting the size of content-length)
            body = client_socket.recv(content_length).decode("utf-8")
            print(f"Body received: {body}")
            
            try:
                with open(f"{directory}/{filename}", "w") as f:
                    f.write(body)

                # Respond with HTTP 201 Created
                response = b"HTTP/1.1 201 Created\r\n\r\n"
            except Exception as e:
                # Log exception to help debug
                print(f"Error writing file: {e}")
                response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
        else:
            response = b"HTTP/1.1 400 Bad Request\r\n\r\n"

    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # Send the response back to the client and ensure the connection is closed after
    print(f"Sending response: {response}")
    try:
        client_socket.sendall(response)
        client_socket.close()
    except Exception as e:
        print(f"Error during sending response: {e}")

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running...")
    while True:
        client_socket, client_address = server_socket.accept()  # wait for client
        threading.Thread(target=handle_request, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    main()

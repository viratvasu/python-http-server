import socket  # noqa: F401


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept() # wait for client
    print(f"Connection received from {client_address}")
    # Read the request from the client
    request = client_socket.recv(4096).decode("utf-8")
    client_data = request.split(" ")
    target = client_data[1]
    if target == "/":
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif target.startswith("/echo/"):
        value = target.split("/echo/")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
        client_socket.sendall(response)
    else:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()

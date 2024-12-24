import socket  # noqa: F401


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept() # wait for client
    print(f"Connection received from {client_address}")
    # Read the request from the client
    request = client_socket.recv(4096).decode("utf-8")
    client_data = request.split(" ")
    if client_data[1] == "/":
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()

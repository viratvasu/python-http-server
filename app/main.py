import threading
import socket  # noqa: F401


def handle_request(socket_conn, addr):
    try:
        # Read the request from the client
        request = socket_conn.recv(4096).decode("utf-8")
        print(f"Received request from {addr}:\n{request}")

        # Respond with the required HTTP response
        response = b"HTTP/1.1 200 OK\r\n\r\n"
        socket_conn.sendall(response)
    except Exception as e:
        print(f"Error handling request from {addr}: {e}")
    finally:
        # Close the connection
        socket_conn.close()
def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")

    while True:
        try:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection received from {client_address}")

            # Handle each client in a separate thread
            threading.Thread(target=handle_request, args=(client_socket, client_address)).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")
      


if __name__ == "__main__":
    main()

import socket  # noqa: F401


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
      client_socket, client_address = server_socket.accept() # wait for client
      print(f"Connection received from {client_address}")
      # Read the request from the client
      request = client_socket.recv(1024).decode('utf-8')
      print(f"Request: {request}")
      if request.startswith("GET"):
          response = "HTTP/1.1 200 OK\r\n\r\n"
          client_socket.sendall(response.encode('utf-8'))
      # return the response with start-line
      #<protocol> <status-code> <status-text>
      client_socket.close()


if __name__ == "__main__":
    main()

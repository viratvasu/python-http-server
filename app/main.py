import threading
import socket  # noqa: F401
import sys


def handle_request(client_socket, client_address):
  print(f"Connection received from {client_address}")
  # Read the request from the client
  request = client_socket.recv(4096).decode("utf-8")
  client_data = request.split(" ")
  target = client_data[1]
  if target == "/":
      response = b"HTTP/1.1 200 OK\r\n\r\n"
  elif target.startswith("/echo/"):
      value = target.split("/echo/")[1]
      response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
  elif target.startswith("/user-agent"):
      value=client_data[-1].strip()
      response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(value)}\r\n\r\n{value}".encode()
      # response = b"HTTP/1.1 200 OK\r\n\r\n"
  elif target.startswith("/files"):
      directory = sys.argv[2]
      filename = target[7:]
      try:
          with open(f"/{directory}/{filename}", "r") as f:
              body = f.read()
          response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
      except Exception as e:
          response = b"HTTP/1.1 404 Not Found\r\n\r\n"
  else:
      response=b"HTTP/1.1 404 Not Found\r\n\r\n"
  
  client_socket.sendall(response)

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
      client_socket, client_address = server_socket.accept() # wait for client
      threading.Thread(target=handle_request, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    main()

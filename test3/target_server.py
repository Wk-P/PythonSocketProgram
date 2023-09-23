import socket

def start_server():
    server_sock = socket.socket()

    server_ip = "127.0.0.1"
    server_port = 80
    server_sock.bind((server_ip, server_port))
    server_sock.listen(2)

    while True:
        print(f"Waiting connection...")

        client_socket, client_address = server_sock.accept()
        print(f"Connected with {client_address[0]}:{client_address[1]}")

        client_socket.send("Yes".encode('utf-8'))

        client_socket.close()


if __name__ == "__main__":
    start_server()
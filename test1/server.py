import socket

# 数据类型 text

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostIP = "127.0.0.1"
    port = 8080
    server.bind((hostIP, port))
    server.listen(3)


    conn, addr = server.accept()

    while True:
        data = conn.recv(1024).decode('utf-8')
        print(data)
        if data == 'Hello' or data == 'hello':
            conn.send('Hello'.encode('utf-8'))
        elif data == 'bye' or data == 'BYE' or data == 'Bye':
            conn.send("Bye".encode('utf-8'))
            break
        else:
            conn.send("...".encode('utf-8'))
    conn.close()

if __name__ == "__main__":
    main()

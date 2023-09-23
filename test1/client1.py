import socket

def main():
    client = socket.socket()
    hostIP = "127.0.0.1"
    port = 8080
    
    client.connect((hostIP, port))

    client.send('Hello'.encode('utf-8'))

    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'bye' or data == 'BYE' or data == 'Bye':
                break
            send_data = str(input("]")).encode('utf-8')
            client.send(send_data)
        
        client.close()

    except ConnectionError as e:
        exit(1)        
if __name__ == "__main__":
    main()

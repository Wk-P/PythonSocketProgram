# client socket
import socket
import requests
import traceback
import json
import time

# REQUEST TYPE: JSON

# socket connection
def main():
    ip, host = '127.0.0.1', 8080
    address = ((ip, host))
    to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Send request to {address}")

    
    to_server_socket.connect(address)
    try:
        while True:
            to_server_socket.send("Hello".encode("utf-8"))

            response = to_server_socket.recv(1024)
            print(f"Response from server: {response.decode()} .")

    except:
        to_server_socket.close()


# requests.get request
def http():
    try:
        url = "http://127.0.0.1:8080"
        headers = {
            "Accept": "application/json"
        }
        data = {
            'content': "Hello"
        }

        response = requests.get(
           url=url, headers=headers, json=data
        )
        print(json.loads(response.text)['message'])

    except Exception as e:
        traceback.print_exc()
        print("Value Error!")


if __name__ == '__main__':
    # main()
    while True:
        http()
        time.sleep(4)
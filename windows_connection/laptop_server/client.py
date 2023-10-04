import requests
import json

def send_request(url):
    data = {
        'content': "Hello"
    }
    return requests.post(url, json=data)

def main():
    url = "http://192.168.1.5:8080"
    response = send_request(url)
    print(response)


if __name__ == "__main__":
    main()
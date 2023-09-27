import requests


def send_request(url):
    return requests.get(url)

def main():
    url = "http://192.168.1.7:8080"
    response = send_request(url)
    print(response)


if __name__ == "__main__":
    main()
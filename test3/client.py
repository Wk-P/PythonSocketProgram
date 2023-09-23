import requests


def send_request(url):
    return requests.get(url)

def main():
    url = "http://127.0.0.1:8080"
    response = send_request(url)
    print(response)


if __name__ == "__main__":
    main()
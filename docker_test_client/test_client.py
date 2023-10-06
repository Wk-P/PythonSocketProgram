import requests
data = {
    'num': 10
}
response = requests.post('http://192.168.56.102:8080', json=data)
print(response.json())
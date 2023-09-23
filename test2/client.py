import requests

# 构造要发送到服务器的数据，这里假设为 JSON 数据
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# 使用 requests 发送 POST 请求，将数据以 JSON 格式发送
response = requests.post('http://127.0.0.1:8080', json=data)

print(response.text)

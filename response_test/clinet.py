import http.client
import json

client_conn = http.client.HTTPConnection("http://127.0.0.1", 8888)

data = json.dumps({
    "req": "Request"
}).encode('utf-8')

client_conn.request(method='POST', url='http://127.0.0.1:8888', body=data)

client_conn.getresponse()
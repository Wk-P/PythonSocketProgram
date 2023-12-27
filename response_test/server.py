import http.server
import http.client
import socketserver
import requests
import socket
import json


class RequestTrans(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        # to json for target 
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        post_data['client_address'] = self.client_address[0]
        post_data['client_port'] = self.client_address[1]
        print(post_data)
        str_post_data = json.dumps(post_data)
        headers = dict(self.headers)
        headers['Content-Length'] = str(content_length + len(str_post_data))
        target_conn = http.client.HTTPConnection("127.0.0.1", 8999)
        target_conn.request(method='POST', url='/', body=str_post_data.encode('utf-8'), headers=headers)
        
        target_conn.close()

with socketserver.TCPServer(("", 8888), RequestTrans) as httpd:
    httpd.serve_forever()
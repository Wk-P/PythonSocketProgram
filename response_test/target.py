import http.server
import socketserver
import requests
import socket
import json

class ReuqestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        str_post_data = self.rfile.read(content_length).decode('utf-8')

        post_data = json.loads(str_post_data)
    
        self.send_response(200)

        self.send_response_to_address("Hello from 8999", post_data['client_address'], post_data['client_port'])

    def send_response_to_address(self, content, address, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((address, port))
            client_socket.sendall(content)

with socketserver.TCPServer(("", 8999), ReuqestHandler) as httpd:
    httpd.serve_forever()
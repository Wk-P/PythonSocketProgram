import http.server
import socket
import threading

# 目标服务器的 IP 和端口
target_ip = "127.0.0.1"  # 替换为实际的目标 IP 地址
target_port = 80  # 替换为实际的目标端口

# 创建路由表，将路径映射到目标服务器的不同路径
route_table = {
    # '/': 127.0.0.1
    "/": {"ip": target_ip, "port": target_port},
    # 添加更多的路径映射...
}

# 创建一个简单的 HTTP 请求处理程序
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 获取请求路径
        path = self.path

        # test
        print(path)

        # 根据路由表查找目标服务器的 IP 和端口
        if path in route_table:
            target = route_table[path]
            target_ip = target["ip"]
            target_port = target["port"]

            # 创建与目标服务器的连接并发送请求
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((target_ip, target_port))
            target_socket.sendall(self.requestline.encode())

            # 从目标服务器接收响应并发送回客户端
            response = target_socket.recv(4096)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response)
            target_socket.close()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')

# 启动 HTTP 服务器监听
def start_server():
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    print("Listening on port 8080...")
    httpd.serve_forever()

# 启动 HTTP 服务器线程
server_thread = threading.Thread(target=start_server)
server_thread.start()

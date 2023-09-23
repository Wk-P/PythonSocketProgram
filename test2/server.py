import http.server
import json

# 自定义请求处理器类
class CustomRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # 从客户端接收数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 解析 JSON 数据
        data = json.loads(post_data)
        
        # 在这里处理数据，例如打印它
        print(data)
        
        # 发送响应
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

# 创建 HTTP 服务器并启动
server_address = ('127.0.0.1', 8080)
httpd = http.server.HTTPServer(server_address, CustomRequestHandler)
print(f'Starting server on {server_address[0]}:{server_address[1]}')
httpd.serve_forever()

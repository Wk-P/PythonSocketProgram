from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import time


class CustomHTTPServer(HTTPServer):
    def serve_forever(self):
        print("Custom server is running...")
        while True:
            print("Waiting request...")
            self.handle_request()  # process request from client
            print("Processed request!")


class CustomResponseHandler(BaseHTTPRequestHandler):
    # set log message
    def log_message(self, format, *args):
        pass


    # parse requests object to json
    def __parse(self):
        content_length = int(self.headers['Content-Length'])
        get_data = self.rfile.read(content_length)
        # parse JSON data
        data = json.loads(get_data)
        return data

    def do_GET(self):
        data = self.__parse()

        print(data['content'])

        # make status code
        self.send_response(200)


        # set header
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # set response data
        response_content = {
            'message': "OK",
            'status': 'success'
        }

        self.wfile.write(json.dumps(response_content).encode('utf-8'))


def main():
    
    # start server
    server_address = ("127.0.0.1", 8002)
    httpd = CustomHTTPServer(server_address, CustomResponseHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except:
        print("Server stopped.")
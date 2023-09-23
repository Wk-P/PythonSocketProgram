from http.server import BaseHTTPRequestHandler, HTTPServer

class ResponseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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

        self.wfile.write(response_content)


def main():
    server_address = ("127.0.0.1", 8001)
    httpd = HTTPServer(server_address, ResponseHandler)

    print(f"Serving on {server_address[0]}:{server_address[1]}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
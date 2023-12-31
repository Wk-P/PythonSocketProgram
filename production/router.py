from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json


# This class is to make a HTTP response
class ResponseHandler(BaseHTTPRequestHandler):
    
    # set log message
    def log_message(self, format, *args):
        print(f"Requested from {self.headers['Host']}.")


    # parse requests object to json
    def __parse(self):
        content_length = int(self.headers['Content-Length'])
        get_data = self.rfile.read(content_length)
        # parse JSON data
        data = json.loads(get_data)
        return data

    # GET method
    def do_GET(self):
        
        # decide address
        target_address = None
        
        for address in route_table:
            if route_table[address]['status'] == "Y":
                target_address = f"{route_table[address]['ip']}:{route_table[address]['port']}"
                break
        

        # send requests to table
        # server can receive request
        if target_address != None:
            
            # make request object
            url = f"http://{target_address}"
            

            # send request to server
            response_content = ""
            error_response = {
                'code': 500,
                'status': 'failed'
            }

            try:
                response_from_server = requests.get(url, json=self.__parse())
                # request from server to router successfully
                response_content = response_from_server.text
            except:
                response_content = json.dumps(error_response)
                print('Response error!')
                

        # server can't receive request
        else:
            response_content = json.dumps(error_response)

        # send response to client (transform to byte string)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(response_content.encode('utf-8'))



def main():
    try:
        # get requests from client
        route_address = ("127.0.0.1", 8080)
        # httpd = HTTPServer(route_address, ResponseHandler)

        print(f"Start router on {route_address[0]}:{route_address[1]}")
        httpd = HTTPServer(route_address, ResponseHandler)

        httpd.serve_forever()
    except:
        print("Router stopped")


if __name__ == "__main__":
    route_table = {
        'addr1': {
            'ip': "127.0.0.1",
            'port': 8001,
            'status': 'N'
        },
        'addr2': {
            'ip': "127.0.0.1",
            'port': 8002,
            'status': 'Y'
        }
    }
    try:
        main()
    except:
        print("Router stopped")
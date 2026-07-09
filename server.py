import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

class SimpleHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == '/hello':
            self._set_headers()
            response = {"message": "Hello, World!"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/time':
            self._set_headers()
            response = {"time": datetime.datetime.utcnow().isoformat() + "Z"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_headers(404)
            response = {"error": "Not Found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

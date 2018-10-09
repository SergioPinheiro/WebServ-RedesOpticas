from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
#from io import BytesIO

data = '''{
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}'''
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # self.wfile.write(json.dumps(data).encode())
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())
        return
        
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
      #  response = BytesIO()
       # response.write(b'This is POST request. ')
        #response.write(b'Received: ')
        #response.write(body)
        #self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
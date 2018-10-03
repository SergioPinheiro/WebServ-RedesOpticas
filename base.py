from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Serv(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(bytes(f.read(), 'utf-8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print ("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = json.loads(self.data_string)
        with open("test123456.json", "w") as outfile:
            json.dump(data, outfile)
        print ("{}".format(data))
        f = open("for_presen.py")
        self.wfile.write(bytes(f.read(), 'utf-8'))
        return

def run(server_class=HTTPServer, handler_class=Serv, port=8080):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()
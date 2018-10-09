from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import networkx as nx

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
        data = json.loads(self.data_string)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        try:
            self.wfile.write(json.dumps(self.dkt(data)).encode())
        except:
            print('Dijkstra error!')
        return

    def dkt(self, json_G):
        G = nx.Graph()
        for edge in json_G['edges']:
            G.add_edge(edge['begin'], edge['end'], weight=int(edge['len']))
        resp = dict()
        for conection in json_G['connections']:
            short = nx.single_source_dijkstra(G, conection['begin'], conection['end'], weight='weight')
            resp["{}-{}".format(conection['begin'], conection['end'])] = short
        return resp

def run(server_class=HTTPServer, handler_class=Serv, port=8080):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()
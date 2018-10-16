from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import networkx as nx
import os

class Serv(BaseHTTPRequestHandler):

    # def __init__(self):
    #     self.elementos = []


    def _set_headers(self):
        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        pass

    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".ico"):
                mimetype='image/ico'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
				#Open the static file requested and send it
                f = open("./atividade 4" + self.path, "r", errors='ignore')#, encoding="utf-8") 
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(), 'utf-8'))
                f.close()
                return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        print ("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        print(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # self.wfile.write(bytes("hello"), 'utf-8')
        try:
            self.wfile.write(json.dumps(self.dkt(data)).encode())
        except:
            print('Dijkstra error!')
        return

    def dkt(self, json_G):
        G = nx.Graph()
        # print(json_G['edges'])
        for edge in json_G['edges']:
            G.add_edge(edge['from'], edge['to'], weight=int(edge['label']))
        resp = list()
        for conection in json_G['connections']:
            item = dict()
            short = nx.single_source_dijkstra(G, conection['begin'], conection['end'], weight='weight')
            item['id'] = "{}-{}".format(conection['begin'], conection['end'])
            item['finalWeight'] = short[0]
            item['path'] = short[1]
            resp.append(item)
        resp = sorted(resp, key=lambda i: i['finalWeight'])
        print(resp)
        return resp

def run(server_class=HTTPServer, handler_class=Serv, port=8080):
    # web_dir = os.path.join(os.path.dirname(__file__), './atividade 4/')
    # print(web_dir)
    # os.chdir(web_dir)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()
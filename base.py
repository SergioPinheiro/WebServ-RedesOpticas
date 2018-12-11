from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import networkx as nx
import numpy as np
import time
from threading import Thread, Lock

def sum_weight(path, graph):
    sum = 0
    for i in range(len(path)-1):
        sum += graph.edges[path[i], path[i+1]]["weight"]
    return sum

def block_wavelenght_in_path(lock, path, wavelenght, c_duration, index, jobs_list, graph):
    print("bloqueando caminho", path, wavelenght)
    lock.acquire()
    for i in range(len(path) - 1):
        graph.edges[path[i], path[i + 1]]['wavelenghts'][str(wavelenght)] = True
    lock.release()
    print("caminho bloqueado", path, wavelenght)
    wake_time = c_duration[index['poisson_duration']]
    print('incrementando valor de indice de duração de {} para {}'.format(index['poisson_duration'], index['poisson_duration']+1))
    index['poisson_duration'] += 1
    print('iniciando processo para caminho', path, wavelenght)
    p = Thread(target=free_wavelenght_in_path, args=(lock, path, wavelenght, wake_time, graph))
    jobs_list.append(p)
    p.start()

def free_wavelenght_in_path(lock, path, wavelenght, wake_time, graph):
    print("esperando {} segundos para liberar caminho {} {}".format(wake_time, path, wavelenght))
    time.sleep(wake_time)
    print("liberando caminho", path, wavelenght)
    lock.acquire()
    for i in range(len(path) - 1):
        graph.edges[path[i], path[i + 1]]['wavelenghts'][str(wavelenght)] = False
    lock.release()
    print("caminho liberado", path, wavelenght)

def first_fit(lock, graph, paths, nwavelenght, id, conections_duration, index, jobs_list):
    resp = dict()
    i = 0
    path = list()
    final_wavelenght = 0
    finishSearch = False
    while not finishSearch and (i < len(paths)):
        j = 0
        while not finishSearch and (j < nwavelenght):
            k = 0
            while not finishSearch and (k < len(paths[i]) - 1):
                # se o comprimento de onda estiver sendo utilizado o loop para
                if graph.edges[paths[i][k], paths[i][k + 1]]['wavelenghts'][str(j)]:
                    break
                elif k == (len(paths[i]) - 2):
                    path = paths[i]
                    final_wavelenght = j
                    finishSearch = True
                k += 1
            j += 1
        if i == (len(paths) - 1) and not finishSearch:
            final_wavelenght = -1
        i += 1
    resp['id'] = id
    resp['path'] = path
    if (len(path) > 0):
        resp['finalWeight'] = sum_weight(path, graph)
        block_wavelenght_in_path(lock, path, final_wavelenght, conections_duration, index, jobs_list, graph)
    else:
        resp['finalWeight'] = 0
        print('não deu fit', id)
    resp['wavelenght'] = final_wavelenght
    return resp




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
        #print(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # self.wfile.write(bytes("hello"), 'utf-8')
        #try:
        self.wfile.write(json.dumps(self.dkt(data)).encode())
        #except:
         #   print('Dijkstra error!')
        return

    def dkt(self, json_G):
        G = nx.Graph()
        resp = list()
        n_wave_lenghts = int(json_G['nwavelenghts'])
        wave_lenghts = dict()
        global_paths = dict()
        lmbda = len(json_G['connections']) / int(json_G['tempo'])
        conections_interval = -np.log(1.0 - np.random.random_sample(len(json_G['connections']))) / lmbda
        lmbda = lmbda
        conections_duration = -np.log(1.0 - np.random.random_sample(len(json_G['connections']))) / lmbda
        #conections_duration = [15]*len(json_G['connections'])
        l = Lock()
        jobs = []
        indexes = {'poisson_interval': 0, 'poisson_duration': 0}
        print('variaveis declaradas')
        print('lista de intervalos')
        print(conections_interval)
        print('lista de durações')
        print(conections_duration)


        # O boleano indica se o comprimento de onda está ou não sendo usado. Ex: True = Está sendo usado
        for i in range(n_wave_lenghts):
            wave_lenghts[str(i)] = False
        for edge in json_G['edges']:
            G.add_edge(edge['from'], edge['to'], weight=int(edge['label']), wavelenghts=wave_lenghts.copy())

        for conection in json_G['connections']:
            id = "{}-{}".format(conection['begin'], conection['end'])
            reverse_id = "{}-{}".format(conection['end'], conection['begin'])
            has_pathlist = False
            while not has_pathlist:
                try:
                    if len(global_paths[id]) > 0:
                        resp.append(first_fit(l, G, global_paths[id], n_wave_lenghts, id, conections_duration, indexes,
                                              jobs))
                        has_pathlist = True
                        print('esperando {} segundos até iniciar nova conexão'.format(conections_interval[
                                                                                          indexes['poisson_interval']]))
                        time.sleep(conections_interval[indexes['poisson_interval']])
                        print('aumentando indice de intervalo de {} para {}'.format(indexes['poisson_interval'],
                                                                                    indexes['poisson_interval']+1))
                        indexes['poisson_interval'] += 1
                except KeyError:
                    try:
                        global_paths[id] = list(
                            nx.shortest_simple_paths(G, conection['begin'], conection['end'], weight='weight'))
                        global_paths[reverse_id] = list(
                            nx.shortest_simple_paths(G, conection['end'], conection['begin'], weight='weight'))
                    except (nx.NetworkXNoPath, nx.exception.NetworkXError, nx.NodeNotFound):
                        #altera a flag em caso de erro para ir para o proximo item
                        has_pathlist = True
                        print('esperando {} segundos até iniciar nova conexão'.format(conections_interval[
                                                                                          indexes['poisson_interval']]))
                        time.sleep(conections_interval[indexes['poisson_interval']])
                        print('aumentando indice de intervalo de {} para {}'.format(indexes['poisson_interval'],
                                                                                    indexes['poisson_interval'] + 1))
                        indexes['poisson_interval'] += 1
                        continue

        resp = sorted(resp, key=lambda i: i['finalWeight'])
        falhas = 0
        for i in resp:
            if i['wavelenght'] == -1:
                falhas+=1
        prob_falha = falhas/len(json_G['connections'])
        final_resp = dict()
        final_resp['connections'] = resp
        final_resp['falha'] = prob_falha

        print(final_resp)
        for key in global_paths.keys():
            print("{} - {}".format(key, global_paths[key]))

        return final_resp

def run(server_class=HTTPServer, handler_class=Serv, port=8080):
    # web_dir = os.path.join(os.path.dirname(__file__), './atividade 4/')
    # print(web_dir)
    # os.chdir(web_dir)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()
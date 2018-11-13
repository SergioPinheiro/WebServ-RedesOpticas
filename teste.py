import networkx as nx
import numpy as np
import time

def sum_weight(path, graph):
    sum = 0
    for i in range(len(path)-1):
        sum += graph.edges[path[i], path[i+1]]["weight"]
    return sum

def block_wavelenght_in_path(graph, path, wavelenght):
    for i in range(len(path)-1):
        graph.edges[path[i], path[i + 1]]['wavelenghts'][str(wavelenght)] = True

def free_wavelenght_in_path(graph, path, wavelenght):
    for i in range(len(path)-1):
        graph.edges[path[i], path[i + 1]]['wavelenghts'][str(wavelenght)] = False


def first_fit(graph, paths, nwavelenght, id):
    resp = dict()
    i = 0
    path = list()
    final_wavelenght = 0
    finishSearch = False
    while (not finishSearch and (i < len(paths))):
        j = 0
        while (not finishSearch and (j < nwavelenght)):
            k = 0
            while (not finishSearch and (k < len(paths[i])-1)):
                if(graph.edges[paths[i][k], paths[i][k+1]]['wavelenghts'][str(j)]==True):
                    break
                elif k == (len(paths[i])-2):
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
    if(len(path)>0):
        resp['finalWeight'] = sum_weight(path, graph)
        block_wavelenght_in_path(graph, path, final_wavelenght)
    else:
        resp['finalWeight'] = 0
    resp['wavelenght'] = final_wavelenght
    return resp


edgesArray = [
    {"from": 1, "to": 2, "label": '50'},
    {"from": 1, "to": 4, "label": '80'},
    {"from": 1, "to": 6, "label": '150'},
    {"from": 2, "to": 3, "label": '60'},
    {"from": 2, "to": 4, "label": '40'},
    {"from": 2, "to": 5, "label": '90'},
    {"from": 3, "to": 5, "label": '110'},
    {"from": 3, "to": 8, "label": '150'},
    {"from": 4, "to": 6, "label": '150'},
    {"from": 4, "to": 7, "label": '130'},
    {"from": 5, "to": 7, "label": '120'},
    {"from": 5, "to": 8, "label": '130'},
    {"from": 6, "to": 7, "label": '120'},
    {"from": 7, "to": 8, "label": '120'}
]

conections = [
    {"begin": 5, "end": 1},
    {"begin": 5, "end": 1},
    {"begin": 5, "end": 1},
    {"begin": 1, "end": 5},
    {"begin": 3, "end": 1},
    {"begin": 3, "end": 1},
    {"begin": 3, "end": 1},
    {"begin": 6, "end": 4},
    {"begin": 111, "end": 530}
]

G = nx.Graph()
resp = list()
n_wave_lenghts = 2
wave_lenghts = dict()
global_paths = dict()
seconds = 300
lmbda = len(conections)/seconds
conections_interval = -np.log(1.0 - np.random.random_sample(len(conections))) / lmbda
conections_duration = -np.log(1.0 - np.random.random_sample(len(conections))) / lmbda

for i in range(n_wave_lenghts):
    wave_lenghts[str(i)] = False
for edge in edgesArray:
    G.add_edge(edge['from'], edge['to'], weight=int(edge['label']), wavelenghts=wave_lenghts.copy() )

for conection in conections:
    poisson_index = 0
    id = "{}-{}".format(conection['begin'], conection['end'])
    reverse_id = "{}-{}".format(conection['end'], conection['begin'])
    item_ready = False
    while not item_ready:
        try:
            if len(global_paths[id]) > 0:
                resp.append(first_fit(G, global_paths[id], n_wave_lenghts, id))
                item_ready = True
        except KeyError:
            try:
                global_paths[id] = list(
                    nx.shortest_simple_paths(G, conection['begin'], conection['end'], weight='weight'))
                global_paths[reverse_id] = list(
                    nx.shortest_simple_paths(G, conection['end'], conection['begin'], weight='weight'))
            except (nx.NetworkXNoPath, nx.exception.NetworkXError, nx.NodeNotFound):
                item_ready = True
                time.sleep(conections_interval[poisson_index])
                poisson_index +=1
                continue

resp = sorted(resp, key=lambda i: i['finalWeight'])
print(resp)
for key in global_paths.keys():
    print(global_paths[key])


'''def dkt(self, json_G):
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
    return resp'''
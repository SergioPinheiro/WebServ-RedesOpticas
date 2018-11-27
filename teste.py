import networkx as nx
import numpy as np
import time
from threading import Thread, Lock


def sum_weight(path, graph):
    sum = 0
    for i in range(len(path) - 1):
        sum += graph.edges[path[i], path[i + 1]]["weight"]
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


if __name__ == '__main__':
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
    {"begin": 6, "end": 4}
    ]

    G = nx.Graph()
    resp = list()
    n_wave_lenghts = 2
    wave_lenghts = dict()
    global_paths = dict()
    seconds = 50
    lmbda = len(conections) / seconds
    conections_interval = -np.log(1.0 - np.random.random_sample(len(conections))) / lmbda
    #conections_interval = [5] * len(conections)
    lmbda = lmbda * 3
    conections_duration = -np.log(1.0 - np.random.random_sample(len(conections))) / lmbda
    #conections_duration = [0.1]*len(conections)
    l = Lock()
    jobs = []
    print('variaveis declaradas')
    print(conections_duration)
    print(conections_interval)
    indexes = {'poisson_interval': 0, 'poisson_duration': 0}
    for i in range(n_wave_lenghts):
        wave_lenghts[str(i)] = False

    for edge in edgesArray:
        G.add_edge(edge['from'], edge['to'], weight=int(edge['label']), wavelenghts=wave_lenghts.copy())

    for conection in conections:
        id = "{}-{}".format(conection['begin'], conection['end'])
        reverse_id = "{}-{}".format(conection['end'], conection['begin'])
        item_ready = False
        while not item_ready:
            try:
                if len(global_paths[id]) > 0:
                    resp.append(first_fit(l, G, global_paths[id], n_wave_lenghts, id,
                                          conections_duration, indexes, jobs))
                    item_ready = True
                    time.sleep(conections_interval[indexes['poisson_interval']])
                    indexes['poisson_interval'] += 1
            except KeyError:
                try:
                    global_paths[id] = list(
                        nx.shortest_simple_paths(G, conection['begin'], conection['end'], weight='weight'))
                    global_paths[reverse_id] = list(
                        nx.shortest_simple_paths(G, conection['end'], conection['begin'], weight='weight'))
                except (nx.NetworkXNoPath, nx.exception.NetworkXError, nx.NodeNotFound):
                    item_ready = True
                    time.sleep(conections_interval[indexes['poisson_interval']])
                    indexes['poisson_interval'] += 1
                    continue

    resp = sorted(resp, key=lambda i: i['finalWeight'])
    print('resposta final')
    print(resp)
    for key in global_paths.keys():
        print(global_paths[key])
    for job in jobs:
        job.join()


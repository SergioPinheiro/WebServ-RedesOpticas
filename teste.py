import networkx as nx

def sum_weight(path):
    sum = 0
    for i in range(len(path)-1):
        sum += G.edges[path[i], path[i+1]]["weight"]
    return sum


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
    {"begin": 3, "end": 1},
    {"begin": 3, "end": 1},
    {"begin": 3, "end": 1},
    {"begin": 6, "end": 4}
]

G = nx.Graph()
for edge in edgesArray:
    #print(edge)
    G.add_edge(edge['from'], edge['to'], weight=int(edge['label']))

#print(list(nx.shortest_simple_paths(G, 5, 1, weight='weight')))
#print(nx.single_source_dijkstra(G, 5, 1, weight='weight'))
#print(G.edges[5,2]["weight"])
#print(sum_weight([5, 2, 1]))

global_paths = dict()

resp = list()
for conection in conections:
    item = dict()
    item["id"] = "{}-{}".format(conection['begin'], conection['end'])
    item_ready = False
    while not item_ready:
        try:
            if len(global_paths[item["id"]]) > 0:
                item['path'] = global_paths[item["id"]].pop(0);
                item['finalWeight'] = sum_weight(item['path'])
                resp.append(item)
                item_ready = True
            else:
                item_ready = True
        except KeyError:
            global_paths[item['id']] = list(nx.shortest_simple_paths(G, conection['begin'], conection['end'], weight='weight'))

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
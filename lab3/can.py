import random
from plotgraph import plot_graph
from mappers import gen2dpoint
from utils import is_neighbours, centr, sec_distance, find_shortest
from netdarw import dump_plot_network, plot_path
import string


class Node:
    def __init__(self, id):
        self.id = id
        self.ip = None
        self.data = []
        self.can = CAN()

    def insert_node(self, node):
        self.can.insert_node(self, node)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f'<Node id : {self.id} >'


class CAN:
    def __init__(self):
        self.zone = []
        self.neigbours = []
        self.data = dict()

        self.__split_index = 0
        self.__split_index_mod = 2

    def insert_node(self, cnode, node):
        if not self.zone:
            return None

        t = self.zone[self.__split_index]
        m = sum(t) / len(t)
        self.zone[self.__split_index] = (t[0], m)
        res = [e if i != self.__split_index else (m, t[1])
               for i, e in enumerate(self.zone)]
        node.can.zone = res
        self.__distribute_neigbours(cnode, node)
        self.__split_index = (self.__split_index + 1) % self.__split_index_mod

    def __distribute_neigbours(self, cnode,  node):
        cur_n = [node]
        ext_n = [cnode]
        for ngb in self.neigbours:
            ngb.can.neigbours.remove(cnode)
            if is_neighbours(self.zone, ngb.can.zone):
                cur_n.append(ngb)
                ngb.can.neigbours.append(cnode)
            if is_neighbours(node.can.zone, ngb.can.zone):
                ext_n.append(ngb)
                ngb.can.neigbours.append(node)

        self.neigbours = cur_n
        node.can.neigbours = ext_n


def generate_graph(vrt_count: int,
                   vrt_pow_min: int,
                   vrt_pow_max: int,
                   max_iterations_per_node=1000):

    graph = dict()
    nodes = []
    nodes.append(Node(0))
    for i in range(1, vrt_count):
        node = Node(i)
        graph[node] = [nodes[-1]]
        graph[nodes[-1]] = [node]
        nodes.append(node)

    for node in nodes:
        cpower = len(graph[node])
        rpower = random.randint(vrt_pow_min, vrt_pow_max)
        iteration = 0
        while cpower < rpower and iteration < max_iterations_per_node:
            rnode = random.choice(nodes)
            iteration += 1

            notCurrent = rnode != node
            notInAlready = rnode not in graph[node]
            powerAllowed = len(graph.get(rnode, [])) < vrt_pow_max
            if notCurrent and notInAlready and powerAllowed:
                graph[node].append(rnode)
                graph[rnode].append(node)
                cpower += 1

        if cpower < vrt_pow_min:
            return {
                'graph': graph,
                'nodes': nodes,
                'ok': False
            }

    return {
        'graph': graph,
        'nodes': nodes,
        'ok': True
    }


def init_physic_network(nodes):
    cur = 256**3
    for node in nodes:
        ip = [cur // (256**i) % 256 for i in range(4)]
        node.ip = '.'.join([str(e) for e in reversed(ip)])
        cur += 1


def search(graph, cnode: Node, point, return_path=False):
    path = []
    res = search_(graph, cnode, point, path)
    if return_path:
        return res, path
    else:
        return res


def search_(graph, cnode: Node, point, path):
    path.append(cnode)
    if cnode.can.zone:
        z = cnode.can.zone
        is_in_zone = all([z[i][0] < point[i] < z[i][1] for i in range(2)])
        if is_in_zone:
            return cnode

    if not cnode.can.neigbours:
        return None

    dsts = [sec_distance(ngb.can.zone, point)
            for ngb in cnode.can.neigbours]
    i = dsts.index(min(dsts))
    return search_(graph, cnode.can.neigbours[i], point, path)


def init_can(graph, nodes):
    nodes[0].can.zone = [(0, 1), (0, 1)]

    for i in range(1, len(nodes)):
        point = gen2dpoint(nodes[i].ip)
        res = search(graph, nodes[i-1], point)
        res.insert_node(nodes[i])


def add_data(grapth, nodes, count):
    files = []
    for i in range(count):
        f = ''.join(random.sample(string.ascii_letters, random.randint(1, 20)))
        files.append(f)
        node = random.choice(nodes)
        node.data.append(f)
        point = gen2dpoint(f)
        snode = search(graph, node, point)
        snode.can.data[f] = node

    return files


def test_file_search(graph, nodes, files):
    logs = []
    rf = random.choice(files)
    rfh = gen2dpoint(rf)
    for node in nodes:
        n, path = search(graph, node, rfh, return_path=True)
        n.can.data[rf].data.index(rf)
        ip_path = find_shortest(graph, node, n)
        logs.append({
            'CAN': len(path) - 1,
            'ip': ip_path,
        })

    return logs


def vizualize_hops(graph, nodes):
    res, path = search(graph, nodes[0], (0.1, 0.13), return_path=True)
    im = plot_path(nodes, path, (1200, 1200))
    im.save('path5.png')

    res, path = search(graph, nodes[0], (0.22, 0.13), return_path=True)
    im = plot_path(nodes, path, (1200, 1200))
    im.save('path10.png')

    res, path = search(graph, nodes[0], (0.172, 0.3), return_path=True)
    im = plot_path(nodes, path, (1200, 1200))
    im.save('path15.png')

def print_stat(logs, nodes):
    def make_stat(stat):
        return f'min : {min(stat)}; max : {max(stat)}; mean : {sum(stat) / len(stat)}'

    can = [e['CAN'] for e in logs]
    print(f'CAN {make_stat(can)}')

    ip = [e['ip'] for e in logs]
    print(f'IP {make_stat(ip)}')
    
    file_routes = [len(node.can.data) for node in nodes]
    print(f'file routes {make_stat(file_routes)}')

    neigbours_count = [len(node.can.neigbours) for node in nodes]
    print(f'neigbours count {make_stat(neigbours_count)}')

 
res = generate_graph(1000, 3, 9)
graph = res['graph']
nodes = res['nodes']
init_physic_network(nodes)
init_can(graph, nodes)
files = add_data(graph, nodes, 10000)
print('graph generated')

logs = test_file_search(graph, nodes, files)
print('test complite')
print_stat(logs, nodes)

dump_plot_network(nodes)
vizualize_hops(graph, nodes)

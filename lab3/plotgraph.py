import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple

Node = namedtuple('Node', ['id'])



def plot_graph(graph):
    G=nx.Graph()

    for node in graph:
        G.add_node(node.id, label=f'asdasd')

    for n1 in graph:
        for n2 in graph[n1]:
            G.add_edge(n1.id, n2)
    
    nx.draw(G)
    

    plt.savefig("simple_path.png")
    plt.show()

def plot_digraph(graph):
    G=nx.DiGraph()
    node_labels = dict()
    for node in graph:
        G.add_node(node.id)
        node_labels[node.id] = str(node.id)

    for n1 in graph:
        for n2 in graph[n1]:
            G.add_edge(n1.id, n2.id)
    
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos)
    nx.draw_networkx_labels(G, pos, node_labels)
    plt.savefig("simple_path.png")
    plt.show()
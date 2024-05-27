import json
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime

startTime = datetime.now()

print('startTime')
print(datetime.now() - startTime)


def draw_graph(graph):
    # add a curve to make it possible to visualize multiple edges between two nodes
    connectionstyle = "arc3,rad=0.4"
    pos = nx.planar_layout(graph)

    nx.draw_networkx_nodes(graph, pos, node_color="lightblue", node_size=300)
    nx.draw_networkx_edges(graph, pos, edge_color="grey", connectionstyle=connectionstyle)

    labels = {
        tuple(edge): f"{'val'}={attrs['weight']} - {attrs['name']}"
        for *edge, attrs in graph.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=labels,
        connectionstyle=connectionstyle
    )


f_users = open('tests/users.json')
f_items = open('tests/items.json')

users = json.load(f_users)
items = json.load(f_items)

items_dict = {item['id']: item for item in items}

# we create a directed graph for each possible item values. the nodes will be the users and the edges
# will be based on their wishes. The aim is to find cycles within those graphs.
graphs = dict([(50, nx.MultiDiGraph()),
               (100, nx.MultiDiGraph()),
               (150, nx.MultiDiGraph()),
               (200, nx.MultiDiGraph()),
               (250, nx.MultiDiGraph()),
               (300, nx.MultiDiGraph()),
               (350, nx.MultiDiGraph()),
               (400, nx.MultiDiGraph()),
               (450, nx.MultiDiGraph()),
               (500, nx.MultiDiGraph())])

for user in users:
    if len(user['items_wishes_id']) > 0:
        for item_wished_id in user['items_wishes_id']:
            item_wished = items_dict[item_wished_id]
            value = item_wished['value']
            if value in graphs:
                graphs.get(value).add_edge(user['id'], item_wished['user_id'], weight=item_wished['value'],
                                           name=item_wished['name'])

# prepare the graphs
for graph in graphs.values():
    #draw_graph(graph)

    # Find a cycle in the graph
    try:
        print('Start find cycle')
        print(datetime.now() - startTime)
        cycle = nx.find_cycle(graph, orientation="original")
        print(cycle)
    except Exception as error:
        print(error)

    #plt.show()

f_users.close()
f_items.close()

print(datetime.now() - startTime)

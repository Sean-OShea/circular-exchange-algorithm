import json
import networkx as nx
import matplotlib.pyplot as plt
import itertools as it


def get_item_by_id(items, item_wished):
    for item in items:
        if item['id'] == item_wished:
            return item
    return None

f_users = open('tests/users.json')
f_items = open('tests/items.json')

users = json.load(f_users)
items = json.load(f_items)

# create a directed graph that can store multiple edges with all the users, linked together based on their wishes
G = nx.MultiDiGraph()

for user in users:
    if len(user['items_wishes_id']) > 0:
        for item_wished_id in user['items_wishes_id']:
            item_wished = get_item_by_id(items, item_wished_id)
            G.add_edge(user['id'], item_wished['user_id'], weight=item_wished['value'], name=item_wished['name'])

pos = nx.planar_layout(G)
# add a curve to make it possible to visualize multiple edges between two nodes
connectionstyle = "arc3,rad=0.4"

nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=300)
nx.draw_networkx_edges(G, pos, edge_color="grey", connectionstyle=connectionstyle)
nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

labels = {
        tuple(edge): f"{'val'}={attrs['weight']} - {attrs['name']}"
        for *edge, attrs in G.edges(keys=True, data=True)
    }
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=labels,
    connectionstyle=connectionstyle
)

# Find a cycle in the graph, value of item not taken into account
cycle = nx.find_cycle(G, orientation="original")
print(cycle)

# Highlight the cycle in red
nx.draw_networkx_edges(G, pos, edgelist=cycle, edge_color="r", width=2)

plt.show()

f_users.close()
f_items.close()
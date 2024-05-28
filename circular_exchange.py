import json
import networkx as nx
import pygraphviz as pgv
import cProfile
import pstats

with cProfile.Profile() as profile:
    f_users = open('tests/users.json')
    f_items = open('tests/items.json')

    users = json.load(f_users)
    items = json.load(f_items)

    items_dict = {item['id']: item for item in items}

    # we create a directed graph for each possible item values. the nodes will be the users and the edges
    # will be based on their wishes. The aim is to find cycles within those graphs.
    graphs = {range: nx.MultiDiGraph() for range in range(50, 500, 50)}

    for user in users:
        if len(user['items_wishes_id']) > 0:
            for item_wished_id in user['items_wishes_id']:
                item_wished = items_dict[item_wished_id]
                value = item_wished['value']
                if value in graphs:
                    graphs.get(value).add_edge(user['id'], item_wished['user_id'], weight=item_wished['value'],
                                               name=item_wished['name'])

    # prepare the graphs
    G_cycles = pgv.AGraph(directed=True)
    for graph in graphs.values():
        # Find a cycle in the graph
        try:
            cycles = nx.find_cycle(graph, orientation='original')
            G_cycles.add_path(cycles)

        except Exception as error:
            print(error)

    G_cycles.layout(prog="dot")
    G_cycles.draw("file.pdf", format="pdf")

    f_users.close()
    f_items.close()

    results = pstats.Stats(profile)
    results.sort_stats('tottime')
    results.print_stats()

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
                                               name=item_wished['name'], key=item_wished['id'])

    # prepare the graphs
    G_cycles = pgv.AGraph(directed=True)
    total_cycles_found = 0
    for graph in graphs.values():
        count_cycles_found = 0
        # Find a cycle in the graph
        try:
            while True:
                cycle = nx.find_cycle(graph, orientation='original')
                cycle_edges = [(edge[0],edge[1],edge[2]) for edge in cycle]
                graph.remove_edges_from(cycle_edges)
                print(cycle)
                G_cycles.add_path(cycle)
                count_cycles_found += 1
        except Exception as error:
            print(error)

        total_cycles_found += count_cycles_found
        print(f"Cycles found: ' {count_cycles_found}")

    G_cycles.layout(prog='dot')
    G_cycles.draw("file.pdf", format="pdf")

    f_users.close()
    f_items.close()

    results = pstats.Stats(profile)
    results.sort_stats('tottime')
    results.print_stats(10)

    print(f"Total cycles found: ' {total_cycles_found}")

import cProfile
import json
import pstats

import networkx as nx
import pygraphviz as pgv

import conf.global_settings as env
from cycles_experiment_edge_removal import *

with cProfile.Profile() as profile:
    f_users = open(f"tests/{env.TESTS['users_file_name']}")
    f_items = open(f"tests/{env.TESTS['items_file_name']}")

    users = json.load(f_users)
    items = json.load(f_items)

    items_dict = {item["id"]: item for item in items}
    users_dict = {user["id"]: user for user in users}

    # we create a directed graph, the nodes will be the users and the edges
    # will be based on their wishes. The aim is to find cycles within those graphs.
    graph = nx.MultiDiGraph()

    for user in users:
        if len(user["items_wishes_id"]) > 0:
            for item_wished_id in user["items_wishes_id"]:
                item_wished = items_dict[item_wished_id]
                value = item_wished["value"]
                graph.add_edge(
                    user["id"],
                    item_wished["user_id"],
                    weight=item_wished["value"],
                    name=item_wished["name"],
                    key=item_wished["id"],
                )

    # prepare the graphs
    G_cycles = pgv.AGraph(directed=True)
    total_cycles_found = 0

    print(f"Cycle search start, graph size: {graph.size()}")
    for item_value in range(
        env.ITEMS["min_value"],
        env.ITEMS["max_value"] + env.ITEMS["value_step"],
        env.ITEMS["value_step"],
    ):
        count_cycles_found = 0
        # Find a cycle in the graph
        try:
            while True:
                cycle = find_cycle(
                    graph,
                    data_filter={
                        "max_depth": env.DFS_CYCLE["max_depth"],
                        "weight": item_value,
                    },
                )
                count_cycles_found += 1
                graph.remove_edges_from(cycle)
                cycle = cycle
                # link the last node to the first
                fromv = cycle[-1]
                while len(cycle) > 0:
                    tov = cycle.pop(0)
                    G_cycles.add_edge(
                        users_dict[fromv[0]]["name"],
                        users_dict[tov[0]]["name"],
                        key=fromv[2],
                        label=f" {fromv[3]['name']} ({fromv[3]['weight']})",
                    )
                    fromv = tov

        except Exception as error:
            print(error)

        total_cycles_found += count_cycles_found
        print(
            f"Cycle search for item value: {item_value}, Cycles found: {count_cycles_found}"
        )

    print(
        f"Cycle search end, graph size: {graph.size()}, total_cycles_found: {total_cycles_found}"
    )
    G_cycles.layout(prog="dot")
    G_cycles.draw("file2.pdf", format="pdf")

    f_users.close()
    f_items.close()

    results = pstats.Stats(profile)
    results.sort_stats("tottime")
    results.print_stats(10)

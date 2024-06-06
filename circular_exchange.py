import cProfile
import json
import logging
import pstats

import networkx as nx
import pygraphviz as pgvs

import conf.global_settings as env
from cycles import find_cycle

logging.basicConfig(
    filename=env.LOGGING["filename"],
    level=logging.DEBUG,
    format=env.LOGGING["format"],
    datefmt=env.LOGGING["datefmt"],
)

with cProfile.Profile() as profile:
    f_users = open(f"tests/{env.TESTS['users_file_name']}")
    f_items = open(f"tests/{env.TESTS['items_file_name']}")

    users = json.load(f_users)
    items = json.load(f_items)

    items_dict = {item["id"]: item for item in items}
    users_dict = {user["id"]: user for user in users}

    logging.debug(f"Number of users loaded: {len(users_dict)}")
    logging.debug(f"Number of items loaded: {len(items_dict)}")

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

    # prepare the graph that will contain all the cycles
    G_cycles = pgvs.AGraph(directed=True)

    # Find a cycle in the graph
    logging.debug(f"Cycle search start. Graph size: {graph.size()}")
    count_cycles_found = 0
    cycles = find_cycle(graph)
    logging.debug(f"Cycles search ends with {cycles} cycles")

    logging.debug("Starting the creation of the cycles graph")
    for cycle in cycles.values():
        if cycle:
            count_cycles_found += 1
            graph.remove_edges_from(cycle)
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

    logging.debug(f"Cycles graph created {count_cycles_found}")
    logging.debug(f"Cycle search end. Graph size: {graph.size()}")

    G_cycles.layout(prog="dot")
    G_cycles.draw(env.TESTS["cycles_file_name"], format="pdf")

    f_users.close()
    f_items.close()

    with open(env.PSTATS["filename"], env.PSTATS["mode"]) as stream:
        results = pstats.Stats(profile, stream=stream)
        results.sort_stats("tottime")
        results.print_stats(10)

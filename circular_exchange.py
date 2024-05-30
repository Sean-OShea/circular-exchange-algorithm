import json
import networkx as nx
import pygraphviz as pgv
import cProfile
import pstats
import conf.global_settings as env

# Uses an implementation of a DFS algorithm for a multi-edge directed graph
def find_cycle(G, source=None):
    """Returns a cycle found via depth-first traversal.

    The cycle is a list of edges indicating the cyclic path.
    Orientation of directed edges is controlled by `orientation`.

    Parameters
    ----------
    G : graph
        A directed/undirected graph/multigraph.

    source : node, list of nodes
        The node from which the traversal begins. If None, then a source
        is chosen arbitrarily and repeatedly until all edges from each node in
        the graph are searched.

    Returns
    -------
    edges : directed edges
        A list of directed edges indicating the path taken for the loop.
        If no cycle is found, then an exception is raised.
        For graphs, an edge is of the form `(u, v)` where `u` and `v`
        are the tail and head of the edge as determined by the traversal.
        For multigraphs, an edge is of the form `(u, v, key)`, where `key` is
        the key of the edge. When the graph is directed, then `u` and `v`
        are always in the order of the actual directed edge.
        If orientation is not None then the edge tuple is extended to include
        the direction of traversal ('forward' or 'reverse') on that edge.

    Raises
    ------
    NetworkXNoCycle
        If no cycle was found.

    Examples
    --------
    In this example, we construct a DAG and find, in the first call, that there
    are no directed cycles, and so an exception is raised. In the second call,
    we ignore edge orientations and find that there is an undirected cycle.
    Note that the second call finds a directed cycle while effectively
    traversing an undirected graph, and so, we found an "undirected cycle".
    This means that this DAG structure does not form a directed tree (which
    is also known as a polytree).

    >>> G = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
    >>> nx.find_cycle(G, orientation="original")
    Traceback (most recent call last):
        ...
    networkx.exception.NetworkXNoCycle: No cycle found.
    >>> list(nx.find_cycle(G, orientation="ignore"))
    [(0, 1, 'forward'), (1, 2, 'forward'), (0, 2, 'reverse')]

    See Also
    --------
    simple_cycles
    """

    def tailhead(edge):
        return edge[:2]

    explored = set()
    cycle = []
    final_node = None
    for start_node in G.nbunch_iter(source):
        if start_node in explored:
            # No loop is possible.
            continue

        edges = []
        # All nodes seen in this iteration of edge_dfs
        seen = {start_node}
        # Nodes in active path.
        active_nodes = {start_node}
        previous_head = None

        for edge in nx.edge_dfs(G, start_node, orientation="original"):
            # Determine if this edge is a continuation of the active path.
            tail, head = tailhead(edge)
            if head in explored:
                # Then we've already explored it. No loop is possible.
                continue
            if previous_head is not None and tail != previous_head:
                # This edge results from backtracking.
                # Pop until we get a node whose head equals the current tail.
                # So for example, we might have:
                #  (0, 1), (1, 2), (2, 3), (1, 4)
                # which must become:
                #  (0, 1), (1, 4)
                while True:
                    try:
                        popped_edge = edges.pop()
                    except IndexError:
                        edges = []
                        active_nodes = {tail}
                        break
                    else:
                        popped_head = tailhead(popped_edge)[1]
                        active_nodes.remove(popped_head)

                    if edges:
                        last_head = tailhead(edges[-1])[1]
                        if tail == last_head:
                            break
            edges.append(edge)

            if head in active_nodes:
                # We have a loop!
                cycle.extend(edges)
                final_node = head
                break
            else:
                seen.add(head)
                active_nodes.add(head)
                previous_head = head

        if cycle:
            break
        else:
            explored.update(seen)

    else:
        assert len(cycle) == 0
        raise nx.exception.NetworkXNoCycle("No cycle found.")

    # We now have a list of edges which ends on a cycle.
    # So we need to remove from the beginning edges that are not relevant.

    for i, edge in enumerate(cycle):
        tail, head = tailhead(edge)
        if tail == final_node:
            break

    return cycle[i:]

with cProfile.Profile() as profile:
    f_users = open(f"tests/{env.TESTS['users_file_name']}")
    f_items = open(f"tests/{env.TESTS['items_file_name']}")

    users = json.load(f_users)
    items = json.load(f_items)

    items_dict = {item['id']: item for item in items}

    # we create a directed graph for each possible item values. the nodes will be the users and the edges
    # will be based on their wishes. The aim is to find cycles within those graphs.
    graphs = {range: nx.MultiDiGraph()
              for range
              in range(env.ITEMS['min_value'], env.ITEMS['max_value'], env.ITEMS['value_step'])}

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
                cycle = find_cycle(graph)
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

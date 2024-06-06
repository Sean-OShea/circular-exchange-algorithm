"""
========================
Cycle finding algorithms
========================
"""

import logging

import networkx as nx

__all__ = ["find_cycle", "edge_dfs"]


def find_cycle(graph: nx.MultiDiGraph):
    """Returns a cycle found via depth-first traversal.

    The cycle is a list of edges indicating the cyclic path.
    Orientation of directed edges is controlled by `orientation`.

    Parameters
    ----------
    graph : graph
        A directed/undirected graph/multigraph.

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
    """

    def tailhead(edge):
        return edge[:2]

    logging.debug("find_cycle Start")

    explored: dict[str, set] = {}
    cycles: dict[str, list] = {}
    final_node = None

    # iterate through all the nodes of the graph in order to find every possible cycles
    for start_node in graph.nbunch_iter():
        # if start_node in explored:
        # No loop is possible.
        # continue

        edges: dict[str, list] = {}
        # All nodes seen in this iteration of edge_dfs
        seen = {start_node}
        # Nodes in active path.
        active_nodes = {start_node}
        previous_head = None

        start_node_edges = graph.edges(start_node, data=True)
        # node exploration has to be made for each possible weight values as there may be multiple cycles going through
        # each node.
        weights = {edge[2]["weight"] for edge in list(start_node_edges)}

        log_cycle_variables(
            start_node=start_node,
            cycles=cycles,
            explored=explored,
            final_node=final_node,
            weights=weights,
            edges=edges,
            seen=seen,
            active_nodes=active_nodes,
            previous_head=previous_head,
        )

        # check if there are new weights that are being encountered. Update the concerned variables if needed
        explored.update({weight: set() for weight in weights.difference(explored)})
        cycles.update({weight: [] for weight in weights.difference(cycles)})
        edges.update({weight: [] for weight in weights.difference(edges)})
        """
        popped_edge.update(
            {weight: [] for weight in weights.difference(popped_edge.keys())}
        )
        popped_head.update(
            {weight: [] for weight in weights.difference(popped_head.keys())}
        )
        last_head.update(
            {weight: [] for weight in weights.difference(last_head.keys())}
        )
        # All nodes seen in this iteration of edge_dfs
        seen = {weight: {start_node} for weight in weights}
        # Nodes in active path.
        active_nodes = {weight: {start_node} for weight in weights}
        previous_head = {weight: None for weight in weights}
        head = {weight: None for weight in weights}
        tail = {weight: None for weight in weights}

        """
        final_node = {weight: None for weight in weights}
        # going from the current start_node, get every accessible edges in the graph
        for edge in edge_dfs(graph, start_node):
            logging.debug(f"Edge found: {edge}")

            weight = edge[3]["weight"]
            # Determine if this edge is a continuation of the active path.
            tail, head = tailhead(edge)
            if explored.get(weight) and head in list(explored.get(weight)):
                # Then we've already explored it. No loop is possible.
                continue
            # Stop the cycle search if it's about to exceed the max_depth filter or if the edge has its weight outside
            # the range of the previous node
            # if weight not in weights:
            #      continue
            """
            if len(active_nodes) == env.DFS_CYCLE["max_depth"]:
                match env.DFS_CYCLE["edge_removal"]:
                    case None:
                        break
                    case "failed_cycle_nodes":
                        # Remove the concerned edge of the starting node as we found no cycle from it
                        for edge in edges[weight]:
                            graph.remove_edge(*edge[:3])
                    case "current_node":
                        # Remove the concerned edge of the starting node as we found no cycle from it
                        graph.remove_edge(*edges[weight][0][:3])
                break
            """
            if previous_head is not None and tail != previous_head:
                # This edge results from backtracking.
                # Pop until we get a node whose head equals the current tail.
                # So for example, we might have:
                #  (0, 1), (1, 2), (2, 3), (1, 4)
                # which must become:
                #  (0, 1), (1, 4)
                while True:
                    try:
                        print(active_nodes)
                        popped_edge = edges[weight].pop()
                    except (IndexError, KeyError):
                        edges[weight] = []
                        active_nodes = {tail}
                        break
                    else:
                        popped_head = tailhead(popped_edge)[1]
                        active_nodes.remove(popped_head)

                    if edges[weight]:
                        last_head = tailhead(edges[weight][-1])[1]
                        if tail == last_head:
                            break

            edges.get(weight).append(edge)

            if head in active_nodes:
                # We have a loop!
                cycles[weight].extend(edges[weight])
                final_node[weight] = head
                break
            else:
                seen.add(head)
                active_nodes.add(head)
                previous_head = head

        for weight in weights:
            if len(cycles) == sum([cycle for cycle in cycles if cycle > 0]):
                break
            else:
                explored.get(weight).update(seen)

    # We now have a list of edges which ends on a cycle.
    # So we need to remove from the beginning edges that are not relevant.

    return cycles


def edge_dfs(G, source):
    """A directed, depth-first-search of edges in `G`, beginning at `source`.

    Yield the edges of G in a depth-first-search order continuing until
    all edges are generated.

    Parameters
    ----------
    G : graph
        A directed multigraph.

    source : node, the node from which the traversal begins.

    Yields
    ------
    edge : directed edge
        A directed edge indicating the path taken by the depth-first traversal.
        `edge` is of the form `(u, v, key, data)`, where `key` is
        the key of the edge. `u` and `v`
        are always in the order of the actual directed edge.
    """
    nodes = list(G.nbunch_iter(source))
    if not nodes:
        return

    kwds = {"data": True}
    kwds["keys"] = True

    def edges_from(node):
        return iter(G.edges(node, **kwds))

    visited_edges = set()
    visited_nodes = set()
    edges = {}

    # start DFS
    for start_node in nodes:
        stack = [start_node]
        while stack:
            current_node = stack[-1]
            if current_node not in visited_nodes:
                edges[current_node] = edges_from(current_node)
                visited_nodes.add(current_node)

            try:
                edge = next(edges[current_node])
            except StopIteration:
                # No more edges from the current node.
                stack.pop()
            else:
                edgeid = (frozenset(edge[:2]), edge[2])
                if edgeid not in visited_edges:
                    visited_edges.add(edgeid)
                    stack.append(edge[1])
                    yield edge


def log_cycle_variables(**kwargs):
    logging.debug("Cycle variables:")
    for variable_name, value in kwargs.items():
        logging.debug(f"---- {variable_name}: {value}")

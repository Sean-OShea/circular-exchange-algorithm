"""
========================
Cycle finding algorithms
========================
"""

import networkx as nx

import conf.global_settings as env

__all__ = ["find_cycle", "edge_dfs"]


def find_cycle(G: nx.MultiDiGraph):
    """Returns a cycle found via depth-first traversal.

    The cycle is a list of edges indicating the cyclic path.
    Orientation of directed edges is controlled by `orientation`.

    Parameters
    ----------
    G : graph
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

    explored = set()
    cycle = []
    final_node = None
    for start_node in G.nbunch_iter():
        if start_node in explored:
            # No loop is possible.
            continue

        edges = []
        # All nodes seen in this iteration of edge_dfs
        seen = {start_node}
        # Nodes in active path.
        active_nodes = {start_node}
        previous_head = None

        for edge in edge_dfs(G, start_node):
            # Stop the cycle search if it's about to exceed the max_depth filter
            if len(active_nodes) == env.DFS_CYCLE["max_depth"]:
                match env.DFS_CYCLE["edge_removal"]:
                    case None:
                        break
                    case "failed_cycle_nodes":
                        # Remove the concerned edge of the starting node as we found no cycle from it
                        for edge in edges:
                            G.remove_edge(*edge[:3])
                    case "current_node":
                        # Remove the concerned edge of the starting node as we found no cycle from it
                        G.remove_edge(*edges[0][:3])
                break
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
        raise Exception("No cycle found.")

    # We now have a list of edges which ends on a cycle.
    # So we need to remove from the beginning edges that are not relevant.

    for i, edge in enumerate(cycle):
        tail, head = tailhead(edge)
        if tail == final_node:
            break

    return cycle[i:]


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
                if edgeid not in visited_edges and edge[3]["weight"] == 50:
                    visited_edges.add(edgeid)
                    stack.append(edge[1])
                    yield edge

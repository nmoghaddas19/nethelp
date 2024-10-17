def bfs(explore_queue, nodes_visited, graph):
    """
    Performs a recursive breadth-first search (BFS) on a graph.

    This function explores the graph in a breadth-first manner starting from nodes
    in the `explore_queue`. It visits each node, exploring all of its neighbors 
    before moving on to nodes at the next level of depth. The distances of each node 
    from the starting node are recorded in `nodes_visited`.

    Parameters:
    ----------
    explore_queue : list
        A queue (list) of nodes to be explored. Initially contains the starting node(s).
    nodes_visited : dict
        A dictionary that stores the nodes that have been visited as keys, with their 
        corresponding distances from the starting node as values.
    graph : networkx.Graph
        The graph on which the BFS is being performed. Must be a NetworkX graph object.

    Returns:
    -------
    nodes_visited : dict
        A dictionary where keys are nodes and values are the shortest distance 
        (in terms of edge count) from the starting node.
    """
    if len(explore_queue) == 0:
        return nodes_visited
    else:
        current_node = explore_queue.pop(0)
        print('visiting node ' + str(current_node))
        for neighbor in G.neighbors(current_node):
            if neighbor in nodes_visited:
                continue
            else:
                nodes_visited[neighbor] = nodes_visited[current_node] + 1
                explore_queue.append(neighbor)
        return bfs(explore_queue, nodes_visited, graph)

def dfs(explore_stack, nodes_visited, graph):
    """
    Performs a recursive depth-first search (DFS) on a graph.

    This function explores the graph in a depth-first manner using a stack. It starts
    from nodes in the `explore_stack` and visits each node by going as deep as possible
    along unvisited neighbors before backtracking. The distances of each node from the 
    starting node are recorded in `nodes_visited`.

    Parameters:
    ----------
    explore_stack : list
        A stack (list) of nodes to be explored. Initially contains the starting node(s).
    nodes_visited : dict
        A dictionary that stores the nodes that have been visited as keys, with their 
        corresponding distances from the starting node as values.
    graph : networkx.Graph
        The graph on which the DFS is being performed. Must be a NetworkX graph object.

    Returns:
    -------
    nodes_visited : dict
        A dictionary where keys are nodes and values are the distance (in terms of edge count) 
        from the starting node, as recorded during the depth-first exploration.
    """
    if len(explore_stack) == 0:
        return nodes_visited
    else:
        current_node = explore_stack.pop(-1)
        print('visiting node {}'.format(str(current_node)))
        for neighbor in G.neighbors(current_node):
            if neighbor in nodes_visited:
                continue
            else:
                nodes_visited[neighbor] = nodes_visited[current_node] + 1
                explore_stack.append(neighbor)
        return dfs(explore_stack, nodes_visited, graph)
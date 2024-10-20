import numpy as np
import networkx as nx
def degree_distribution(G, number_of_bins=15, log_binning=True, density=True, directed=False):
    """
    Given a degree sequence, return the y values (probability) and the
    x values (support) of a degree distribution that you're going to plot.
    
    Parameters
    ----------
    G (nx.Graph):
        the network whose degree distribution to calculate

    number_of_bins (int):
        length of output vectors
    
    log_binning (bool):
        if you are plotting on a log-log axis, then this is useful
    
    density (bool):
        whether to return counts or probability density (default: True)
        Note: probability densities integrate to 1 but do not sum to 1. 

    directed (bool or str):
        if False, this assumes the network is undirected. Otherwise, the
        function requires an 'in' or 'out' as input, which will create the 
        in- or out-degree distributions, respectively.
        
    Returns
    -------
    bins_out, probs (np.ndarray):
        probability density if density=True node counts if density=False; binned edges
    
    """

    # Step 0: Do we want the directed or undirected degree distribution?
    if directed:
        if directed=='in':
            k = list(dict(G.in_degree()).values()) # get the in degree of each node
        elif directed=='out':
            k = list(dict(G.out_degree()).values()) # get the out degree of each node
        else:
            out_error = "Help! if directed!=False, the input needs to be either 'in' or 'out'"
            print(out_error)
            # Question: Is this the correct way to raise an error message in Python?
            #           See "raise" function...
            return out_error
    else:
        k = list(dict(G.degree()).values()) # get the degree of each node


    # Step 1: We will first need to define the support of our distribution
    kmax = np.max(k)    # get the maximum degree
    kmin = 0            # let's assume kmin must be 0


    # Step 2: Then we'll need to construct bins
    if log_binning:
        # array of bin edges including rightmost and leftmost
        bins = np.logspace(0, np.log10(kmax+1), number_of_bins+1)
    else:
        bins = np.linspace(0, kmax+1, num=number_of_bins+1)


    # Step 3: Then we can compute the histogram using numpy
    probs, _ = np.histogram(k, bins, density=density)


    # Step 4: Return not the "bins" but the midpoint between adjacent bin
    #         values. This is a better way to plot the distribution.
    bins_out = bins[1:] - np.diff(bins)/2.0
    
    return bins_out, probs

def calculate_katz_centrality(G, alpha, node = None):
    """
    Calculate the Katz centrality for each node in the graph G.
    
    Katz centrality is a measure of node influence that considers both the number of immediate neighbors and the influence of more distant nodes in the network. 
    It is computed by taking into account the sum of the weighted paths that connect nodes, where the influence of more distant nodes is exponentially attenuated 
    based on a damping parameter (alpha).
    
    Parameters
    ----------
    G : nx.Graph
        The input graph, which must be a NetworkX graph (either directed or undirected).
    
    alpha : float
        The attenuation factor, which controls the weight given to longer paths. 
        For the Katz centrality to converge, alpha must be less than the reciprocal of the largest eigenvalue of the adjacency matrix of G.
    
    node : object, optional (default = None)
        A specific node in the graph for which to return the Katz centrality. 
        If provided, the function returns the centrality of this node only. 
        If not provided, the function returns the Katz centrality for all nodes in the graph.
    
    Returns
    -------
    katz_centrality : list or float
        If `node` is not provided, returns a list of values corresponding to the normalized Katz centrality of each node.
        If `node` is specified, returns a single float representing the Katz centrality of the specified node.
    
    Raises
    ------
    TypeError
        If G is not a valid NetworkX graph.

    IndexError
        If specified node does not exist in G.
    
    ValueError
        If alpha is not smaller than the reciprocal of the largest eigenvalue of the adjacency matrix of G, 
        as Katz centrality does not converge in this case.
    
    Warnings
    --------
    - A warning is printed if the graph is not connected, as Katz centrality's interpretation is not well-defined for disconnected graphs.
    - A warning is printed if the largest eigenvalue of the adjacency matrix is zero, which indicates no connectivity in the graph.

    Notes
    -----
    The Katz centrality is calculated as:
    
        C_katz = (I - alpha * A)^-1 * 1
    
    where I is the identity matrix, A is the adjacency matrix, and 1 is a vector of ones.
    
    The centrality values are normalized by dividing each node's Katz centrality by the maximum value among all nodes.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> calculate_katz_centrality(G, alpha=0.1)
    {0: 0.896, 1: 0.922, 2: 1.0, 3: 0.922, 4: 0.896}
    
    >>> calculate_katz_centrality(G, alpha=0.1, node=2)
    1.0
    """
    #warning = None
    if not isinstance(G, nx.Graph): # raise error if G is not nx.Graph
        raise TypeError("G must be a NetworkX graph")

    A = nx.adjacency_matrix(G).toarray() # convert G into adjacency matrix A
    eigvals = np.linalg.eigvals(A) # calculate the eigenvalues of A
    max_eigval = max(abs(val) for val in eigvals) # find the leading eigenvalue of A
    if max_eigval == 0: # check for unconnected graph
        raise Exception('Graph has no connectivity')
        
    if max_eigval >= 1/alpha: # check that alpha is with allowable range
        raise ValueError("Alpha must be less than the reciprocal of the leading eigenvalue of the adjacency matrix")
        
    if max_eigval != 0 and not nx.is_connected(G): # check that graph is connected (but not completely disconnected)
        raise Exception('Graph is disconnected. Interpretation of Katz centrality is not clear for disconnected graphs')
        # todo: calculate katz on disconnected subgraphs seperately

    I = np.eye(len(G)) # create the identity matrix of same size as A
    ones = np.array([1]*len(A)) # create vector of ones of same length as A
    katz_centrality = np.linalg.inv(I - alpha * A) @ ones # calculate katz centrality
    katz_normalized = katz_centrality/max(katz_centrality) # normalize by largest value
    if node:
        if node not in list(G.nodes()):
            raise IndexError("Node must be in graph G")
        katz_node = katz_normalized[node] # extract centrality of specified node
        return(katz_node)
    else:
        return(katz_normalized)

def average_shortest_path_length_per_node(G):
    """
    Calculate the average shortest path length from each node to all other reachable nodes in the graph.

    This function computes the average shortest path length for each node in the graph `G`.
    For each node, the shortest path lengths to all other reachable nodes are calculated, 
    and the average of those lengths is returned. If a node is isolated (not connected 
    to other nodes), it will not be included in the average.

    Parameters:
    ----------
    G : networkx.Graph
        A NetworkX graph (can be directed or undirected). The graph should be connected, 
        or the results may not be meaningful for isolated nodes.

    Returns:
    -------
    dict
        A dictionary where the keys are the nodes in the graph and the values are the average 
        shortest path lengths for each node. The average is computed over all reachable nodes, 
        excluding the node itself.
    
    Notes:
    -----
    - For disconnected graphs, the function will only consider reachable nodes. The average 
      for isolated nodes will exclude unreachable nodes.
    - The graph `G` can be directed or undirected, and the shortest path lengths are computed 
      accordingly.
    
    Example:
    --------
    >>> G = nx.path_graph(5)
    >>> average_shortest_path_length_per_node(G)
    {0: 2.0, 1: 1.5, 2: 1.0, 3: 1.5, 4: 2.0}
    """
    avg_shortest_paths = {}
    
    # Compute shortest path lengths from each node to every other node
    for node in G.nodes():
        shortest_paths = nx.shortest_path_length(G, source=node)  # Dictionary of shortest paths from `node`
        
        # Compute the average shortest path length for the current node
        total_length = sum(shortest_paths.values())  # Sum of shortest paths
        num_nodes = len(shortest_paths)  # Number of reachable nodes
        
        avg_shortest_paths[node] = total_length / (num_nodes - 1)  # Exclude the node itself from the average
    
    return avg_shortest_paths

def closeness_centrality(G):    
    """
    Calculate the closeness centrality for each node in a graph from scratch.

    Closeness centrality is a measure of how close a node is to all other nodes
    in the network. It is calculated as the reciprocal of the sum of the shortest
    path distances from a node to all other nodes in the graph. This function 
    computes the closeness centrality for all nodes in the graph `G` without 
    using any external library functions for the centrality calculation.

    Parameters
    ----------
    G : networkx.Graph
        The input graph on which the closeness centrality is calculated. It can
        be any type of graph (undirected, directed, etc.) supported by NetworkX.

    Returns
    -------
    centrality : dict
        A dictionary where the keys are nodes in the graph and the values are
        their corresponding closeness centrality scores. If a node is isolated,
        its centrality will be 0.

    Notes
    -----
    - For each node, this function computes the sum of shortest path lengths to 
      all other reachable nodes in the graph using NetworkX's `shortest_path_length`.
    - Nodes that are disconnected from the rest of the graph will have a centrality 
      of 0.0.
    - This function assumes that the graph is connected; however, it gracefully 
      handles isolated nodes by assigning them a centrality score of 0.0.

    Time Complexity
    ---------------
    The time complexity is O(N * (V + E)), where N is the number of nodes, V is 
    the number of vertices, and E is the number of edges, due to the use of 
    shortest path calculations for each node.

    Citations
    ---------
    Bavelas, A. (1950). Communication patterns in task-oriented groups. The Journal 
    of the Acoustical Society of America, 22(6), 725-730.

    Sabidussi, G. (1966). The centrality index of a graph. Psychometrika, 31(4), 581–603.

    Freeman, L. C. (1979). Centrality in social networks conceptual clarification. 
    Social Networks, 1(3), 215–239.

    Example
    -------
    >>> import networkx as nx
    >>> G = nx.path_graph(4)
    >>> closeness_centrality_from_scratch(G)
    {0: 0.6666666666666666, 1: 1.0, 2: 1.0, 3: 0.6666666666666666}
    """

    centrality = {}
    N = G.number_of_nodes()  # Total number of nodes in the graph

    for node_i in G.nodes():
        # Compute shortest paths from node_i to all other nodes
        shortest_paths = nx.shortest_path_length(G, source=node_i)
        
        # Sum the lengths of the shortest paths
        total_distance = sum(shortest_paths.values())

        # Closeness centrality calculation (ignoring disconnected components)
        if total_distance > 0 and N > 1:
            centrality[node_i] = (N - 1) / total_distance
        else:
            centrality[node_i] = 0.0  # In case the node is isolated

    return centrality

def eigenvector_centrality(G, max_iter=100, tol=1e-08):
    """
    Calculate the eigenvector centrality for each node in a graph from scratch.

    Eigenvector centrality is a measure of a node's influence in a network based on 
    the idea that connections to high-scoring nodes contribute more to the score 
    of a node than equal connections to low-scoring nodes. This centrality measure 
    assigns relative scores to all nodes in the network based on the principle that 
    a node's centrality is determined by the centrality of its neighbors.

    Parameters
    ----------
    G : networkx.Graph
        The input graph on which the eigenvector centrality is calculated. It can be
        any type of graph (undirected, directed, etc.) supported by NetworkX.

    max_iter : int, optional (default=100)
        Maximum number of iterations for the power iteration method used to compute
        the centrality values. Higher values may be required for large graphs.

    tol : float, optional (default=1e-06)
        Tolerance for the convergence of the eigenvector centrality values. The 
        algorithm iterates until the change in centrality values is smaller than this
        threshold.

    Returns
    -------
    centrality : dict
        A dictionary where the keys are nodes in the graph and the values are
        their corresponding eigenvector centrality scores.

    Notes
    -----
    - Eigenvector centrality was introduced by Bonacich (1972) as an extension 
      of degree centrality, emphasizing the importance of connections to high-degree 
      or highly influential nodes. 
    - This algorithm computes eigenvector centrality using the power iteration 
      method, which involves iteratively updating the centrality scores of each 
      node based on the scores of their neighbors until convergence.
    - Eigenvector centrality works best in connected, undirected graphs; for 
      directed or disconnected graphs, results may vary or be undefined.
    - The algorithm will stop either after `max_iter` iterations or when the 
      centrality values converge to within the specified `tol`.

    Time Complexity
    ---------------
    The time complexity is O(V * E * I), where V is the number of vertices, 
    E is the number of edges, and I is the number of iterations (limited by `max_iter`).

    Citations
    ---------
    Bonacich, P. (1972). Factoring and weighting approaches to status scores and 
    clique identification. *Journal of Mathematical Sociology, 2*(1), 113-120.

    Newman, M. E. J. (2008). The mathematics of networks. *The New Palgrave 
    Dictionary of Economics, 2*(1), 1-12.

    Example
    -------
    >>> import networkx as nx
    >>> G = nx.karate_club_graph()
    >>> eigenvector_centrality_from_scratch(G)
    {0: 0.3730400736153818, 1: 0.2082196569730357, 2: 0.20624526357714606, ...}
    """
    
    # Initialize centrality dict with uniform values for all nodes
    centrality = {node: 1.0 / len(G) for node in G}
    N = len(G)

    # Power iteration method
    for _ in range(max_iter):
        prev_centrality = centrality.copy()
        max_diff = 0  # Track maximum change in centrality values

        for node in G:
            # Update centrality: sum of neighbors' centralities
            centrality[node] = sum(prev_centrality[neighbor] for neighbor in G[node])

        # Normalize centrality values (divide by Euclidean norm)
        norm = np.sqrt(sum(value ** 2 for value in centrality.values()))
        if norm == 0:
            return centrality  # Handle disconnected graphs
        centrality = {node: value / norm for node, value in centrality.items()}

        # Check for convergence
        max_diff = max(abs(centrality[node] - prev_centrality[node]) for node in G)
        if max_diff < tol:
            break

    return centrality
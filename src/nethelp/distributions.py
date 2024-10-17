import numpy as np
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
    Compute the average shortest path length for each node in the graph G.
    
    :param G: NetworkX graph (can be directed or undirected)
    :return: Dictionary where keys are nodes and values are the average shortest path lengths.
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
# nethelp

[![PyPI - Version](https://img.shields.io/pypi/v/nethelp.svg)](https://pypi.org/project/nethelp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nethelp.svg)](https://pypi.org/project/nethelp)

-----
`nethelp` is a Python package for network analysis and color utilities. The package includes various graph-related functions, such as computing degree distributions, running graph algorithms, and performing shortest path calculations. It also provides utilities for handling colorblindness and color conversions.



## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [License](#license)

## Installation
To install the package, clone the repository, cd to the directory and use pip:
```console
git clone https://github.com/nmoghaddas19/nethelp.git 
cd nethelp 
pip install .
```

## Features 

### Graph Algorithms and Network Analysis
`bfs(explore_queue, nodes_visited, graph)`
- Implements a recursive breadth-first search (BFS) algorithm. Starting from a given node, it explores the graph, keeping track of visited nodes and the shortest paths to all other nodes.

`dfs(explore_stack, nodes_visited, graph)`

- Implements a recursive depth-first search (DFS) algorithm. It explores as far as possible along a branch before backtracking, similarly keeping track of visited nodes and paths.

`average_shortest_path_length_per_node(G)`

- Computes the average shortest path length from each node to all other reachable nodes in the graph G.

`degree_distribution(G, number_of_bins=15, log_binning=True, density=True, directed=False)`

- Calculates the degree distribution of the graph G. Supports log binning for logarithmic plots, and both in-degree and out-degree distributions for directed graphs.

`calculate_katz_centrality(G, alpha, node = None)`
- Calculate the Katz centrality for each node in the graph G.

`average_shortest_path_length_per_node(G)`
- Calculate the average shortest path length from each node to all other reachable nodes in the graph.

`def closeness_centrality(G)`
- Calculate the closeness centrality for each node in a graph

`eigenvector_centrality(G, max_iter=100, tol=1e-08)`
- Calculate the eigenvector centrality for each node in a graph

### Color utilities 
`get_colorblindness_colors(hex_col, colorblind_types='all')`

Simulates how a given color appears to different types of colorblindness. Supports a range of colorblind types like protanopia, deuteranopia, and grayscale.

`rgb_to_hsv(rgb)`

- Converts an RGB color to HSV format.

`rgb_to_hex(rgb)`

- Converts an RGB tuple to a hex color code.

`hex_to_rgb(hex_col)`

- Converts a hex color code to an RGB tuple.

`hex_to_grayscale(hex_col)`

- Converts a hex color code to its grayscale equivalent.

`lightness(hex_col)`

- Computes the perceived lightness of a color.

`saturation(hex_col)`

- Calculates the saturation of a color, from 0 (unsaturated) to 1 (fully saturated).

`hue(hex_col)`

- Returns the hue of a color in degrees (0 to 360).



## Usage
After installing, import the package and use the functions as needed:
```python
import nethelp as nh
import networkx as nx

# Example: Calculate degree distribution
G = nx.erdos_renyi_graph(100, 0.05)
bins, probs = nh.distributions.degree_distribution(G)

# Example: Convert RGB to Hex
hex_color = nh.vis.rgb_to_hex((255, 0, 0))
```



## License

`nethelp` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


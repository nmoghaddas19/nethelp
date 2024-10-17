%pwd
import os
os.chdir('nethelp/')
%pwd
pip install .

import networkx as nx
import nethelp 
import numpy as np
# import numpy as np

print(dir(nethelp))

G = nx.erdos_renyi_graph(100, 0.05)
nethelp.distributions.degree_distribution(G)

gt = nethelp.convert.nx2gt(G)
# from nethelp.distributions import degree_distribution
# degree_distribution()

nethelp.distributions.degree_distribution()
nethelp.degree_distribution()

nethelp.vis.hex_to_rgb('ffffff')

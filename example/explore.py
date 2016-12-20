'''
Script to develop code for displaying tree diagram of references dependecies
'''

import bib_network as bn

bibfile = 'example/cornice.bib'

# Quick default method:
bn.bib2plot(bibfile)

# for more control, and getting insight data
ref_dict = bn.read_bib2dict(bibfile)
G = bn.initialize_network(ref_dict)
node_color_vec, cm = bn.node_coloring('Blues', G)
nnode = bn.node_size(G)
bn.plot_net(G, node_color_vec, cm, nnode*2)
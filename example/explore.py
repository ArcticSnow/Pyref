'''
Script to develop code for displaying tree diagram of references dependecies

'''
from __future__ import division
import networkx as nx
import bibtexparser
import time
import numpy as np
import matplotlib.pyplot as plt


bibfile = 'example/cornice.bib'

# load
with open(bibfile) as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)
ref_dict = bib_database.get_entry_dict()

# initialize anc extract value for the networkx object ( extract nodes and relationship)
G = nx.DiGraph()
for k in ref_dict.keys()[1:]:
    G.add_node(ref_dict.get(k).get('author').split(',')[0] + ' ' + ref_dict.get(k).get('year'))
    print 'key: ' + k

for k in ref_dict.keys():
    if [a for a in ref_dict.get(k).keys() if a == 'parent'] == [u'parent']:

        parent = ref_dict.get(k).get('parent').split(', ')
        print k
        print parent

        for par in parent:
            print par
            G.add_edge(ref_dict.get(par).get('author').split(',')[0] + ' ' + ref_dict.get(par).get('year'),
                       ref_dict.get(k).get('author').split(',')[0] + ' ' + ref_dict.get(k).get('year'))
            time.sleep(.01)
    else:
        print k + ' has no parents'
pos = nx.spring_layout(G)

# Extract year of nodes for coloring nodes in function of year
mynode = np.array(G.nodes()).astype(str)
nodeY = mynode
def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))
for i,y in enumerate(mynode):
    nodeY[i] = get_num(y)
nodeY = nodeY.astype(int)
cm = plt.cm.get_cmap('Paired')

# node size, ===== need to change to the number a paper is cited
nnode = np.array(G.degree().values())+1
nnode = np.round(nnode/nnode.max()*1500)

# draw network
pos=nx.nx_agraph.graphviz_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=nnode+800, node_color=nodeY, cmap=cm)
nx.draw_networkx_edges(G, pos, arrows=True)
nx.draw_networkx_labels(G, pos)

# add colorbar to plot
sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=nodeY.min(), vmax=nodeY.max()))
sm._A = []
plt.colorbar(sm)

# remove tick from plot
plt.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    left='off',
    right='off',
    labelbottom='off',
    labelleft='off')

plt.show()
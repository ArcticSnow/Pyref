'''
Functions to plot reference connection
'''

from __future__ import division
import networkx as nx
import bibtexparser
import time
import numpy as np
import matplotlib.pyplot as plt


def read_bib2dict(bibfile):
    # load custom bib file
    with open(bibfile) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    ref_dict = bib_database.get_entry_dict()
    return ref_dict

def initialize_network(ref_dict):
    '''
    initialize anc extract value for the networkx object ( extract nodes and relationship)

    :param ref_dict: python dictionnary from read_bib2dict()
    :return: G
    '''

    G = nx.DiGraph()
    for k in ref_dict.keys()[1:]:
        if ref_dict.get(k).get('author').split('and').__len__() == 1:
            node = ref_dict.get(k).get('author').split(',')[0] + '\n(' + ref_dict.get(k).get('year') + ')'

        elif ref_dict.get(k).get('author').split('and').__len__() == 2:
            second_author = ref_dict.get(k).get('author').split('and')[1]
            node = ref_dict.get(k).get('author').split(',')[0] + ' and ' + second_author.split(',')[
                0] + '\n(' + ref_dict.get(k).get('year') + ')'

        else:
            node = ref_dict.get(k).get('author').split(',')[0] + ' et al.\n(' + ref_dict.get(k).get('year') + ')'
        G.add_node(node)
        print 'key: ' + k

    for k in ref_dict.keys():
        if [a for a in ref_dict.get(k).keys() if a == 'parent'] == [u'parent']:

            parent = ref_dict.get(k).get('parent').split(', ')
            print k
            print parent

            if ref_dict.get(k).get('author').split('and').__len__() == 1:
                nodeK = ref_dict.get(k).get('author').split(',')[0] + '\n(' + ref_dict.get(k).get('year') + ')'
            elif ref_dict.get(k).get('author').split('and').__len__() == 2:
                second_author = ref_dict.get(k).get('author').split('and')[1]
                nodeK = ref_dict.get(k).get('author').split(',')[0] + ' and ' + second_author.split(',')[0] + '\n(' + ref_dict.get(k).get('year') + ')'
            else:
                nodeK = ref_dict.get(k).get('author').split(',')[0] + ' et al.\n(' + ref_dict.get(k).get('year') + ')'


            for par in parent:
                print par

                if ref_dict.get(par).get('author').split('and').__len__() == 1:
                    nodePAR = ref_dict.get(par).get('author').split(',')[0] + '\n(' + ref_dict.get(par).get('year') + ')'
                elif ref_dict.get(par).get('author').split('and').__len__() == 2:
                    second_author = ref_dict.get(par).get('author').split('and')[1]
                    nodePAR = ref_dict.get(par).get('author').split(',')[0] + ' and ' + second_author.split(',')[
                        0] + '\n(' + ref_dict.get(par).get('year') + ')'
                else:
                    nodePAR = ref_dict.get(par).get('author').split(',')[0] + ' et al.\n(' + ref_dict.get(par).get('year') + ')'

                G.add_edge(nodePAR, nodeK)
                time.sleep(.01)
        else:
            print k + ' has no parents'
    return G

def node_coloring(ColMap, G):
    '''
    Define coloramp for coloring the nodes
    :param ColMap: string of the colormap to use. See http://matplotlib.org/users/colormaps.html
    :param G: Networkx object from initialize_network()
    :return: node_color_vector, cm
    '''

    # Extract year of nodes for coloring nodes in function of year
    mynode = np.array(G.nodes()).astype(str)
    node_colvec = mynode
    def get_num(x):
        return int(''.join(ele for ele in x if ele.isdigit()))
    for i,y in enumerate(mynode):
        node_colvec[i] = get_num(y)
    node_colvec = node_colvec.astype(int)
    cm = plt.cm.get_cmap(ColMap)
    return node_colvec, cm


def node_size(G, method='cited by', size_base=500, size_var=2000):
    node_in = np.array(G.in_degree().values()) + 1
    node_out = np.array(G.out_degree().values()) + 1

    for i,k in enumerate(G.nodes()):
        node_in[i] = G.in_degree().get(k) +1
        node_out[i] = G.out_degree().get(k) + 1

    if method == 'cited by':
        nnode = np.round(node_out / node_out.max() * size_var) + size_base

    elif method == 'citing':
        nnode = np.round(node_in / node_in.max() * size_var) + size_base

    return nnode


def plot_net(G, node_color_vec, cm, nnode):
    plt.figure(facecolor='white')
    # draw network
    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=nnode, node_color=node_color_vec, cmap=cm)
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_labels(G, pos)

    # add colorbar to plot
    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=node_color_vec.min(), vmax=node_color_vec.max()))
    sm._A = []
    plt.colorbar(sm)

    plt.axis('off')
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

def bib2plot(bibfile):
    '''
    Default setting to plot
    :param bibfile:
    :return:
    '''

    ref_dict = read_bib2dict(bibfile)
    G = initialize_network(ref_dict)
    node_color_vec, cm = node_coloring('Paired', G)
    nnode = node_size(G)
    plot_net(G, node_color_vec, cm, nnode)



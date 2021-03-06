from network import Network
import random

from scipy.sparse import csr_matrix
from allensdk.config.model.formats.hdf5_util import Hdf5Util

import numpy as np
import pandas as pd
import csv

# probabilities of establishing a connection from source -> target
connection_probabilities = { 
    ('excitatory', 'excitatory'): .75,
    ('excitatory', 'inhibitory'): .25,
    ('inhibitory', 'inhibitory'): .1,
    ('inhibitory', 'excitatory'): .5
}


def construct_matrix(connections):
    ''' turn a list of connection dictionaries into a numpy csr matrix '''
    rows = [ c['source'] for c in connections ]
    cols = [ c['target'] for c in connections ]
    data = [ c['weight'] for c in connections ]

    return csr_matrix((data, (rows, cols)))


def random_connectivity(src_i, tgt_i, source, target):
    ''' given a source target pair, create a connection (or not) '''
    p = connection_probabilities[source['type'],target['type']]
    if random.random() < p:
        return { 'weight': random.random() }


# initialize the network
net = Network()

# add some populations
net.add_population(10, type='inhibitory')
net.add_population(30, type='excitatory')

# add the connectivity rule
net.connect(random_connectivity) 

# build the matrix
cells, connections = net.build()

# turn it into a sparse matrix
m = construct_matrix(connections)

# the connectivity to hdf5
Hdf5Util().write('connections.h5', m)

# write the cell info to csv
cells = pd.DataFrame.from_dict(cells)
cells.to_csv('cells.csv', index=False)


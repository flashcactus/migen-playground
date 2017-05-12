#!/usr/bin/python3
import random
import itertools
import neural_net
import math

def normgauss(maxval):
    def ng():
        r = random.gauss(0,maxval/4)
        if abs(r) > maxval:
            return 0
        else:
            return r
    return ng

def randlayer(prev_start, start, num_neurons, num_connections, randfunc = lambda:0):
    '''generates a neural net layer with connections to the previous layer'''
    #generate the connections first
    from_indices = range(prev_start, start)
    to_indices = range(start, start+num_neurons)
    #edges = random.sample(list(itertools.product(from_indices,to_indices)), num_connections)
    edges = set()
    for neur in from_indices:
        edges.add((neur,random.choice(to_indices)))
    for neur in to_indices:
        edges.add((random.choice(from_indices), neur))
    possible_edges = set(itertools.product(from_indices, to_indices)) - edges
    try:
        edges.update(set(random.sample(possible_edges, num_connections-len(edges))))
    except ValueError:
        pass
    rconns = {n:[] for n in to_indices}
    for e in edges:
        rconns[e[1]].append(e[0])
    #return [(a,rconns[a]) for a in rconns]
    neurons = [
        neural_net.neuron_desc(rconns[n], [randfunc() for r in range(len(rconns[n]))], randfunc())
        for n in to_indices
    ]
    return neurons,len(edges)


def randgraph_layered(input_count, layer_counts, con_density, connum_func=lambda a,b,r:a*b*r, randfunc=lambda:0):
    start = -input_count
    nexts = 0
    neurons = []
    layers = []
    edge_count = 0
    for lc in layer_counts:
        new_layer, new_edge_c = randlayer(start, nexts, lc, math.ceil(connum_func(nexts - start, lc, con_density)), randfunc)
        neurons += new_layer
        edge_count += new_edge_c
        start = nexts
        nexts = start + lc
    outputs = list(range(start,nexts))
    return neurons,outputs,edge_count


def rectnet(width, depth, density, fp_widths):
    graph,outputs,edge_cnt = randgraph_layered(width,[width]*depth,density,randfunc=normgauss(2**fp_widths[0]))
    print("Rectnet: instantiated net with",len(graph),"neurons and",edge_cnt,"edges")
    return neural_net.StaticNN(width,graph,outputs,*fp_widths)



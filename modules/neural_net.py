#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import periph
import neuro


class neuron_desc:
    def __init__(self,inputs=[],weights=[],bias=0,actfun_constructor=neuro.pseudosigmoid_tanh):
        '''
        structure describing a neuron in a net and its connections.
        inputs[a] == b:
            if b >= 0:
                a'th input of this neuron connected to output of b'th neuron
            else (b < 0 or not an int):
                a'th input of this neuron connected to network input labeled 'b'
                [-b if b is a number]
        '''
        self.inputs = inputs
        self.weights = weights
        self.bias = bias
        self.actfun = actfun_constructor

    def __repr__(self):
        return 'neural_net.neuron_desc({}, {}, {}, {})'.format(self.inputs,self.weights,self.bias,repr(self.actfun))


class StaticNN (Module):
    def __init__(self,input_cnt,neurons,outputs,int_width,frac_width):
        self.inputs = [neuro.sgnsig(int_width + frac_width) for i in range(input_cnt)]
        self.outputs = []

        ###

        #construct the neurons
        self.submodules.neurons = [
            neuro.static_neuron(
                neuro.weighted_sum(int_width,frac_width,len(n.weights)),
                n.actfun(int_width,frac_width),
                map(lambda a:neuro.float2fix(a,frac_width),n.weights),
                neuro.float2fix(n.bias,frac_width),
                int_width,
                frac_width
            )
            for n in neurons]

        
        #connect them together and connect the inputs
        for neu_n,ndesc in enumerate(neurons):
            for inp_n,source in enumerate(ndesc.inputs):
                if isinstance(source, int):
                    if source >= 0:#input from another neuron
                        print('.',end='')
                        self.comb += self.neurons[neu_n].inputs[inp_n].eq(self.neurons[source].output)
                        continue
                    else:
                        source = -source-1;
                #add the input if it's not there
                print(',',end='')
                '''
                if source not in self.inputs:
                    self.inputs[source] = neuro.sgnsig(int_width + frac_width)
                '''
                #connect the neuron input to corresponding net input
                self.comb += self.neurons[neu_n].inputs[inp_n].eq(self.inputs[source])

        #check whether all the inputs are actually sequentially numbered, i.e. an array
        '''
        if False not in (isinstance(key, int) for key in self.inputs) and False not in (i == v for i,v in enumerate(sorted(b)):

            self.input_l = [b[i] for i in sorted(b)]
        '''

        #create & connect the outputs
        for o_src in outputs:
            self.outputs.append(neuro.sgnsig(int_width + frac_width))
            self.comb += self.outputs[-1].eq(self.neurons[o_src].output)
    

class LayeredSyncNN (Module):
    def __init__(self,input_cnt,layers,int_width,frac_width):
        self.inputs = [neuro.sgnsig(int_width + frac_width) for i in range(input_cnt)]

        # construct the neurons, in layers this time
        self.submodules.neurons = [
            [
            neuro.static_neuron(
                neuro.weighted_sum(int_width,frac_width,len(n.weights)),
                n.actfun(int_width,frac_width),
                map(lambda a:neuro.float2fix(a,frac_width),n.weights),
                neuro.float2fix(n.bias,frac_width),
                int_width,
                frac_width
            )
            for n in layer]
        for layer in layers]

        #connect the layers together
        for layer_n, layer in enumerate(layers):
            for neuron_n, ndesc in enumerate(layer):
                for inp_n, inp_src in enumerate(ndesc.inputs):
                    if inp_src >= 0:
                        self.sync += self.neurons[layer_n][neuron_n].inputs[inp_n].eq(self.neurons[layer_n-1][inp_src].output if layer_n >= 1 else self.inputs[inp_src])
                        continue
                    else:
                        raise KeyError("source indices must be nonnegative in layered net")

        #create & connect the outputs (w/o latching)
        self.outputs = [neuro.sgnsig(int_width + frac_width) for i in range(len(layers[-1]))]
        self.comb += [self.outputs[i].eq(self.neurons[-1][i].output) for i in range(len(layers[-1]))]

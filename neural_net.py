
#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import periph
import neuro


class neuron_desc:
    def __init__(self,inputs=[],weights=[],bias=0,actfun_constructor=neuro.pseudosigmoid_tanh):
        '''
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


class StaticNN (Module):
    def __init__(self,neurons,outputs,int_width,frac_width):
        self.inputs = {}
        self.outputs = []

        ###

        #construct the neurons
        self.neurons = [
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
        for ndesc,neu in zip(neurons,self.neurons):
            for inp_n,source in enumerate(ndesc.inputs):
                if isinstance(source, int):
                    if source >= 0:#input from another neuron
                        print('.')
                        self.comb += neu.inputs[inp_n].eq(self.neurons[source].output)
                        continue
                    else:
                        source = -source;
                #add the input if it's not there
                if source not in self.inputs:
                    self.inputs[source] = neuro.sgnsig(int_width + frac_width)
                #connect the neuron input to corresponding net input
                self.comb += neu.inputs[inp_n].eq(self.inputs[source])

        #check whether all the inputs are actually sequentially numbered, i.e. an array
        '''
        if False not in (isinstance(key, int) for key in self.inputs) and False not in (i == v for i,v in enumerate(sorted(b)):

            self.input_l = [b[i] for i in sorted(b)]
        '''

        #create & connect the outputs
        for o_src in outputs:
            self.outputs.append(neuro.sgnsig(int_width + frac_width))
            self.comb += self.outputs[-1].eq(self.neurons[o_src].output)
            


class _top(Module):
    def __init__(self,plat):
        pass




if __name__ == '__main__':
    import builder as brd
    import sys

    if sys.argv[1][0].lower() == 'b':
        brd.build(_top(brd.plat))         

    brd.flash()


#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import periph
from mystuff import *

def float2fix(num,frac_width):
    '''convert a python number to the appropriate fixed-point representation'''
    return int(num*2**frac_width)

def sgnsig(width,*args,**kwargs):
    '''shorthand for creating signed signals'''
    return Signal((width,True),*args,**kwargs)

class fp_multiplier(Module):
    '''module for multiplying fixed point stuff'''
    def __init__(self, int_width, frac_width):
        if int_width<0 or frac_width<0:
            raise ValueError("int_width and frac_width must be non-negative")
        width=int_width+frac_width
        self.a = sgnsig(width)
        self.b = sgnsig(width)
        self.result = sgnsig(2*int_width + frac_width)

        ###

        wide_result = sgnsig(width*2)

        self.comb += wide_result.eq(self.a * self.b)
        self.comb += self.result.eq(wide_result[frac_width:])

class weighted_sum(Module):
    '''sum(input*weight for input, weight in zip(inputs,weights)) + bias'''
    def __init__(self, int_width, frac_width, num_inputs=0):
        self.sigw = int_width + frac_width
        self.mulw = 2*int_width + frac_width
        self.int_width = int_width
        self.frac_width = frac_width

        self.inputs = []
        self.winputs = []

        self.weights = []
        self.bias = sgnsig(self.sigw)

        self.output = sgnsig(self.mulw)

        for i in range(num_inputs):
            self.add_input()

    def add_input(self):
        '''add and return a new input'''
        self.inputs.append(sgnsig(self.sigw))
        self.winputs.append(sgnsig(self.mulw))
        self.weights.append(sgnsig(self.sigw))

        ###

        mul = fp_multiplier(self.int_width,self.frac_width)
        self.submodules += mul

        ###

        self.comb += mul.a.eq(self.inputs[-1])
        self.comb += mul.b.eq(self.weights[-1])
        self.comb += self.winputs[-1].eq(mul.result)

        return self.inputs[-1]
    
    def do_finalize(self):
        print('wsum: finalize called')
        s = self.bias
        for winp in self.winputs:
            s = s+winp
        #    print(s)
        self.comb += self.output.eq(s)
        

class pseudosigmoid_tanh(Module):
    '''somewhat approximates a tanh sigmoid with linear functions'''
    def __init__(self, int_width, frac_width, include_deriv=False, min_deriv=1):
        self.int_width = int_width
        self.frac_width = frac_width
        self.sigw = int_width + frac_width

        self.input = sgnsig(self.sigw)
        self.output = sgnsig(self.sigw)
        
        self.in_mul75 = sgnsig(self.sigw)
        self.submodules.mul75 = fp_multiplier(int_width, frac_width)

        ###

        #hook up the multiplier
        self.comb += [
            self.mul75.a.eq(self.input),
            self.mul75.b.eq(float2fix(0.75,self.frac_width)),
            self.in_mul75.eq(self.mul75.result)
        ]

        #do the sigmoid
        self.comb += [
            If( self.in_mul75 > float2fix(1,self.frac_width),
                self.output.eq(float2fix(1,self.frac_width))
            ).Elif( self.in_mul75 < float2fix(-1,self.frac_width),
                self.output.eq(float2fix(-1,self.frac_width))
            ).Else(
                self.output.eq(self.in_mul75)
            )
        ]

        ###

        if include_deriv:
            # compute an approximation of the derivative of a tanh
            self.deriv = sgnsig(self.sigw)
            self.outsqfun = sgnsig(self.sigw)

            #add another multiplier
            self.submodules.sqrmul = fp_multiplier(int_width, frac_width)
            #hook it up to compute 1-f(x)^2
            self.comb += [
                self.sqrmul.a.eq(self.output),
                self.sqrmul.b.eq(self.output),
                self.outsqr.eq(float2fix(1,self.frac_width) - self.sqrmul.result)
            ]

            #deriv := max(min_deriv, 1-f(x)^2)
            self.comb += [
                If( self.outsqr > min_deriv,
                    self.deriv.eq(self.outsqr)
                ).Else(
                    self.deriv.eq(min_deriv)
                )
            ]


class static_neuron(Module):
    def __init__(self, wsum, actfun, weights, bias, int_width, frac_width):
        self.submodules.wsum = wsum
        self.submodules.actfun = actfun
        self.inputs = wsum.inputs
        self.output = self.actfun.output
        
        #
        
        #assign the weights statically
        self.comb += [wg_inp.eq(static_wg) for wg_inp,static_wg in zip(wsum.weights,weights)]
        self.comb += wsum.bias.eq(bias)

        self.comb += self.actfun.input.eq(self.wsum.output)
        


if __name__ == '__main__':
    import builder as brd
    import sys

    if sys.argv[1][0].lower() == 'b':
        brd.build(_top(brd.plat))         

    brd.flash()


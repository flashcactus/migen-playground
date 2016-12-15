#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import periph
from mystuff import *

def sgnsig(width,*args,**kwargs):
    return Signal((width,true),*args,**kwargs)

class fp_multiplier(Module):
    def __init__(self, int_width, frac_width):
        if int_width<0 or frac_width<0:
            raise ValueError("int_width and frac_width must be non-negative")
        width=int_width+frac_width
        a = sgsig(width)
        b = sgsig(width)
        result = sgsig(2*int_width + frac_width)

        ###

        wide_result = sgsig(width*2)

        self.comb += wide_result.eq(a * b)
        self.comb += result.eq(wide_result[frac_width:])

class weighted_sum(Module):
    def __init__(self, int_width, frac_width):
        self.sigw = int_width + frac_width
        self.widths = (int_width, frac_width)

        self.inputs = []
        self.winputs = []

        self.weights = []
        self.bias = sgsig(self.sigw)

        self.output = sgsig(self.sigw)

    def add_input():
        inp = sgsig(self.sigw)
        winp = sgsig(self.sigw)
        wght = sgsig(self.sigw)

        self.inputs.append(inp)
        self.winputs.append(winp)
        self.weights.append(wght)

        ###

        mul = fp_multiplier(*self.widths)
        self.submodules += mul

        ###

        self.comb += mul.a.eq(inp)
        self.comb += mul.b.eq(wght)
        self.comb += winp.eq(mul.result)

        return inp
    
    def do_finalize():
        s = self.bias
        for winp in self.winputs:
            s = s+winp
        self.comb += self.output.eq(s)
        

if __name__ == '__main__':
    import builder as brd
    import sys

    if sys.argv[1][0].lower() == 'b':
        brd.build(_top(brd.plat))         

    brd.flash()


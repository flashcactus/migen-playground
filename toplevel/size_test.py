#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

from modules import mystuff
from modules import periph
import modules.neuro as neuro
from modules import neural_net 
from modules import randnet

import math

fpga_clk_freq = int(50e6)



class _top(Module):
    def __init__(self,plat,nwidth,ndepth,ndens,fpwidths):
        digits = [plat.request("seven_seg",n) for n in range(6)] 
        leds = Cat([plat.request("user_led",n) for n in range(10)])
        btns = [plat.request("key",i) for i in range(4)]
        switches = [plat.request("sw",i) for i in range(10)]

        sigwidth = fpwidths[0]+fpwidths[1] 


        self.submodules.net = randnet.rectnet(nwidth, ndepth, ndens, fpwidths)

        self.submodules.lfsr = mystuff.LFSR(max(16,sigwidth),[0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1])
        self.submodules.shifter = mystuff.WideShiftReg(sigwidth,nwidth)

        ###

        #feed the PRS into the shifter
        self.comb += self.shifter.serial_in.eq(self.lfsr.vec)
        self.cntr = Signal(max=sigwidth)
        
        self.sync += If(cntr == 0,
            self.shifter.shift_clk.eq(1)
            self.cntr.eq(sigwidth)
        ).Else(
            self.cntr.eq(self.cntr - 1)
        )

        
        #feed the shifter int the net
        self.sync += [inp.eq(self.shifter.array[i]) for i,inp in enumerate(self.net.inputs)]
        

        #feed diagnostics out
        cksum = 0
        for o in self.net.outputs:
            cksum = o^cksum

        self.comb += leds.eq(cksum)
        

if __name__ == '__main__':
    import builder as brd
    import sys

    try:
        build = ('b' in sys.argv[1].lower())
        flash = ('f' in sys.argv[1].lower())
    except IndexError:
        print('no argv, assuming default (bf)')
        build = True
        flash = True
        pass

    if build:
        brd.build(_top(brd.plat))         
    if flash:
        brd.flash()


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
        
        self.sync += If(self.cntr == 0,
            self.shifter.shift_clk.eq(1),
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
    from sys import argv, stdout

    nwidth,ndepth = map(int,argv[1:3])
    ndens = float(argv[3])
    fpwidths = tuple(map(int,argv[4:6]))

    try:
        build = ('b' in argv[6].lower())
        flash = ('f' in argv[6].lower())
    except IndexError:
        print('no argv, assuming default (bf)')
        build = True
        flash = True
        pass

    if build:
        top = _top(brd.plat,nwidth,ndepth,ndens,fpwidths)
        stdout.flush()
        brd.build(top)
    if flash:
        brd.flash()


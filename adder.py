#!/usr/bin/python3

#from migen.fhdl.std import *
from migen import *

class tri_adder(Module):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.c = Signal()
        self.lo = Signal()
        self.hi = Signal()

        ###

        self.comb += lo.eq(a^b^c)
        self.comb += hi.eq(a&b | b&c | a&c)

class n_bit_adder_gay(Module):
    def __init__(self, num_bits):
        self.a=Signal(num_bits)
        self.b=Signal(num_bits)
        self.c=Signal()
        self.result=Signal(num_bits+1)
        
        ###

        adders=[tri_adder() for bit in range(num_bits)]
        
        for bitno in range(num_bits):
            if bitno > 0:
                self.comb += adders[bitno].c.eq(adders[bitno-1].hi) #carry
            self.comb += adders[bitno].a.eq(a[bitno])
            self.comb += adders[bitno].b.eq(b[bitno])
            self.comb += result[bitno].eq(adders[bitno].lo)
        self.comb += result[num_bits].eq(adders[num_bits-1].hi)
        
        self.submodules += adders
            
class n_bit_adder_straight(Module):
    def __init__(self, num_bits):
        self.a=Signal(num_bits)
        self.b=Signal(num_bits)
        self.c=Signal()
        self.result=Signal(num_bits+1)
        
        ###

        self.comb += result.eq(a+b+c)


class n_bit_adder_gay_sync(Module):
    def __init__(self, num_bits):
        self.a=Signal(num_bits)
        self.b=Signal(num_bits)
        self.c=Signal()
        self.result=Signal(num_bits+1)

        ###
        self.submodules.nba = n_bit_adder_gay(num_bits)

        self.sync += self.result.eq(self.submodules.nba.result)
        self.sync += self.submodules.nba.a.eq(self.a)
        self.sync += self.submodules.nba.b.eq(self.b)
        self.sync += self.submodules.nba.c.eq(self.c)


class _LedTest(Module):
    def __init__(self,platform):
        bits=10
        
        counter = Signal(bits)

        leds = Cat([plat.request("user_led",n) for n in range(bits)])
        btn = plat.request("key",0)
        
        ###

        self.clock_domains.cd_btn = ClockDomain()
        
        self.sync.btn += counter.eq(counter+1)

        self.comb += self.cd_btn.clk.eq(btn)
        self.comb += leds.eq(counter)


    
if __name__ == '__main__':
    from migen.build.generic_platform import * 

    from migen.build.platforms import de0nano
    import de0cv

    plat = de0cv.Platform()         

    #plat.add_extension([ ("debug", 0, Pins("B16 C16 D16 E16 F16 G16 H16 G15"))]) 

    plat.build(_LedTest(plat))         
    plat.create_programmer().load_bitstream("build/top.sof")

#!/usr/bin/python3
from migen import *

import periph

class _LedTest(Module):
    def __init__(self,platform):
        ckdiv_counter = Signal(32)

        counter = Signal(24)

        digits = [plat.request("7seg",n) for n in range(6)] 

        leds = Cat([plat.request("user_led",n) for n in range(10)])
        btn = plat.request("key",0)

        
        ###
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_slow = ClockDomain()
        
        self.submodules.convs = [periph.display_convert_7seg() for n in range(6)]

        self.sync.sys += ckdiv_counter.eq(ckdiv_counter+1)
        self.sync.slow += counter.eq(counter+1)

        #drive the clocks
        clk50 = plat.request("clk50")
        self.comb += self.cd_sys.clk.eq(clk50)
        self.comb += self.cd_slow.clk.eq(ckdiv_counter[20])

        #7seg converter input
        self.comb += [self.convs[n].value.eq(counter[4*n:4*(n+1)]) for n in range(6)]

        #output to leds
        self.comb += leds.eq(counter[:10])
        self.comb += [digits[n].eq(~self.convs[n].digit) for n in range(6)]

    
if __name__ == '__main__':
    from migen.build.generic_platform import * 

    import de0cv

    plat = de0cv.Platform()         

    plat.build(_LedTest(plat))         
    plat.create_programmer().load_bitstream("build/top.sof")

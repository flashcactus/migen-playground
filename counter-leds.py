#!/usr/bin/python3
from migen import *

import periph

class _LedTest(Module):
    def __init__(self,platform):
        bits=10
        
        counter = Signal(bits)

        digit = plat.request("7seg")

        leds = Cat([plat.request("user_led",n) for n in range(bits)])
        btn = plat.request("key",0)

        
        ###
        self.clock_domains.cd_btn = ClockDomain()
        
        self.submodules.conv = periph.display_convert_7seg()

        self.sync.btn += counter.eq(counter+1)

        #drive the button clock domain
        self.comb += self.cd_btn.clk.eq(btn)

        #7seg converter input
        self.comb += self.conv.value.eq(counter[:4])

        #output to leds
        self.comb += [
            leds.eq(counter),
            digit.eq(self.conv.digit),
        ]



    
if __name__ == '__main__':
    from migen.build.generic_platform import * 

    import de0cv

    plat = de0cv.Platform()         

    #plat.add_extension([ ("debug", 0, Pins("B16 C16 D16 E16 F16 G16 H16 G15"))]) 

    plat.build(_LedTest(plat))         
    plat.create_programmer().load_bitstream("build/top.sof")

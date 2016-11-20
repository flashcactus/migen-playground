#!/usr/bin/python3
from migen import *

class _LedTest(Module):
    def __init__(self,platform):
        led = plat.request("user_led",0)
        btn = plat.request("key",0)
        
        ###

        self.clock_domains.cd_btn = ClockDomain()
        self.comb += self.cd_btn.clk.eq(btn)

        self.sync.btn += led.eq(~led)



    
if __name__ == '__main__':
    from migen.build.generic_platform import * 

    from migen.build.platforms import de0nano
    import de0cv

    plat = de0cv.Platform()         

    #plat.add_extension([ ("debug", 0, Pins("B16 C16 D16 E16 F16 G16 H16 G15"))]) 

    plat.build(_LedTest(plat))         
    plat.create_programmer().load_bitstream("build/top.sof")

#!/usr/bin/python3
from migen import *

class _blink(Module):
    def __init__(self,platform):
        leds = Cat([plat.request("user_led",i) for i in range(4)])
        pins = plat.request("gpio_0",0)[:4]
        
        ###

        self.comb += leds.eq(pins)



    
if __name__ == '__main__':
    from migen.build.generic_platform import * 

    from migen.build.platforms import de0nano
    import de0cv

    plat = de0cv.Platform()         

    plat.build(_blink(plat))         
    plat.create_programmer().load_bitstream("build/top.sof")

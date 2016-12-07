#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import periph

class Strober(Module):
    def __init__(self):
        self.inp = Signal()
        self.strobe = Signal()

        self.submodules.fsm = FSM()

        ###
        
        self.fsm.act("IDLE",
            If(self.inp,
                NextValue(self.strobe,1),
                NextState("WAITRELEASE")
            )
        )

        self.fsm.act("WAITRELEASE",
            [
                NextValue(self.strobe,0),
                If (~self.inp,
                    NextState("IDLE")
                )
            ]
        )


class _LedTest(Module):
    def __init__(self,platform):
        ckdiv_counter = Signal(32)

        counter = Signal(24)

        digits = [plat.request("7seg",n) for n in range(6)] 

        leds = Cat([plat.request("user_led",n) for n in range(10)])
        btn = plat.request("key",0)
        sw = plat.request("sw",0)

        direction = Signal(reset=1)

        ###

        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_slow = ClockDomain()
        
        self.submodules.convs = [periph.display_convert_7seg() for n in range(6)]

        self.submodules.btn_stb = Strober()

        ###

        #btn strobe
        self.comb += self.btn_stb.inp.eq(~btn)
        
        #7seg converter input
        self.comb += [self.convs[n].value.eq(counter[4*n:4*(n+1)]) for n in range(6)]
        
        #output to leds
        self.comb += leds.eq(counter[:10])
        self.comb += [digits[n].eq(~self.convs[n].digit) for n in range(6)]

        #drive the clocks
        clk50 = plat.request("clk50")
        self.comb += self.cd_sys.clk.eq(clk50)
        self.comb += self.cd_slow.clk.eq(ckdiv_counter[20])

        #direction
        self.sync.sys += If(self.btn_stb.strobe, direction.eq(~direction))

        ## sync
        self.sync.sys += ckdiv_counter.eq(ckdiv_counter+1)
        self.sync.slow += If(direction, counter.eq(counter+1)).Else(counter.eq(counter-1))



    
if __name__ == '__main__':
    from migen.build.generic_platform import * 

    import de0cv

    plat = de0cv.Platform()         

    plat.build(_LedTest(plat))         
    plat.create_programmer().load_bitstream("build/top.sof")

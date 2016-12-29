#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import mystuff
import periph
import neuro
from wq_uart import UART


class _top(Module):
    def __init__(self,plat):
        digits = [plat.request("seven_seg",n) for n in range(6)] 
        leds = Cat([plat.request("user_led",n) for n in range(10)])
        btns = [plat.request("key",i) for i in range(4)]
        switches = [plat.request("sw",i) for i in range(10)]

        class serial:
            rx = plat.request("gpio_0",5)
            tx = plat.request("gpio_0",3)

        counter = Signal(32)

        ###

        self.submodules.uart = UART(serial, int(50e6), 9600)

        #7seg converters
        self.submodules.convs = [periph.display_convert_7seg() for n in range(6)]
        self.comb += [digits[i].eq(~self.convs[i].digit) for i in range(6)]

        #pair them into bytes
        convpairs = [Cat(self.convs[2*i].value, self.convs[2*i+1].value) for i in range(3)]
        
        self.submodules.shifter = mystuff.WideShiftReg(8,3)

        ###
        
        #feed the shift register into the digits
        self.comb += [convpairs[i].eq(v) for i,v in enumerate(self.shifter.array)]


        #feed diagnostics into the leds
        self.comb += [
            leds[i].eq(sig) for i, sig in enumerate(
                [
                    self.uart.tx_ready,
                    self.uart.tx_ack,
                    self.uart.rx_ready,
                    self.uart.rx_ack,
                    self.uart.rx_error,
                ] 
            )
        ]


        self.sync += If(self.uart.rx_ready, 
            self.uart.rx_ack.eq(1), 
            self.shifter.serial_in.eq(self.uart.rx_data),
            self.shifter.shift_clk.eq(1)
        ).Else(
            self.uart.rx_ack.eq(0),
            self.shifter.shift_clk.eq(0)
        )

        #transmit the alphabet
        self.sync += [
                counter.eq(counter+1),
                self.uart.tx_data.eq(ord('a')+counter[26:30]),

                If(counter[:26]==0,
                    self.uart.tx_ready.eq(1),
                ).Else(
                    self.uart.tx_ready.eq(0),
                )
            ]



if __name__ == '__main__':
    import builder as brd
    import sys

    ''' 
    try:
        if sys.argv[1][0].lower() == 'b':
            brd.build(_top(brd.plat))         
    except:
        print('no build')
        pass
    '''
    brd.build(_top(brd.plat))         

    brd.flash()
        

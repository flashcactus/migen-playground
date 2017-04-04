#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import mystuff
import periph
import neuro
import neural_net 
from wq_uart import UART

import math


fpga_clk_freq = int(50e6)



class _testnet(Module):
    def __init__(self):
        self.widths = (4,4)
        self.neurons = [
            neural_net.neuron_desc([-1,-2],[3,3],-1.5), #and1(x1,x2)
            neural_net.neuron_desc([-1,-2],[3,3],1.5),  #or1(x1,x2)
            neural_net.neuron_desc([0,1],[-3,3],-1.5),  #and(~and1,or1)
        ]
         
        self.submodules.net = neural_net.StaticNN(2,self.neurons,[2],*self.widths)

'''
class staticxornet(Module):
    def __init__(self):
        (int_width,frac_width) = (4,4)
        self.neurons = [
            neuro.static_neuron(
                wsum    = neuro.weighted_sum(int_width,frac_width,len(n.weights)),    #wsum
                actfun  = neuro.pseudosigmoid_tanh(int_width,frac_width),             #
                weights = map(lambda a:neuro.float2fix(a,frac_width),n.weights),
                bias    = neuro.float2fix(n.bias,frac_width),
                int_width = int_width,
                frac_width = frac_width
            )
        ]
'''         



class _top(Module):
    def __init__(self,plat,bytenum=2):
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

        #group them x3
        convtokens = [Cat(self.convs[2*i+k].value for k in range(2)) for i in range(3)]
        
        
        self.submodules.shifter = mystuff.WideShiftReg(8,bytenum)

        ###
        
        #feed the shift register into the digits
        self.comb += [convtokens[i].eq(v) for i,v in enumerate(self.shifter.array)]



        #receive the uart
        self.submodules.uart_ready_stb = mystuff.Strober()

        self.data_ready = Signal()
        self.recv_byte_cnt = Signal(max=bytenum)
        self.comb += [
            self.uart_ready_stb.inp.eq(self.uart.rx_ready),
            self.shifter.serial_in.eq(self.uart.rx_data),
            If(self.uart_ready_stb.strobe,
                self.uart.rx_ack.eq(1),
                self.shifter.shift_clk.eq(1)
            ).Else(
                self.uart.rx_ack.eq(0),
                self.shifter.shift_clk.eq(0)
            ),
        ]

        self.sync += [
            If(self.uart_ready_stb.strobe,
                self.recv_byte_cnt.eq(self.recv_byte_cnt + 1),
                self.data_ready.eq(0)
            ).Elif(self.recv_byte_cnt == bytenum,
                self.recv_byte_cnt.eq(0),
                self.data_ready.eq(1)
            )
        ]
                
        self.submodules.testnet = _testnet()

        #feed diagnostics into the leds
        self.comb += [
                leds[0].eq(self.data_ready),
                leds[4].eq(self.recv_byte_cnt == 0),
                Cat(leds[1:3]).eq(self.recv_byte_cnt),
                leds[9].eq(self.testnet.outputs[0] >= 0)
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
        

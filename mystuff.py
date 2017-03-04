#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *


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


class WideShiftReg(Module):
    def __init__(self, elem_width, elem_count):
        self.array = [Signal(elem_width) for i in range(elem_count)]
        self.serial_in = Signal(elem_width)

        self.shift_clk = Signal()

        self.submodules.strober = Strober()
        
        ###

        self.comb += [
            self.strober.inp.eq(self.shift_clk)
        ]

        #do the shifting
        self.sync += If(self.strober.strobe,
            [next_e.eq(prev_e) for next_e,prev_e in zip(self.array, [self.serial_in] + self.array[:-1])]        
        )



class uart_token_receiver(Module):
    def __init__(self,token_size,token_count,serial,endianness='b',baud=9600,fpga_clk_freq=5000000):
        self.ready = Signal()
        self.error = Signal()
        self.ack = Signal()
        #self.tokens = [...] ##first in = first index

        ###
        
        self.token_size = token_size
        self.token_count = token_count
        self.bytes_in_token = math.ceil(token_size/8)

        #the receiver
        self.submodules.uart = UART(serial, fpga_clk_freq, baud)
        
        #accumulate the tokens here
        self.submodules.token_shifter = WideShiftReg(token_size,self.token_count)

        #accumulate the bytes in a token here
        self.submodules.byte_shifter = WideShiftReg(8,self.bytes_in_token)

        ###

        #feed the byte shifter
        self.comb += self.byte_shifter.serial_in.eq(self.uart.rx_data)

        #feed the reassembled tokens into the token shifter
        if endianness.lower() == 'b': #big-endian
            self.comb += self.token_shifter.serial_in.eq(Cat(self.byte_shifter.array))
        elif endianness.lower() == 'l': #little-endian
            self.comb += self.token_shifter.serial_in.eq(Cat(self.byte_shifter.array[::-1]))
        else: 
            raise ValueError("endianness must be either 'b' or 'l'")

        self.tokens = self.token_shifter.array[::-1] #first in = first index

        ###

        self.recv_byte_count = Signal(max=self.bytes_in_token)
        self.recv_token_count = Signal(max=self.token_count)

        self.submodules.byte_fsm = FSM()

        self.byte_fsm.act("WAIT_BYTES",
            If(self.uart.rx_ready,
                self.uart.rx_ack.eq(1), 
                self.byte_shifter.shift_clk.eq(1),
                NextValue(self.recv_byte_count, self.recv_byte_count+1)
            ).Else(
                self.uart.rx_ack.eq(0),
                self.byte_shifter.shift_clk.eq(0)
            ),
            If(self.recv_byte_count == self.bytes_in_token,
                NextState("INSERT_TOKEN"),
                NextValue(self.token_shifter.shift_clk,1),
            )
        )

        self.byte_fsm.act("INSERT_TOKEN",
            NextState("WAIT_BYTES"),
            NextValue(self.recv_byte_count,0),
            NextValue(self.token_shifter.shift_clk,0),
            If(self.recv_token_count == self.token_count,
                NextValue(self.error,1),
                NextValue(self.recv_token_count,0)
            ).Else(
                NextValue(self.recv_token_count,self.recv_token_count+1)
            )
        )

        
        self.comb += If(self.recv_token_count == self.token_count,
            self.ready.eq(1)
        ).Else(
            self.ready.eq(0)
        )

        self.sync += If(self.ready & self.ack,
            self.recv_token_count.eq(0)
        )

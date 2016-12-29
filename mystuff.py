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

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



# This file is Copyright (c) 2013 Florent Kermarrec <florent@enjoy-digital.fr>
# License: BSD

from migen.build.generic_platform import *
from migen.build.altera import AlteraPlatform
from migen.build.altera.programmer import USBBlaster


_io = [
    ("clk50", 0, Pins("M9"), IOStandard("3.3-V LVTTL")),
    ("clk50", 1, Pins("H13"), IOStandard("3.3-V LVTTL")),
    ("clk50", 2, Pins("E10"), IOStandard("3.3-V LVTTL")),
    ("clk50", 3, Pins("V15"), IOStandard("3.3-V LVTTL")),

    ("user_led", 0, Pins("AA2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 1, Pins("AA1"), IOStandard("3.3-V LVTTL")),
    ("user_led", 2, Pins("W2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 3, Pins("Y3"), IOStandard("3.3-V LVTTL")),
    ("user_led", 4, Pins("N2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 5, Pins("N1"), IOStandard("3.3-V LVTTL")),
    ("user_led", 6, Pins("U2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 7, Pins("U1"), IOStandard("3.3-V LVTTL")),
    ("user_led", 8, Pins("L2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 9, Pins("L1"), IOStandard("3.3-V LVTTL")),


    ("7seg", 0, Pins("U21 V21 W22 W21 Y22 Y21 AA22"), IOStandard("3.3-V LVTTL")),
    ("7seg", 1, Pins("AA20 AB20 AA19 AA18 AB18 AA17 U22"), IOStandard("3.3-V LVTTL")),
    ("7seg", 2, Pins("Y19 AB17 AA10 Y14 V14 AB22 AB21"), IOStandard("3.3-V LVTTL")),
    ("7seg", 3, Pins("Y16 W16 Y17 V16 U17 V18 V19"), IOStandard("3.3-V LVTTL")),
    ("7seg", 4, Pins("U20 Y20 V20 U16 U15 Y15 P9"), IOStandard("3.3-V LVTTL")),
    ("7seg", 5, Pins("N9 M8 T14 P14 C1 C2 W19"), IOStandard("3.3-V LVTTL")),


    ("key", 0, Pins("U7"), IOStandard("3.3-V LVTTL")),
    ("key", 1, Pins("W9"), IOStandard("3.3-V LVTTL")),
    ("key", 2, Pins("M7"), IOStandard("3.3-V LVTTL")),
    ("key", 3, Pins("M6"), IOStandard("3.3-V LVTTL")),

    ("sw", 0, Pins("U13"), IOStandard("3.3-V LVTTL")),
    ("sw", 1, Pins("V13"), IOStandard("3.3-V LVTTL")),
    ("sw", 2, Pins("T13"), IOStandard("3.3-V LVTTL")),
    ("sw", 3, Pins("T12"), IOStandard("3.3-V LVTTL")),
    ("sw", 4, Pins("AA15"), IOStandard("3.3-V LVTTL")),
    ("sw", 5, Pins("AB15"), IOStandard("3.3-V LVTTL")),
    ("sw", 6, Pins("AA14"), IOStandard("3.3-V LVTTL")),
    ("sw", 7, Pins("AA13"), IOStandard("3.3-V LVTTL")),
    ("sw", 8, Pins("AB13"), IOStandard("3.3-V LVTTL")),
    ("sw", 9, Pins("AB12"), IOStandard("3.3-V LVTTL")),

#    ("serial", 0,
#        Subsignal("tx", Pins("D3"), IOStandard("3.3-V LVTTL")),
#        Subsignal("rx", Pins("C3"), IOStandard("3.3-V LVTTL"))
#    ),

#    ("sdram_clock", 0, Pins("R4"), IOStandard("3.3-V LVTTL")),
#    ("sdram", 0,
#        Subsignal("a", Pins("P2 N5 N6 M8 P8 T7 N8 T6 R1 P1 N2 N1 L4")),
#        Subsignal("ba", Pins("M7 M6")),
#        Subsignal("cs_n", Pins("P6")),
#        Subsignal("cke", Pins("L7")),
#        Subsignal("ras_n", Pins("L2")),
#        Subsignal("cas_n", Pins("L1")),
#        Subsignal("we_n", Pins("C2")),
#        Subsignal("dq", Pins("G2 G1 L8 K5 K2 J2 J1 R7 T4 T2 T3 R3 R5 P3 N3 K1")),
#        Subsignal("dm", Pins("R6 T5")),
#        IOStandard("3.3-V LVTTL")
#    ),
#
#    ("epcs", 0,
#        Subsignal("data0", Pins("H2")),
#        Subsignal("dclk", Pins("H1")),
#        Subsignal("ncs0", Pins("D2")),
#        Subsignal("asd0", Pins("C1")),
#        IOStandard("3.3-V LVTTL")
#    ),
#
#    ("i2c", 0,
#        Subsignal("sclk", Pins("F2")),
#        Subsignal("sdat", Pins("F1")),
#        IOStandard("3.3-V LVTTL")
#    ),
#
#    ("g_sensor", 0,
#        Subsignal("cs_n", Pins("G5")),
#        Subsignal("int", Pins("M2")),
#        IOStandard("3.3-V LVTTL")
#    ),
#
#    ("adc", 0,
#        Subsignal("cs_n", Pins("A10")),
#        Subsignal("saddr", Pins("B10")),
#        Subsignal("sclk", Pins("B14")),
#        Subsignal("sdat", Pins("A9")),
#        IOStandard("3.3-V LVTTL")
#    ),

    ("gpio_0", 0,
        Pins("N16 B16 M16 C16 D17 K20 K21 K22 M20 M21 N21 R22 R21 T22 N20 N19 M22 P19 L22 P17 P16 M18 L18 L17 L19 K17 K19 P18 R15 R17 R16 T20 T19 T18 T17 T15"),
        IOStandard("3.3-V LVTTL")
    ),
    ("gpio_1", 0,
        Pins("H16 A12 H15 B12 A13 B13 C13 D13 G18 G17 H18 J18 J19 G11 H10 J11 H14 A15 J13 L8 A14 B15 C15 E14 E15 E16 F14 F15 F13 F12 G16 G15 G13 G12 J17 K16"),
        IOStandard("3.3-V LVTTL")
    ),
]


class Platform(AlteraPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20

    def __init__(self):
        AlteraPlatform.__init__(self, "5CEBA4F23C7", _io)

    def create_programmer(self):
        return USBBlaster()


from migen import *

class display_convert_7seg(Module):
    def __init__(self,invert=False):
        self.value=Signal(4)
        self.digit=Signal(7)
        
        ###
        
        mapping = {
            #     abcdefg
            #     0123456 
            0x0: 0b0111111 ,
            0x1: 0b0000110 ,
            0x2: 0b1011011 ,
            0x3: 0b1001111 ,
            0x4: 0b1100110 ,
            0x5: 0b1101101 ,
            0x6: 0b1111101 ,
            0x7: 0b0000111 ,
            0x8: 0b1111111 ,
            0x9: 0b1101111 ,
            0xa: 0b1110111 ,
            0xb: 0b1111100 ,
            0xc: 0b0111001 ,
            0xd: 0b1011110 ,
            0xe: 0b1111001 ,
            0xf: 0b1110001 ,
        }


        self.comb += Case(self.value, {k:self.digit.eq(mapping[k]) for k in mapping}) 



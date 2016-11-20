
from migen import *

class display_convert_7seg(Module):
    def __init__(self,invert=False):
        self.value=Signal(4)
        self.digit=Signal(7)
        
        ###
        
        mapping = {
            #     abcdefg
            #     0123456 
            0 : 0b0111111 ,
            1 : 0b0000110 ,
            2 : 0b1011011 ,
            3 : 0b1100111 ,
            4 : 0b1100110 ,
            5 : 0b1101101 ,
            6 : 0b1111101 ,
            7 : 0b0000111 ,
            8 : 0b1111111 ,
            9 : 0b1101111 ,
            10: 0b1110111 ,
            11: 0b1111100 ,
            12: 0b0111100 ,
            13: 0b1011110 ,
            14: 0b1111011 ,
            15: 0b1110001 ,
        }

        '''
        mapping = {
            0x0: 0b1111110,
            0x1: 0b0110000,
            0x2: 0b1101101,
            0x3: 0b1110011,
            0x4: 0b0110011,
            0x5: 0b1011011,
            0x6: 0b1011111,
            0x7: 0b1110000,
            0x8: 0b1111111,
            0x9: 0b1111011,
            0xa: 0b1110111,
            0xb: 0b0011111,
            0xc: 0b0011110,
            0xd: 0b0111101,
            0xe: 0b1101111,
            0xf: 0b1000111
        }
        '''

        self.comb += Case(self.value, {k:self.digit.eq(mapping[k]) for k in mapping}) 



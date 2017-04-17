#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import neuro

import random
import math
#random.seed(1)

num_samples = 20

test_widths = [4,4]

to_fix = lambda n: int(n*2**test_widths[1])
to_float = lambda n: n*2**-test_widths[1]
fixify = lambda n: to_float(to_fix(n))

import neural_hwtest

net_ut = neural_hwtest._testnet()
net_ut.finalize()

def test_tn():
    for i in range(num_samples):
        sample=[random.uniform(-2,2) for i in range(2)]
        yield net_ut.net.inputs[0].eq(to_fix(sample[0]))
        yield net_ut.net.inputs[1].eq(to_fix(sample[1]))
        yield
        result = (yield net_ut.net.outputs[0])
        print(sample, '->', to_float(result))
        for nnum, n in enumerate(net_ut.net.neurons):
            for inum, i in enumerate(net_ut.net.neurons[nnum].inputs):
                print(nnum, inum, to_float((yield net_ut.net.neurons[nnum].inputs[inum])))

run_simulation(net_ut, test_tn(), vcd_name="xornet.vcd")

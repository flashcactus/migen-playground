#!/usr/bin/python3
from migen import *
from migen.genlib.fsm import *

import neuro

import random
import math
#random.seed(1)

num_samples = 20

test_widths = [8,16]
wsum_input_n = 4

to_fix = lambda n: int(n*2**test_widths[1])
to_float = lambda n: n*2**-test_widths[1]
fixify = lambda n: to_float(to_fix(n))


##################################
# FP MUL


fpm_ut = neuro.fp_multiplier(*test_widths)
def test_fp_mul():
    for i in range(num_samples):
        inps = [random.normalvariate(0,30) for i in range(2)]
        fxinp = list(map(to_fix,inps))
        yield fpm_ut.a.eq(fxinp[0])
        yield fpm_ut.b.eq(fxinp[1])
        yield
        result = (yield fpm_ut.result)
        true_product = inps[0]*inps[1]
        fixified_product = fixify(inps[0])*fixify(inps[1])
        print ('mul', inps, '=', to_float(result))
        print ('\terr v flt', (to_float(result) - true_product) / to_float(1), 'LSB')
        print ('\terr v fix', (to_float(result) - fixified_product) / to_float(1), 'LSB')
        assert abs(to_float(result) - fixified_product) < to_float(1)
##############################
# pseudotanh

pseudotanh = lambda n: 0.75*n if abs(0.75*n)<1 else 1 if n>0 else -1

psth_dut = neuro.pseudosigmoid_tanh(*test_widths)

def test_psth():
    for inp in (random.normalvariate(0,3) for i in range(num_samples)):
        yield psth_dut.input.eq(to_fix(inp))
        yield
        fix_result = (yield psth_dut.output)
        result = to_float(fix_result)
        flt_err = result - pseudotanh(inp)
        fix_err = result - pseudotanh(fixify(inp))
        print('psth {} = {}'.format(inp,result))
        print('\tflt_err {:.5e} ({:.2f} LSB)'.format(flt_err, flt_err/to_float(1)))
        print('\tfix_err {:.5e} ({:.2f} LSB)'.format(fix_err, fix_err/to_float(1)))
        try:
            assert abs(fix_err) < to_float(1)
        except:
            print('TEST FAILED')



###################################
# WEIGHTED SUM

#benchmark weighted sum
weighted_sum = lambda inputs, weights, bias: bias + sum(i*w for i,w in zip(inputs, weights))

#the victim
wsum_ut = neuro.weighted_sum(*test_widths)

#add inputs & test values
bias = random.normalvariate(0,0.2)
fix_bias = to_fix(bias)
print('bias',bias,fix_bias)

#generate some random weights
weights=[]
for i in range(wsum_input_n):
    inp = wsum_ut.add_input()
    weights.append(random.normalvariate(0,2/wsum_input_n))

fix_weights = list(map(to_fix,weights))


def wsum_check_case(inp_set):
    fix_inps = list(map(to_fix,inp_set))
    for sinp,inp,swei,wei in zip(wsum_ut.inputs,fix_inps,wsum_ut.weights,fix_weights):
        yield sinp.eq(inp)
        yield swei.eq(wei)
    yield wsum_ut.bias.eq(fix_bias)
    yield

    fix_result = (yield wsum_ut.output)
    result = to_float(fix_result)
    true_value = weighted_sum(inp_set,weights,bias)
    fixified_true_value = weighted_sum(map(fixify,inp_set),map(fixify,weights),fixify(bias))
    
    flt_err = result - true_value
    fix_err = result - fixified_true_value

    print('in',inp_set,weights)
    print('\tout', fix_result, '=', result)
    print('\tflt_err {:.5e} ({:.2f} LSB)'.format(flt_err, flt_err/to_float(1)))
    print('\tfix_err {:.5e} ({:.2f} LSB)'.format(fix_err, fix_err/to_float(1)))
    assert abs(fix_err) < to_float(len(inp_set))

def test_wsum():
    for i in range(num_samples):
        yield from wsum_check_case([random.normalvariate(0,30) for j in range(wsum_input_n)])


###################################
# Static neuron

#benchmark neuron
wsum_ptanh_neuron = lambda inputs, weights, bias: pseudotanh(weighted_sum(inputs, weights, bias))
    

#the victim
#we'll use the weights & bias from the wsum test
neuron_dut = neuro.static_neuron(
        neuro.weighted_sum(*test_widths,wsum_input_n),
        neuro.pseudosigmoid_tanh(*test_widths),
        fix_weights,
        fix_bias,
        *test_widths
    )


def neuron_check_case(inp_set):
    fix_inps = list(map(to_fix,inp_set))
    for sinp,inp in zip(neuron_dut.inputs,fix_inps):
        yield sinp.eq(inp)
    yield

    fix_result = (yield neuron_dut.output)
    result = to_float(fix_result)

    fix_sum = (yield neuron_dut.wsum.output)
    flt_sum = to_float(fix_sum)

    true_value = wsum_ptanh_neuron(inp_set,weights,bias)
    fixified_true_value = wsum_ptanh_neuron(map(fixify,inp_set),map(fixify,weights),fixify(bias))
    
    flt_err = result - true_value
    fix_err = result - fixified_true_value

    print('in',inp_set,weights)
    print('\tsum {} = {}\n\tout {} = {}'.format(fix_sum, flt_sum, fix_result, result))
    print('\tflt_err {:.5e} ({:.2f} LSB)'.format(flt_err, flt_err/to_float(1)))
    print('\tfix_err {:.5e} ({:.2f} LSB)'.format(fix_err, fix_err/to_float(1)))
    try:
        assert abs(fix_err) < to_float(len(inp_set))
    except:
        print("\nFAIL\n")

def test_neuron():
    for i in range(num_samples):
        yield from neuron_check_case([random.normalvariate(0,30) for j in range(wsum_input_n)])


########################################
########################################

print("#"*20,"\nsimulating fp_mul...\n\n")
run_simulation(fpm_ut, test_fp_mul())

print("#"*20,"\nsimulating pseudotanh...\n\n")
run_simulation(psth_dut, test_psth())

print("#"*20,"\nsimulating weighted sum...\n\n")
run_simulation(wsum_ut, test_wsum(), vcd_name="wsum.vcd")

print("#"*20,"\nsimulating static neuron...\n\n")
run_simulation(neuron_dut, test_neuron(), vcd_name="neuron.vcd")

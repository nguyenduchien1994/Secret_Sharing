from __future__ import division
import sys
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/reedsolomon")

import ffield
import reedsolo
import random

test_cases = 10000

def truncate(code,f):
    to_return = []
    for i in range(0,len(code),f):
        to_return.append(code[i:i+f])
    return to_return

def robustEncoder(S,f):

    F = ffield.FField(f)
    trun_S = truncate(S,f)

    bin_S0 = trun_S[0]
    bin_S1 = trun_S[1]
    bin_S2 = trun_S[2]

    int_S0 = int(bin_S0,2)
    int_S1 = int(bin_S1,2)
    int_S2 = int(bin_S2,2)

    int_E3 = F.Add(F.Multiply(int_S0,int_S1),F.Multiply(F.Multiply(int_S2,int_S2),int_S2))

    bin_E3 = '{0:08b}'.format(int_E3)

    return bin_S0 + bin_S1 + bin_S2 + bin_E3

def robustDecoder(E,f):

    F = ffield.FField(f)
    trun_E = truncate(E,f)

    bin_S0 = trun_E[0]
    bin_S1 = trun_E[1]
    bin_S2 = trun_E[2]
    bin_E3 = trun_E[3]

    int_S0 = int(bin_S0,2)
    int_S1 = int(bin_S1,2)
    int_S2 = int(bin_S2,2)
    int_E3 = int(bin_E3,2)

    eval_E3 = F.Add(F.Multiply(int_S0,int_S1),F.Multiply(F.Multiply(int_S2,int_S2),int_S2))

    if eval_E3 == int_E3:
        return True
    else:
        return False

def shareDistribute():
    return 0

def secretRecon():
    return 0

def tester(f):

    F = ffield.FField(f)
    error = int("11111111000000001111111100000000",2)
    miss = 0

    for i in range(0,test_cases):
        int_S = random.randint(0,2**24-1)
        bin_S = '{0:024b}'.format(int_S)
        E = robustEncoder(bin_S,f)
        int_E = int(E,2)
        tilda_E = F.Add(int_E,error)
        bin_tilda_E = '{0:032b}'.format(tilda_E)

        if (robustDecoder(bin_tilda_E,f)):
            miss += 1

    print "Miss Rate = " + str(miss*100/test_cases) + "%"

tester(8)


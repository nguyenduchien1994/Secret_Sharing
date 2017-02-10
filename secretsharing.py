from __future__ import division
import sys

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
#sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")
#sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/reedsolomon")

import ffield
#import reedsolo
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

def shareDistribute(E,f,n):

    F = ffield.FField(f)
    a0 = int("10101010101010101010101010101010",2)
    a1 = int("01010101010101010101010101010101",2)
    shares = {}

    for x in range(1,n+1):
        D = F.Add(F.Add(F.Multiply(F.Multiply(x,x),int(E,2)),F.Multiply(a1,x)),a0)
        D = '{0:032b}'.format(D)
        shares['{0:032b}'.format(x)] = D

    return shares

def secretRecon(holders,f):

    F = ffield.FField(f)

    if len(holders) == 2:
        denom = F.Add(int(holders.keys()[0],2),int(holders.keys()[1],2))
        nom = F.Add(int(holders.values()[0],2),int(holders.values()[1],2))
        E = F.Multiply(nom,F.Inverse(denom))

        return '{0:032b}'.format(E)

    elif len(holders) == 3:
        E = 0
        for x in holders.keys():
            D = holders[x]
            nom = int(D,2)
            denom = 1
            for y in holders.keys():
                if y != x:
                    denom = F.Multiply(denom,F.Add(int(x,2),int(y,2)))
            E = F.Add(E,F.Multiply(nom,F.Inverse(denom)))

        return '{0:032b}'.format(E)

    else:

        return 0

def test_M1_M2(f):

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

def test_full():

    int_S = random.randint(0,2**24-1)
    bin_S = '{0:024b}'.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    E = robustEncoder(bin_S,8)

    print "###### The encrypted-secret is " + E + " ######"

    shares = shareDistribute(E,32,10)
    chosen = dict((key,value) for key, value in shares.iteritems() if key in ('{0:032b}'.format(1),'{0:032b}'.format(2),'{0:032b}'.format(3))) # Python 2.6
    #chosen = {x: shares[x] for x in ('{0:032b}'.format(4),'{0:032b}'.format(2),'{0:032b}'.format(3))} # Python 2.7
    E_con = secretRecon(chosen,32)

    print "###### Reconstructed secret is " + E_con + " ######"

    if robustDecoder(E_con,8):
        print "###### Correct! ######"
    else:
        print "###### Incorrect! ######"

#test_M1_M2(8)
test_full()


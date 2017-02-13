from __future__ import division
import sys

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/reedsolomon")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/reedsolomon")

import ffield
import reedsolo
import random
from Robust import Robust
from AMD import AMD
from AMD_extended import AMD_extended
from ShareDistribute import ShareDistribute
from SecretRecon import SecretRecon
from GroupTesting import GroupTesting

def test_M1_M2(f):

    F = ffield.FField(f)
    error = int("11111111000000001111111100000000",2)
    test_cases = 10000
    miss = 0

    for i in range(0,test_cases):
        int_S = random.randint(0,2**24-1)
        bin_S = '{0:024b}'.format(int_S)
        r = Robust(f)
        E = r.encode(bin_S)
        int_E = int(E,2)
        tilda_E = F.Add(int_E,error)
        bin_tilda_E = '{0:032b}'.format(tilda_E)

        if (r.decode(bin_tilda_E)):
            miss += 1

    print "Miss Rate = " + str(miss*100/test_cases) + "%"

def test_extended_AMD(f):

    print "###### Test Extended AMD ######"

    F = ffield.FField(f)
    #error = int("11111111000000001111111100000000",2)
    error = random.randint(0,2**40-1)
    test_cases = 100000
    miss = 0

    for i in range(0,test_cases):
        int_S = random.randint(0,2**24-1)
        bin_S = '{0:024b}'.format(int_S)
        a = AMD_extended(f)
        E = a.encode(bin_S)
        int_E = int(E,2)
        tilda_E = F.Add(int_E,error)
        bin_tilda_E = '{0:040b}'.format(tilda_E)

        if (a.decode(bin_tilda_E)):
            miss += 1

    print "Miss Rate = " + str(miss*100/test_cases) + "%"

def test_robust():

    print "****** Robust Encryption ******"

    int_S = random.randint(0,2**24-1)
    bin_S = '{0:024b}'.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    r = Robust(8)
    E = r.encode(bin_S)

    print "###### The encrypted secret is " + E + " ######"

    sd = ShareDistribute(32)
    shares = sd.distribute(E,7)
    chosen = dict((key,value) for key, value in shares.iteritems() if key in ('{0:032b}'.format(1),'{0:032b}'.format(2),'{0:032b}'.format(3))) # Python 2.6
    #chosen = {x: shares[x] for x in ('{0:032b}'.format(4),'{0:032b}'.format(2),'{0:032b}'.format(3))} # Python 2.7
    sr = SecretRecon(32)
    E_con = sr.recon_3(chosen)

    print "###### Reconstructed secret is " + E_con + " ######"

    if r.decode(E_con):
        print "###### Correct! ######"
    else:
        print "###### Incorrect! ######"

def test_amd():

    print "****** AMD Encryption ******"

    int_S = random.randint(0,2**24-1)
    bin_S = '{0:024b}'.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    a = AMD(8)
    E = a.encode(bin_S)

    print "###### The encrypted secret is " + E + " ######"

    sd = ShareDistribute(32)
    shares = sd.distribute(E,10)

    chosen = dict((key,value) for key, value in shares.iteritems() if key in ('{0:032b}'.format(1),'{0:032b}'.format(2),'{0:032b}'.format(3))) # Python 2.6
    #chosen = {x: shares[x] for x in ('{0:032b}'.format(4),'{0:032b}'.format(2),'{0:032b}'.format(3))} # Python 2.7
    sr = SecretRecon(32)
    E_con = sr.recon_3(chosen)

    print "###### Reconstructed secret is " + E_con + " ######"

    if a.decode(E_con):
        print "###### Correct! ######"
    else:
        print "###### Incorrect! ######"

def test_group_testing():

    n = 7
    k = 3
    t = n-k

    print "****** Group Testing Test ******"
    int_S = random.randint(0,2**24-1)
    bin_S = '{0:024b}'.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    #r = Robust(8)
    #E = r.encode(bin_S)

    a = AMD(8)
    E = a.encode(bin_S)

    print "###### The encrypted secret is " + E + " ######"

    sd = ShareDistribute(32)
    shares = sd.distribute(E,n)

    cheaters = []

    for count in range(0,t):
        cheater = random.randint(1,n)
        while cheater in cheaters:
            cheater = random.randint(1,n)
        cheaters.append(cheater)
        cheater = '{0:032b}'.format(cheater)
        int_cheat_code = random.randint(0,2**32-1)
        bin_cheat_code = '{0:032b}'.format(int_cheat_code)
        shares[cheater] = bin_cheat_code

    print "###### The cheaters are " + str(cheaters) + " ######"

    #chosen = dict((key,value) for key, value in shares.iteritems() if key in ('{0:032b}'.format(1),'{0:032b}'.format(2),'{0:032b}'.format(3))) # Python 2.6
    chosen = {x: shares[x] for x in ('{0:032b}'.format(4),'{0:032b}'.format(2),'{0:032b}'.format(3))} # Python 2.7
    sr = SecretRecon(32)
    E_con = sr.recon_3(chosen)

    print "###### Reconstructed secret is " + E_con + " ######"

    #if r.decode(E_con):
    if a.decode(E_con):
        print "###### Correct! ######"
    else:
        print "###### Incorrect! ######"

    g = GroupTesting(n,k)
    matrix = g.genMatrix()

    syndrome = []

    for combination in matrix:
        chosen_idx = []
        chosen = {}
        for idx,holder in enumerate(combination):
            if holder == 1:
                chosen_idx.append(idx)
        for idx in chosen_idx:
            chosen['{0:032b}'.format(idx+1)] = shares['{0:032b}'.format(idx+1)]

        E_con = sr.recon_3(chosen)

        #if r.decode(E_con):
        if a.decode(E_con):
            syndrome.append(0)
        else:
            syndrome.append(1)

    print "###### Syndrome: " + str(syndrome) + " ######"

    t_matrix = g.transpose(matrix)
    indicator = [0]*len(t_matrix)

    for i in range(0,len(t_matrix)):
        for j in range(0,len(t_matrix[i])):
            if t_matrix[i][j] & syndrome[j] == 1:
                indicator[i] += 1

    non_cheaters = []
    max_fails = g.nCr(n-1,k-1)

    for k in range(0,len(indicator)):
        if indicator[k] < max_fails:
            non_cheaters.append(k+1)

    print "@@@@@@ The non-cheaters are " + str(non_cheaters) + " @@@@@@"

#test_M1_M2(8)
#test_robust()
#test_amd()
test_extended_AMD(8)
#test_group_testing()

from __future__ import division
import sys

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/reedsolomon")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/reedsolomon")

import ffield
import reedsolo
import random
import time
from Robust import Robust
from AMD import AMD
from AMD_extended import AMD_extended
from ShareDistribute import ShareDistribute
from SecretRecon import SecretRecon
from GroupTesting import GroupTesting

freq_CPU = 2327.40 * 10**6

def test_reedsolo():
    return 0

def test_M1_M2(f):

    F = ffield.FField(f)
    error = int("11111111000000001111111100000000",2)
    test_cases = 10000
    miss = 0

    format_S = '{0:0'+str(3*f)+'b}'
    format_E = '{0:0'+str(4*f)+'b}'

    for i in range(0,test_cases):
        int_S = random.randint(0,2**24-1)
        bin_S = format_S.format(int_S)
        r = Robust(f)
        E = r.encode(bin_S)
        int_E = int(E,2)
        tilda_E = F.Add(int_E,error)
        bin_tilda_E = format_E.format(tilda_E)

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

    format_S = '{0:0'+str(3*f)+'b}'
    format_E = '{0:0'+str(5*f)+'b}'

    for i in range(0,test_cases):
        int_S = random.randint(0,2**24-1)
        bin_S = format_S.format(int_S)
        a = AMD_extended(f)
        E = a.encode(bin_S)
        int_E = int(E,2)
        tilda_E = F.Add(int_E,error)
        bin_tilda_E = format_E.format(tilda_E)

        if (a.decode(bin_tilda_E)):
            miss += 1

    print "Miss Rate = " + str(miss*100/test_cases) + "%"

def test_robust(f):

    print "****** Robust Encryption ******"

    format_S = '{0:0'+str(3*f)+'b}'
    format_E = '{0:0'+str(4*f)+'b}'

    int_S = random.randint(0,2**24-1)
    bin_S = format_S.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    r = Robust(f)
    E = r.encode(bin_S)

    print "###### The encrypted secret is " + E + " ######"

    sd = ShareDistribute(4*f)
    shares = sd.distribute(E,7)
    #chosen = dict((key,value) for key, value in shares.iteritems() if key in (format_E.format(1),format_E.format(2),format_E.format(3))) # Python 2.6
    chosen = {x: shares[x] for x in (format_E.format(4),format_E.format(2),format_E.format(3))} # Python 2.7
    sr = SecretRecon(4*f)
    E_con = sr.recon_3(chosen)

    print "###### Reconstructed secret is " + E_con + " ######"

    if r.decode(E_con):
        print "###### Correct! ######"
    else:
        print "###### Incorrect! ######"

def test_amd(f):

    print "****** Test AMD Encryption ******"

    format_S = '{0:0'+str(3*f)+'b}'
    format_E = '{0:0'+str(4*f)+'b}'

    F = ffield.FField(f)
    error = random.randint(1,2**(f*4)-1)
    #test_cases = 40000
    test_cases = 4*(2**f)
    miss = 0

    for i in range(0,test_cases):

        int_S = random.randint(0,2**(3*f)-1)
        bin_S = format_S.format(int_S)

        a = AMD(f)
        bin_E = a.encode(bin_S)
        int_E = int(bin_E,2)
        tilda_E = F.Add(int_E,error)
        #tilda_E = int_E
        bin_tilda_E = format_E.format(tilda_E)

        #sd = ShareDistribute(4*f)
        #shares = sd.distribute(bin_tilda_E,10)
        #cheat = F.Add(int(shares[format_E.format(4)],2),error)
        #shares[format_E.format(4)] = format_E.format(cheat)
        #chosen = dict((key,value) for key, value in shares.iteritems() if key in (format_E.format(1),format_E.format(2),format_E.format(3))) # Python 2.6
        #chosen = {x: shares[x] for x in (format_E.format(4),format_E.format(2),format_E.format(3))} # Python 2.7
        #sr = SecretRecon(4*f)
        #E_con = sr.recon_3(chosen)

        #if (a.decode(E_con)):
        if (a.decode(bin_tilda_E)):
            miss += 1

    print "For field value = " + str(f)
    print "Miss Rate = " + str(miss*100/test_cases) + "%"

def test_group_testing(f):

    n = 7
    k = 3
    t = n-k

    format_S = '{0:0'+str(3*f)+'b}'
    format_E = '{0:0'+str(4*f)+'b}'

    print "****** Group Testing Test ******"
    int_S = random.randint(0,2**24-1)
    bin_S = format_S.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    #r = Robust(f)
    #E = r.encode(bin_S)

    a = AMD(f)
    E = a.encode(bin_S)

    print "###### The encrypted secret is " + E + " ######"

    sd = ShareDistribute(4*f)
    shares = sd.distribute(E,n)

    cheaters = []

    for count in range(0,t):
        cheater = random.randint(1,n)
        while cheater in cheaters:
            cheater = random.randint(1,n)
        cheaters.append(cheater)
        cheater = format_E.format(cheater)
        int_cheat_code = random.randint(0,2**(f*4)-1)
        bin_cheat_code = format_E.format(int_cheat_code)
        shares[cheater] = bin_cheat_code

    print "###### The cheaters are " + str(cheaters) + " ######"

    #chosen = dict((key,value) for key, value in shares.iteritems() if key in (format_E.format(1),format_E.format(2),format_E.format(3))) # Python 2.6
    chosen = {x: shares[x] for x in (format_E.format(4),format_E.format(2),format_E.format(3))} # Python 2.7
    sr = SecretRecon(f*4)
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

    start = time.clock()

    for combination in matrix:
        chosen_idx = []
        chosen = {}
        for idx,holder in enumerate(combination):
            if holder == 1:
                chosen_idx.append(idx)
        for idx in chosen_idx:
            chosen[format_E.format(idx+1)] = shares[format_E.format(idx+1)]

        E_con = sr.recon_3(chosen)

        #if r.decode(E_con):
        if a.decode(E_con):
            syndrome.append(0)
        else:
            syndrome.append(1)

    end = time.clock()
    print "@@@@@@ Group Testing takes " + str(end-start) + " seconds or " + str((end-start)*freq_CPU) + " cycles @@@@@@"
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

    return non_cheaters

#test_M1_M2(8)
#test_robust()
test_amd(8)
test_amd(10)
test_amd(12)
test_amd(16)
#test_amd(32)
#test_extended_AMD(8)
#test_group_testing(8)
#test_reedsolo()

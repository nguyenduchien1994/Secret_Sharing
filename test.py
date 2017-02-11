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
from ShareDistribute import ShareDistribute
from SecretRecon import SecretRecon

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

def test_robust():

    print "****** Robust Encryption ******"

    int_S = random.randint(0,2**24-1)
    bin_S = '{0:024b}'.format(int_S)

    print "###### The secret is " + bin_S + " ######"

    r = Robust(8)
    E = r.encode(bin_S)

    print "###### The encrypted secret is " + E + " ######"

    sd = ShareDistribute(32)
    shares = sd.distribute(E,10)
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

test_M1_M2(8)
test_robust()
test_amd()
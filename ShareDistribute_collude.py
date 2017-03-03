import sys
import random

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")

import ffield

class ShareDistribute_collude():

    def __init__(self,f):
        self.f = f
        self.F = ffield.FField(self.f)
        self.a0 = "1011101110111100"
        self.a1 = "0111011101110111"
        self.E = "1010101111001101"
        self.a0 = int(self.a0,2)
        self.a1 = int(self.a1,2)

    def distribute(self,cheaters):

        shares = {}

        for x in cheaters:
            D = self.F.Add(self.F.Add(self.F.Multiply(self.F.Multiply(x,x),int(self.E,2)),self.F.Multiply(self.a1,x)),self.a0)
            D = ('{0:0'+str(self.f)+'b}').format(D)
            shares[('{0:0'+str(self.f)+'b}').format(x)] = D
        return shares

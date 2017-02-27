import sys
import random

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")

import ffield

class ShareDistribute():

    def __init__(self,f):
        self.f = f
        self.F = ffield.FField(self.f)
        self.a0 = "10"*(f/2)
        self.a1 = "01"*(f/2)
        self.a0 = int(self.a0,2)
        self.a1 = int(self.a1,2)
        #self.a0 = random.randint(0,2**(4*f)-1)
        #self.a1 = random.randint(0,2**(4*f)-1)

    def distribute(self,E,n):

        shares = {}

        for x in range(1,n+1):
            D = self.F.Add(self.F.Add(self.F.Multiply(self.F.Multiply(x,x),int(E,2)),self.F.Multiply(self.a1,x)),self.a0)
            D = ('{0:0'+str(self.f)+'b}').format(D)
            shares[('{0:0'+str(self.f)+'b}').format(x)] = D
        return shares

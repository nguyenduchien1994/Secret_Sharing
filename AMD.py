import sys

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")

import ffield
import random

class AMD():

    def __init__(self,f):
        self.f = f
        self.F = ffield.FField(self.f)
        self.R = random.randint(2,2**(self.f)-1)
        print "The value of R is: " + str(self.R)

    def __truncate(self,code):
        to_return = []
        for i in range(0,len(code),self.f):
            to_return.append(code[i:i+self.f])
        return to_return

    def encode(self,S):

        trun_S = self.__truncate(S)

        bin_S0 = trun_S[0]
        bin_S1 = trun_S[1]
        bin_S2 = trun_S[2]

        int_S0 = int(bin_S0,2)
        int_S1 = int(bin_S1,2)
        int_S2 = int(bin_S2,2)

        int_E3 = self.F.Add(self.F.Multiply(int_S0,self.R),self.F.Add(self.F.Multiply(self.F.Multiply(self.R,self.R),int_S1),self.F.Multiply(self.F.Multiply(self.F.Multiply(self.R,self.R),self.R),int_S2)))
        bin_E3 = ('{0:0'+str(self.f)+'b}').format(int_E3)

        return bin_S0 + bin_S1 + bin_S2 + bin_E3


    def decode(self,E):

        trun_E = self.__truncate(E)

        bin_S0 = trun_E[0]
        bin_S1 = trun_E[1]
        bin_S2 = trun_E[2]
        bin_E3 = trun_E[3]

        int_S0 = int(bin_S0,2)
        int_S1 = int(bin_S1,2)
        int_S2 = int(bin_S2,2)
        int_E3 = int(bin_E3,2)

        eval_E3 = self.F.Add(self.F.Multiply(int_S0,self.R),self.F.Add(self.F.Multiply(self.F.Multiply(self.R,self.R),int_S1),self.F.Multiply(self.F.Multiply(self.F.Multiply(self.R,self.R),self.R),int_S2)))

        if eval_E3 == int_E3:
            return True
        else:
            return False



import sys

sys.path.append("/ad/eng/users/h/e/heinous/Desktop/Research/Secret_Sharing/Finite-Field")
sys.path.append("/home/heinous/Desktop/Research/SecretSharing/Secret_Sharing/Finite-Field")

import ffield

class SecretRecon():

    def __init__(self,f):
        self.f = f
        self.F = ffield.FField(self.f)

    def recon_2(self,chosen):

        denom = self.F.Add(int(chosen.keys()[0],2),int(chosen.keys()[1],2))
        nom = self.F.Add(int(chosen.values()[0],2),int(chosen.values()[1],2))
        E = self.F.Multiply(nom,self.F.Inverse(denom))
        return '{0:032b}'.format(E)

    def recon_3(self,chosen):

        E = 0
        for x in chosen.keys():
            D = chosen[x]
            nom = int(D,2)
            denom = 1
            for y in chosen.keys():
                if y != x:
                    denom = self.F.Multiply(denom,self.F.Add(int(x,2),int(y,2)))
            E = self.F.Add(E,self.F.Multiply(nom,self.F.Inverse(denom)))
        return '{0:032b}'.format(E)

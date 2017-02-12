import sys
import itertools

class GroupTesting():

    def __init__(self,n,k):
        self.n = n
        self.k = k

    def genMatrix(self):
        matrix = []
        lst = list(itertools.product([0, 1], repeat=self.n))

        for combination in lst:
            if combination.count(1) == self.k:
                matrix.append(combination)

        return matrix



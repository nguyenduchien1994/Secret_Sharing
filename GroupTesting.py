import sys
import itertools
import operator as op

class GroupTesting():

    def __init__(self,n,k):
        self.n = n
        self.k = k

    def genMatrix(self):
        matrix = []
        lst = list(itertools.product([0, 1], repeat=self.n))

        for combination in lst:
            if combination.count(1) == self.k:
                matrix.append(list(combination))

        return matrix

    def transpose(self,matrix):

        t_matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]

        return t_matrix

    def nCr(self,n,r):

        r = min(r, n-r)
        if r == 0: return 1
        numer = reduce(op.mul, xrange(n, n-r, -1))
        denom = reduce(op.mul, xrange(1, r+1))
        return numer//denom


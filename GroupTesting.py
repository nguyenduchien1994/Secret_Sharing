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
                matrix.append(list(combination))

        return matrix

    def transpose(self,matrix):

        t_matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]

        return t_matrix



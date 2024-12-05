#!usr/bin/env python3

import constraint as c
from itertools import combinations


def main():

    p = c.Problem()

    size = 4
    xs = range(size)

    p.addVariable(xs, xs)
    p.addConstraint(c.AllDifferentConstraint())

    def difDiagonal(col1, col2):
        def actualDiagonal(row1, row2):
            return abs(col1 - col2) != abs(row1 - row2)
        return actualDiagonal
    
    for (x1, x2) in combinations(xs, 2):
        p.addConstraint(difDiagonal(x1, x2), (x1, x2))
    
    sol = p.getSolutions()
    print(sol)


main()

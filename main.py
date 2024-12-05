#!usr/bin/env python3

import constraint as c

def main():

    p = c.Problem()

    p.addVariable("Pedro", ["pizza", "pollo"])
    p.addVariable("Marta", ["pizza", "hamburguesa"])
    p.addVariable("Pilar", ["pizza", "pollo", "hamburguesa"])

    def areEqual(a, b):
        return a==b
    
    x = areEqual

    p.addConstraint(areEqual, ["Pedro", "Marta"])
    p.addConstraint(areEqual, ["Pedro", "Pilar"])
    p.addConstraint(areEqual, ["Marta", "Pilar"])
    
    sol = p.getSolver()

    print(sol.getSolution())

if __name__ == "__main__":
    main()

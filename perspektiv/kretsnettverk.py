import sympy as sym

A = sym.Matrix([[-15,5,0, -230],[5,-23,7, 0],[0,7,-17, 9]])

sym.pprint(A.rref())


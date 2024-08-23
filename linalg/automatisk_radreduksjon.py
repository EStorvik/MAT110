import sympy as sym

A = sym.Matrix([[1,2,1,4],[3,8,7,20], [2,7,9,23]])

sym.pprint(A.rref())
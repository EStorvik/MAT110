import sympy as sym

A = sym.Matrix ( [ [ 1 , 1 , 1 ] , [ 1 , 1 , 2 ] , [ 2 , 1 , 1 ] ] )
I = sym.eye( 3 )
M = A.row_join(I)
sym.pprint(M.rref())
import sympy as sym
import numpy as np
import matplotlib.pyplot as plt

A = sym.Matrix([[0,0,0,0,1],[1,1,1,1,1],[2**4, 2**3, 2**2, 2**1, 2**0], [3**4, 3**3, 3**2, 3**1, 3**0], [4**4, 4**3, 4**2, 4**1, 4**0]])
b = sym.Matrix([[1],[3.2],[5.6],[-2],[7]])

sym.pprint(A)
a = A.inv()*b
print(a)
def f(x):
    return a[0]*x**4+a[1]*x**3+a[2]*x**2+a[3]*x+a[4]

xx = np.linspace(0,4,1000)
plt.figure("plotting 5 order polynomial")
plt.plot(xx,f(xx))
plt.show()


# ______________________
def f(x):
    return x**3 - 2*x - 5

# ______________________
def dfdx(x):
    return 3*x**2 - 2

# ______________________
def newtons_metode(x, f, dfdx, tol=1e-10, max_iter=100):
    """
    Newtons metode for å finne nullpunkt av f(x)

    argumenter:
        x: ________
        f: ________
        dfdx: ________
        tol: ________
        max_iter: ________
    
    Returnerer: ____, ____"""
    # __________________
    for i in range(max_iter):
        # __________________
        x = x - f(x)/dfdx(x)
        # __________________
        if abs(f(x)) < tol:
            break
    # __________________
    return x, i

# ______________________
x, i = newtons_metode(3, f, dfdx)
print(f"____ {x} _____ {i} ____")
import os

flag = os.environ.get("FLAG", "neko{the_neko_must_fit_to_the_hyperelliptic}")
p = random_prime(2 ** 512)

xv = randint(0, p-1)
yv = int(flag.encode().hex(), 16)

assert yv < p

g = 2
PR.<x> = PolynomialRing(GF(p))
f = sum(randint(0, p-1)*x**i for i in range(2*g + 1 + 1))
F = f + (yv**2 - f.subs({x: xv}))

HC = HyperellipticCurve(F, 0)
J = HC.jacobian()(GF(p))

D = J(HC((xv, yv)))
print(f"p = {p}")
for i in range(2, 5):
    k = i*(i+1)
    print(k*D)



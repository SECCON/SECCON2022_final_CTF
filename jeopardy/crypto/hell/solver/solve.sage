f = open("output.txt")

p = int(f.readline().strip().split(" = ")[1])
PR.<x> = PolynomialRing(GF(p))
y = 0

R = [
    sage_eval(f.readline().strip(), locals=locals()),
    sage_eval(f.readline().strip(), locals=locals()),
    sage_eval(f.readline().strip(), locals=locals()),
]


# (b[i]**2 - F) % a[i] == 0
xs = [PR(R[i][1])**2 % PR(R[i][0]) for i in range(len(R))]
mods = [PR(R[i][0]) for i in range(len(R))]
F = CRT(xs, mods)
print("[debug] F =", F)

HC = HyperellipticCurve(F, 0)
J = HC.jacobian()(GF(p))

E = J(R[2]) - (J(R[0]) + J(R[1]))
P = HC.lift_x(E[0].nth_root(2).monic().roots()[0][0])
print(bytes.fromhex(hex(P[1])[2:]))

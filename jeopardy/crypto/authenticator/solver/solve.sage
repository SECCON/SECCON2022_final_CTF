from ptrlib import Socket
import time
import os

HOST = os.environ.get("SECCON_HOST", "localhost")
PORT = os.environ.get("SECCON_PORT", "9999")

PR.<x> = PolynomialRing(GF(2))
g = PR(Integer(0xcd8da4ff37e45ec3).bits()[::-1]) + x**64
n = g.degree()

QR.<x> = QuotientRing(PR, g)
PPR.<X> = PolynomialRing(QR)


def i2p(x):
    return PR(Integer(x).bits())


def p2i(p):
    return Integer(p.list(), 2)


def rev(p, size):
    return PR((p.list() + [0] * size)[:size][::-1])



sock = Socket(HOST, int(PORT))


# get key from hint
sock.sendlineafter("> ", "H")
t = int(time.time()) // 5 * 5
hint = int(sock.recvlineafter("hint: "), 16)

# W = crc("hint", X)
data = b"hint"
k2 = len(data) * 8
W = rev(i2p(int.from_bytes(data, "little")), k2)
f = W*x**n + X*x**k2 - rev(i2p(hint), 64)
O = f.roots()[0][0]

# O = crc(X, 0)
k = 8 * 8
I = rev(i2p(0), n)
W = X*x**n + I*x**k  # should be reversed
f = W - O  # rev(O) = rev(X*x**n)
Kt = p2i(rev(f.roots()[0][0], 64))

K = Kt ^^ t


# find key
t = int(time.time()) // 5 * 5
k = 64
W = i2p(K ^^ t)
W = rev(W, k)
value = W*x^n +  X*x^k
f = value - X
code = p2i(rev(f.roots()[0][0], k))

# send
print("input:", hex(code)[2:])
sock.sendlineafter("> ", "A")
sock.sendlineafter("code: ", hex(code)[2:])
print(sock.recv())

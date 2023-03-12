from .iproblem import IProblem
from typing import Optional
import secrets
from Crypto.Util.number import *
import gmpy
import time
import random
import matplotlib.pyplot as plt

def square_root(n, p):
    n %= p
    if pow(n, (p-1)>>1, p) != 1:
        return -1
    q = p-1; m = 0
    while q & 1 == 0:
        q >>= 1
        m += 1
    z = random.randint(1, p-1)
    while pow(z, (p-1)>>1, p) == 1:
        z = random.randint(1, p-1)
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q+1)>>1, p)
    if t == 0:
        return 0
    m -= 2
    while t != 1:
        while pow(t, 2**m, p) == 1:
            c = c * c % p
            m -= 1
        r = r * c % p
        c = c * c % p
        t = t * c % p
        m -= 1
    return r

class EC:
    def __init__(self):
        self.p = 1009
        self.field = [[0 for i in range(self.p)] for j in range(self.p)]
        self.ans = [0]*(self.p*self.p)

        self.a = random.randrange(1,self.p)
        self.b = random.randrange(1,self.p)
        # y^2 = x^3 + a*x + b
        self.points = []

        for x in range(self.p):
            for y in range(1, self.p):
                if (y*y) % self.p == (x*x*x + self.a * x + self.b) % self.p:
                    self.points.append((x,y))
                    self.points.append((x,self.p-y))
                    self.field[y][x] = 1
                    self.field[self.p - y][x] = 1
                    self.ans[self.p*y + x] = 1
                    self.ans[self.p*(self.p-y) + x] = 1

        self.x, self.y = self.points[random.randrange(0,len(self.points))]

        for p in self.points:
            x, y = p
            assert y*y % self.p == (x*x*x + self.a * x + self.b) % self.p
        
        assert self.y*self.y % self.p == (self.x*self.x*self.x + self.a * self.x + self.b) % self.p
    
    def get_field(self):
        res = [[0 for i in range(1009)] for j in range(1009)]
        for p in self.points:
            res[p[1]][p[0]] = 1

        for i in range(self.p):
            res[i][self.x] = 1
            res[self.y][i] = 1
        return res

    def get(self):
        ans = [0] * (1009*1009)
        for p in self.points:
            ans[p[1] * self.p + p[0]] = 1

        for i in range(self.p):
            ans[i * self.p + self.x] = 1
            ans[self.y * self.p + i] = 1
        return ans 
    
    def next(self):
        phi = (3*self.x*self.x + self.a) * pow(2*self.y, -1, self.p)
        psi = (-3*self.x*self.x*self.x - self.a*self.x + 2 * self.y * self.y) * pow(2*self.y, -1, self.p)
        self.x = (phi * phi - 2 * self.x) % self.p
        self.y = (-phi * self.x - psi) % self.p
        assert self.y*self.y % self.p == (self.x*self.x*self.x + self.a * self.x + self.b) % self.p
    
    def oracle(self,ans):
        print(self.x, self.y)
        cnt = 0
        for l,r in zip(ans, self.get()):
            if l == r:
                cnt += 1
        self.next()
        return cnt
    
    def index_to_pos(self, index):
        return (index // self.p), (index % self.p)

    def field_to_ans(self, field):
        ans = []
        for i in range(len(field)):
            for j in range(len(field[i])):
                ans.append(field[i][j])
        return ans

ec = EC()
p = ec.p

offset = 0
prev_score = 0
posses = []


zeroy = 0
for i in range(p):
    print(ec.oracle([2]*p*i + [1]*p))
    if ec.oracle([2] * p*i + [1] * p) == 1:
        zeroy = i
        break

yoffset = zeroy + 1
for _ in range(2):
    for i in range(yoffset, p):
        base = [2] * (p * p)
        for j in range(p):
            base[zeroy * p + j] = 1

        res = ec.oracle(base)

        for j in range(p):
            base[i * p + j] = 1
        res = ec.oracle(base)

        if res == 3:
            yoffset = i
            break

    high = 1009
    low = 0 
    while high - low > 1:
        mid = (high + low) // 2
        a = [1] * mid

        base = [2] * (p * p)

        for j in range(mid):
            base[zeroy * p + j] = 1
        for j in range(mid):
            base[yoffset*p + j] = 1

        res = ec.oracle(base) % 2
        if res == 0:
            low = mid
        else:
            high = mid

    print(ec.ans[yoffset*p:yoffset*p+high])
    A = [0] * (high-1) + [1]
    y, x = ec.index_to_pos(yoffset*p+high-1)
    print("test:", ec.field[y][x])
    offset += high+2
    prev_score += 1
    posses.append((y,x))
    yoffset += 1

Xs = []
for pos in posses:
    Xs.append(pos[0]*pos[0] - pos[1] * pos[1] * pos[1] % p)

a = (Xs[1]-Xs[0]) * pow(posses[1][1] - posses[0][1], -1, p) % p
y, x = posses[0]
b = (y*y - x*x*x - a * x) % p
print(a,b)

width = p//2
zeroy = 0
results = []
for i in range(10):
    print(ec.x < width)
    results.append(ec.oracle([2]*p*zeroy + [1] * width))

xpoints = []
for x in range(p):
    xx = x
    y = square_root(x*x*x + a * x + b, p) % p
    if y*y % p == 1:
        continue

    print("==================================================")
    print(x,y)
    print("--------------------------------------------------")
    print(y*y % p)
    print((x*x*x + a *x + b) % p)
    print("--------------------------------------------------")

    assert y*y % p == (x*x*x + a *x + b) % p
    if y == 0:
        continue
    f = True
    for j in range(10):
        if (True if x < width else False) != results[j]:
            print("error")
            f = False
        print(x,y)
        phi = (3*x*x + a) * pow(2*y, -1, p)
        psi = (-3*x*x*x - a*x + 2 * y * y) * pow(2*y, -1, p)
        x = (phi * phi - 2 * x) % p
        y = (-phi * x - psi) % p
        if y == 0 or x == 0:
           f = False 
           break
        assert y*y % p == (x*x*x + a *x + b) % p
    if f:
        xpoints.append(xx)
        print("true:", xx)

print("point:")
print(xpoints)
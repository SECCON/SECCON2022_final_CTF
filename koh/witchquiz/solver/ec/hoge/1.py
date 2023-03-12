import secrets
from Crypto.Util.number import *
import gmpy
import time
import random
import sys

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

tickcnt = 0

def score(answer):
    import requests
    import json
    url = "http://127.0.0.1:8080/api/quiz/"

    token = sys.argv[1]
    your_token = token # please enter your token
    headers = {'Authorization': 'Token ' + your_token}

    params = json.dumps({"answer": answer, 'stage': 2})
    print(len(answer))

    score = 0
    while True:
        print("requests start")
        try:
            res = requests.post(url, data=params, headers=headers)
        except:
            continue
        print("requests end")
        print(res.text)
        if res.status_code == 200:
            res = json.loads(res.text)

            score = res["score"]
            print(f"tick={res['tick']}, score={score}")
            break
        time.sleep(0.1)

    return score

def get_y(x,a,b):
    y = square_root(x*x*x + a*x + b, p) % p
    return y

def next(x,y,a,b):
    phi = (3*x*x + a) * pow(2*y, -1, p)
    psi = (-3*x*x*x - a*x + 2 * y * y) * pow(2*y, -1, p)
    x = (phi * phi - 2 * x) % p
    y = (-phi * x - psi) % p
    return x,y

p = 1009
offset = 0
prev_score = 0
posses = []
tickcnt = 0

print("phase1")
zeroy = 0
for i in range(p):
    if score([2]*p*i + [1]*p) == 1:
        zeroy = i
        break

print("phase2")
yoffset = zeroy + 1
for _ in range(2):
    for i in range(yoffset, p):
        base = [2] * (p * p)
        for j in range(p):
            base[zeroy * p + j] = 1

        res = score(base)

        for j in range(p):
            base[i * p + j] = 1
        res = score(base)

        if res == 3:
            yoffset = i
            break

    high = 1009
    low = 0 
    while high - low > 1:
        print(f"high={high}, low={low}")
        mid = (high + low) // 2
        a = [1] * mid

        base = [2] * (p * p)

        for j in range(mid):
            base[zeroy * p + j] = 1
        for j in range(mid):
            base[yoffset*p + j] = 1

        res = score(base) % 2
        if res == 0:
            low = mid
        else:
            high = mid

    A = [0] * (high-1) + [1]
    y, x = yoffset, high-1
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
print(f"a={a}, b={b}")

print("phase3")

width = p//2
zeroy = 0
results = []
for i in range(10):
    results.append(score([2]*p*zeroy + [1] * width))

result_points = []
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

        x, y = next(x,y,a,b)
        print(x,y)
        if y == 0 or x == 0:
           f = False 
           break
        assert y*y % p == (x*x*x + a*x + b) % p
    if f:
        result_points.append((x,y))
        print("true:", x, y)

print("point:")
cands = []
for x, _ in result_points:
    y = get_y(x, a, b)
    print(x,y)
    print(x,p-y)
    cands.append((x,y))
    cands.append((x,p-y))

for i in range(len(cands)):
    x,y = cands[i]
    print("memomemo:", i,x,y)

    for j in range(i):
        phi = (3*x*x + a) * pow(2*y, -1, p)
        psi = (-3*x*x*x - a*x + 2 * y * y) * pow(2*y, -1, p)
        x = (phi * phi - 2 * x) % p
        y = (-phi * x - psi) % p

    ans = [0] * (1009*1009)
    for xx in range(p):
        for yy in range(1, p):
            if (yy*yy) % p == (xx*xx*xx + a * xx + b) % p:
                ans[yy * p + xx] = 1

    for i in range(p):
        ans[i * p + x] = 1
        ans[y * p + i] = 1

    print("--------------------------------------------------")
    print(score(ans))
    print("--------------------------------------------------")

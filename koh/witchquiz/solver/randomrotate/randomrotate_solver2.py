from typing import Optional
import secrets
from fractions import Fraction

class LCG:
    def __init__(self, seed, m):
        self.a = 2
        self.seed = seed
        self.m = 2*m + 1

    def rand(self):
        self.seed = (self.seed * 2) % self.m
        return (self.seed * self.a) % self.m

def generator():
    N = 65536
    ans = [(x+1) for x in range(N)]
    seed = int(secrets.token_hex(16), 16)
    # m = int(secrets.token_hex(16), 16)
    m = 272468326198554491379699426769250460883 # public

    lcg = LCG(seed, m)

    debug = []
    for i in range(N-1, 0, -1):
        r = lcg.rand()
        debug.append(r)
        j = r % i
        ans[i], ans[j] = ans[j], ans[i]

    rotate_sums = [0]
    for ticks in range(10000):
        rotate_sums.append((rotate_sums[-1] + (lcg.rand() % N)) % N)

    return ans, rotate_sums

# if __name__ == '__main__':
#     ans, rotate_sums, debug, m = generator()
#     print(f"ans = {ans}")
#     print(f"rotate_sums = {rotate_sums}")
#     print(f"debug = {debug}")
#     print(f"m = {m}")

temp = []

scores = []
for i in range(1000):
    # ToDo anses
    scores.append(rr.score(i+1, answer=[1,0]*(65536//2)))

lsbs = []
for i in range(len(scores)-1):
    lsbs.append(scores[i+1] ^ scores[i])

low = Fraction(0, 1)
high = Fraction(m, 1)

for i in range(len(lsbs)):
    mid = (low+high)/2
    if lsbs[i] == 0:
        high = mid
    else:
        low = mid

assert low.__ceil__() == high.__floor__()

rands = [low.__ceil__()]
for i in range(65534):
    rands.append(rands[-1] * pow(2,-1,m) % m)
rands.reverse()
for i in range(10000):
    rands.append(rands[-1] * 2 % m)


N = 65536
ans = [(x+1) for x in range(N)]
seed = int(secrets.token_hex(16), 16)
m = int(secrets.token_hex(16), 16)
rands_index = 0

for i in range(N-1, 0, -1):
    r = rands[rands_index]
    rands_index += 1
    j = r % i
    ans[i], ans[j] = ans[j], ans[i]

rotate_sums = [0]
for ticks in range(10000):
    r = rands[rands_index]
    rands_index += 1
    rotate_sums.append((rotate_sums[-1] + (r % N)) % N)

tick = 1000

print(ans)
r = rotate_sums[tick-1]
ans = ans[r:] + ans[:r]

print(rr.score(tick, answer=ans))
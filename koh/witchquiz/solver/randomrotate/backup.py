from typing import Optional
import secrets
from fractions import Fraction
from typing import Optional
import secrets
from fractions import Fraction

class RandomRotate():
    def score(self, tick: int, answer: Optional[list[int]]) -> int:
        tick += 0

        if answer == None:
            return 0

        from randomrotate_ans import ans, rotate_sums
        r = rotate_sums[tick-1]
        ans = ans[r:] + ans[:r]

        cnt = 0
        for l, r in zip(answer, ans):
            cnt += (1 if l == r else 0)
        return tick, cnt

class LCG:
    def __init__(self, seed, m):
        self.a = 2
        self.seed = seed
        self.m = m

    def rand(self):
        self.seed = (self.seed * 2) % self.m
        return (self.seed * self.a) % self.m

def generator():
    N = 65536
    ans = [(x+1) for x in range(N)]
    seed = int(secrets.token_hex(8), 16)
    # m = int(secrets.token_hex(8), 16) * 2 + 1
    m = 27652344047805921227 # public

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

rr = RandomRotate()
m = 27652344047805921227
start_tick = 100000000
last_tick = 0

temp = []

scores = []
for i in range(256):
    # ToDo anses
    tick, score = rr.score(i+1, answer=[1,0]*(65536//2))
    start_tick = min(tick, start_tick)
    last_tick = max(tick, last_tick)
    scores.append(score)

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
for i in range(65534 + start_tick - 1):
    rands.append(rands[-1] * pow(2,-1,m) % m)
rands.reverse()
for i in range(10000 - (start_tick - 1)):
    rands.append(rands[-1] * 2 % m)

N = 65536
ans = [(x+1) for x in range(N)]
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

tick = last_tick + 5
print(ans)
r = rotate_sums[tick-1]
ans = ans[r:] + ans[:r]

print(rr.score(tick, answer=ans))
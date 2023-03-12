from typing import Optional
import secrets
from fractions import Fraction
from typing import Optional
import secrets
from fractions import Fraction
import sys

def get_score(tick: int, answer) -> int:
    import requests
    import json
    url = "http://localhost/api/quiz/"

    your_token = sys.argv[1]
    headers = {'Authorization': 'Token ' + your_token}

    params = json.dumps({"answer": answer, 'stage': 4, 'tick': tick})

    while True:
        res = requests.post(url, data=params, headers=headers)
        print(res.text)
        if res.status_code == 200:
            r = json.loads(res.text)
            print(f"tick={r['tick']}, score={r['score']}")
            tick = r['tick']
            score = r['score']
            return tick, score

m = 27652344047805921227
start_tick = 100000000
last_tick = 0
offset = 4

temp = []

scores = []
for i in range(66):
    # ToDo anses
    tick, score = get_score(i+offset, answer=[1,0]*(65536//2))
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

tick = last_tick + 1
print(ans)
r = rotate_sums[tick-1]
ans = ans[r:] + ans[:r]

print("target_tick:", tick)
while True:
    print(get_score(tick, answer=ans))

from typing import Optional
import secrets
from fractions import Fraction
import requests
import json
import time

def score(my):
  while True:
    url = "http://localhost:8080/api/quiz/"

    your_token = 'user1Token' # please enter your token
    headers = {'Authorization': 'Token ' + your_token}

    params = json.dumps({"answer": my, 'stage': 3})
    res = requests.post(url, data=params, headers=headers)
    print(res.text)
    if res.status_code == 200:
        res = json.loads(res.text)
        return res['score'], res['tick']
    time.sleep(1)
counter = 0

ans = []
for _ in range(1000000):
    ans.append(int(secrets.token_hex(1), 16) % 2)

decided = []
temporary = []

prev = 0
for i in range(3480):
    print(_)
    a = [0] * (100000//100 + 1)
    result, tick = score(decided + a)
    if result - prev <= len(a)//2:
        decided += [1] * (100000//100 + 1)
    else:
        decided += [0] * (100000//100 + 1)
    prev = result
    if i % 28 == 0:
        result, tick = score(decided + [0] * (100000-len(decided)))
        result, tick = score(decided + [1] * (100000-len(decided)))

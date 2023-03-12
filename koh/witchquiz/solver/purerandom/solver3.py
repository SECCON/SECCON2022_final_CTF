from typing import Optional
import secrets
from fractions import Fraction
import secrets
import json
import requests
import time


def score(tick, my):
  while True:
    url = "http://127.0.0.1:8000/api/quiz/"

    your_token = 'user1Token' # please enter your token
    headers = {'Authorization': 'Token ' + your_token}

    params = json.dumps({"answer": my, 'stage': 1, 'tick': tick})
    res = requests.post(url, data=params, headers=headers)
    print(res.text)
    if res.status_code == 200:
        res = json.loads(res.text)
        print(res['score'], res['tick'])
        return res['score'], res['tick']
    time.sleep(0.5)

ans = []
for i in range(10,1440):
    print(score(i+1, [i+1]))

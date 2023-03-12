from typing import Optional
import secrets
from fractions import Fraction
import secrets
import json
import requests
import time


def score(my, tick):
  while True:
    url = "http://127.0.0.1:8000/api/quiz/"

    your_token = 'BDj4fkkM69uxWAvxI1y-K9QHIOyF1aU2jwtlKiJR95o=' # please enter your token
    headers = {'Authorization': 'Token ' + your_token}

    params = json.dumps({"answer": my, 'stage': 1, 'tick': tick})
    res = requests.post(url, data=params, headers=headers)
    print(res.text)
    if res.status_code == 200:
        res = json.loads(res.text)
        print(res['score'], res['tick'])
        return res['score']
    time.sleep(0.5)

score([201], 6)

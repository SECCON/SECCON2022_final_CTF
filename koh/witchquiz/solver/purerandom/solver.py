import requests
import json
import time
import sys

url = "http://localhost:8080/api/quiz/"
your_token = sys.argv[1] # please enter your token
headers = {'Authorization': 'Token ' + your_token}

def score(answer, tick):
    while True:
        params = json.dumps({
        'answer': [tick] +answer, # [required] your answer (Substituted into `your_answer` in the code)
        'stage': 1, # [required] this stage number. please use this value for this stage :)
        'tick': tick # [optional] specify the current tick or less (If omitted, the maximum value of ticks that can be submitted at the time of submission will be adopted.)
        })
        res = requests.post(url, data=params, headers=headers)

        # Returns 200 if accepted. otherwise returns not 200
        if res.status_code == 200:
            print(res.text)
            return json.loads(res.text)['score']
        else:
            print("error:", res.text)
        time.sleep(0.5)

tick = 10
decided = []
while True:
    tick = tick + 1
    a = score(decided + [0], tick)
    if a == len(decided) + 2:
        decided.append(0)
    else:
        decided.append(1)

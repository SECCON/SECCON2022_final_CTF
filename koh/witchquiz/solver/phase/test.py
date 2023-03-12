import requests
import json
url = "http://localhost/api/quiz/"

your_token = "jeCU-Qicr8jEvHcp06cCc7Cix49ikfcxoif32pOhPjA=" # please enter your token
headers = {'Authorization': 'Token ' + your_token}

while True:
    params = json.dumps({
      'answer': [1]*100000, # [required] your answer (Substituted into `your_answer` in the code)
      'stage': 2, # [required] this stage number. please use this value for this stage :)
      'tick': 1440 # [optional] specify the current tick or less (If omitted, the maximum value of ticks that can be submitted at the time of submission will be adopted.)
      })
    res = requests.post(url, data=params, headers=headers)

    # Returns 200 if accepted. otherwise returns not 200
    if res.status_code == 200:
      print(res.text)
    else:
      print(res.text)
        

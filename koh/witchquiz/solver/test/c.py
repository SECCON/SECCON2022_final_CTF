import requests
import json
url = "http://localhost:8080/api/quiz/"

your_token = "30dZTgjsk5snKQtiGiCQBkWMIgEQEDh-gX8jx3gMbCg="
headers = {'Authorization': 'Token ' + your_token}

params = json.dumps({
  'answer': [0,1,2,3,4], # [required] your answer (Substituted into `your_answer` in the code)
  'stage': 4, # [required] this stage number. please use this value for this stage :)
  'tick': 1246 # [optional] you can choose: 1 <= tick <= 1246 && not yet submitted on that tick, If omitted, tick = 1246 (current tick)
  })
res = requests.post(url, data=params, headers=headers)

# Returns 200 if accepted. otherwise returns not 200
if res.status_code == 200:
  print("success:", res.text)
else:
  print("error:", res.text)

import requests
import json
url = "http://localhost/api/quiz/"

# please enter your token
your_token = "UT8_ccHK0IjB8NPhsV_WEnUoN0QPydYZI2NhyybyMc0="

headers = {'Authorization': 'Token ' + your_token}

params = json.dumps({
  'answer': [-1], # [required] your answer (Substituted into `your_answer` in the code)
  'stage': 2, # [required] this stage number. please use this value for this stage :)
  'tick': 1014 # [optional] you can choose: 1 <= tick <= 1014 && not yet submitted on that tick, If omitted, tick = 1014 (current tick)
  })
res = requests.post(url, data=params, headers=headers)

# Returns 200 if accepted. otherwise returns not 200
if res.status_code == 200:
  print("success:", res.text)
else:
  print("error:", res.text)

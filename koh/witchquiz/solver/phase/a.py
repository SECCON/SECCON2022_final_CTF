import requests
import json
url = "http://localhost:8080/api/quiz/"

your_token = # please enter your token
headers = {'Authorization': 'Token ' + your_token}

params = json.dumps({
  'answer': [0,1,2,3,4], # [required] your answer (Substituted into `your_answer` in the code)
  'stage': 2, # [required] this stage number. please use this value for this stage :)
  })
res = requests.post(url, data=params, headers=headers)

# Returns 200 if accepted. otherwise returns not 200
if res.status_code == 200:
  print("success:", res.text)
else:
  print("error:", res.text)

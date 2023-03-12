import requests
import json
url = "http://localhost/api/quiz/"

your_token = "stspD3iyqv8pnRmS1Z9RPHUvRRL3R7iyFJgEiC_Xr5Y=" # please enter your token
headers = {'Authorization': 'Token ' + your_token}

while True:
    print("start")
    params = json.dumps({
      'answer': [1]*(1009*1009), # [required] your answer (Substituted into `your_answer` in the code)
      'stage': 1, # [required] this stage number. please use this value for this stage :)
      })
    res = requests.post(url, data=params, headers=headers)
    print(res.text)

    # Returns 200 if accepted. otherwise returns not 200
    if res.status_code == 200:
      print(res.text)
    else:
      print(res.text)

from typing import Optional
import secrets
from fractions import Fraction
import secrets
import json
import requests
import time


url = "http://127.0.0.1:8000/api/quiz/"

your_token = 'qH4pS42mJ5gf2uvm_iAp2MFYfO0OR9gYey14RomIEpY=' # please enter your token
headers = {'Authorization': 'Token ' + your_token}

params = json.dumps(
        {
        'stage': 1,
        'tick':60 
        }
        )

res = requests.get(url, data=params, headers=headers)
print(res.text)

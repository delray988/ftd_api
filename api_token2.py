#!/bin/python

import sys
import requests

URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'
payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(sys.argv[2], sys.argv[3])
headers = {"Content-Type": "application/json", "Accept": "application/json"}

requests.packages.urllib3.disable_warnings()

response = requests.post(URL, data=payload, headers=headers, verify=False)
if response.status_code == 200:
   access_token = response.json().get('access_token')
   expiration = response.json().get('expires_in')
   print("the following access token: {} will expire in: {} seconds".format(access_token, expiration))
else: print("HTTP ERROR: {}".format(response.status_code))

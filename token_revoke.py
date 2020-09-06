#!/bin/python

"""
Revoke a token
"""

import requests
import sys
import os
import re

#read the contents of the access token text file into a variable
with open('access_token.txt', "r") as file:
   access_token = file.read().replace('\n', '')

URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'

payload = '{{"grant_type": "revoke_token", \
"access_token": "{}", \
"token_to_revoke": "{}"}}'.format(access_token, access_token)

headers = {"Content-Type": "application/json", "Accept": "application/json"} 

requests.packages.urllib3.disable_warnings()
response = requests.post(URL, data=payload, headers=headers, verify=False)

if response.status_code == 200:
   print('token revoked')
else:
   print("HTTP ERROR: {}".format(response.status_code))
   print("Server Error: {}".format(response.json().get('message')))

#!/bin/python

"""
Revoke a token
"""
import pdb
import requests
import sys
import os
import re

URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'

#Scan the current directory for any files named 'access_token.txt'
#If any are found revoke the token and delete the access_token.txt and refresh_token.txt files
print("Searching for tokens to revoke ...")
with os.scandir('./') as entries:
   token_count = 0
   for entry in entries:
      if re.search(r'access_token.txt\b', str(entry)) is not None:
         with open('access_token.txt', "r") as file:
            access_token = file.read().replace('\n', '')

         payload = '{{"grant_type": "revoke_token", \
             "access_token": "{}", \
             "token_to_revoke": "{}"}}'.format(access_token, access_token)
         headers = {"Content-Type": "application/json", "Accept": "application/json"} 


         requests.packages.urllib3.disable_warnings()
         response = requests.post(URL, data=payload, headers=headers, verify=False)

         if response.status_code == 200:
            print('token revoked')
            #os.remove('access_token.txt')
            #print('access_token.txt file removed')
            #os.remove('refresh_token.txt')
            #print('refresh_token.txt file removed')
         else:
            print("HTTP ERROR: {}".format(response.status_code))
            print("Server Error: {}".format(response.json().get('message')))
         token_count = 1
      else:
         pass

#if there are no detected files with '-access_token.txt' in the name
#let the user know
if token_count == 0:
   print("There were no detected access tokens")





#!/bin/python

"""
Revoke a custom token
"""
import requests
import sys
import os
import re
import shutil

#Scan the current directories that may contain custom tokens
#All custom token directories will end in '_token'
#Print to screen and give the user an input dialog to type name of custom token directory
print("Searching for tokens to revoke ...")
with os.scandir('./') as entries:
   token_count = 0
   for entry in entries:
      if re.search(r'_token\b', str(entry)) is not None:
         print(str(entry.name).rstrip('_token'))
         token_count = 1
      else:
         pass

#Request user input based on which custom token s\he wants to revoke
#set the path for the custom token's directory and read the
#original access token stored in 'access_token.txt'
if token_count != 0:
   token_name=input("Enter one of the names printed above: ")
   ct_dir= '/{}_token'.format(token_name)
   path = os.getcwd() + ct_dir
   file_path = path + '/access_token.txt'
   with open(file_path, "r") as file:
      access_token = file.read().replace('\n', '')

   #define the token api endpoint
   URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'
   #define the payload as a dictiionary object containing the original access token
   #as well as the name of the custom token
   payload = '{{"grant_type": "revoke_token", \
             "access_token": "{}", \
             "custom_token_subject_to_revoke": "{}"}}'.format(access_token, token_name)
   #Send in JSON format and accept on JSON back
   headers = {"Content-Type": "application/json", "Accept": "application/json"}

   #disable warnings
   requests.packages.urllib3.disable_warnings()
   response = requests.post(URL, data=payload, headers=headers, verify=False)

   if response.status_code == 200:
      print('custom token revoked')
   else:
      print("HTTP ERROR: {}".format(response.status_code))
      print("Server Error: {}".format(response.json().get('message')))

else:
   #if there are no detected directories with '_token' in the name
   #let the user know
   print("There were no detected custom tokens")






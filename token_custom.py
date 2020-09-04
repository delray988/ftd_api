#!/bin/python

"""
Create a custom token from the password grant access token request that was
written to the access_token.txt file from the token_request.py script
"""

"""
TODO:
Create the custom tokens in the '/tmp/' directory
update token_custom_revoke.py to read from /tmp/ and delete revoked tokens afterwards

"""

import requests
import os
import sys
import shutil
import pdb

ftd = sys.argv[1]
token_name = input("Enter name of token: ")
expiration = input("Enter amount of seconds for expiration: ")
ref_expiration =  int(expiration) * 2
ref_count = input("Enter amount of times you want to refresh: ")

URL = 'https://' + ftd + ':443/api/fdm/latest/fdm/token'

#Read the access_token file as a variable for the payload
#Reading the contents within a 'with' will allow you to close the file
#and is a good idea to make a habit for good coding practices
with open('access_token.txt', 'r') as file:
    original_access_token = file.read().replace('\n', '')

#pdb.set_trace()
payload= '{{"grant_type": "custom_token", \
"access_token": "{}", \
"desired_expires_in": {}, \
"desired_refresh_expires_in": {}, \
"desired_subject": "{}", \
"desired_refresh_count": {}}}'.format(original_access_token, expiration, ref_expiration, token_name, ref_count)

headers = {"Content-Type": "application/json", "Accept": "application/json"}

requests.packages.urllib3.disable_warnings()
response = requests.post(URL, data=payload, headers=headers, verify=False)

if response.status_code == 200:

   #Create a directory named after the custom access token
   #format the created directory to not include the quotes in its name
   #Move the original access token stored in access_token.txt to the custom token directory
   ct_dir = "{}_token".format(token_name)
   os.mkdir(ct_dir.rstrip("'"))
   shutil.move('access_token.txt', ct_dir)

   #Retrieve the custom access token from the JSON response and store it in a variable
   #Write the token to file and move it to the directory named after custom token
   custom_token = response.json().get('access_token')
   with open("custom_token.txt", "w") as text_file:
      print("{}".format(custom_token), file=text_file)
   shutil.move('custom_token.txt', ct_dir)

   #Retrieve the refresh token for the custom token from the JSON response and store it in a variable
   #Write the refresh token to file and move it to the directory named after the custom token
   ref_token = response.json().get('refresh_token')
   with open("refresh_token.txt", "w") as text_file:
      print("{}".format(ref_token), file=text_file)
   shutil.move('refresh_token.txt', ct_dir)

else:
   print("HTTP ERROR: {}".format(response.status_code))
   print("Server Error: {}".format(response.json().get('message')))


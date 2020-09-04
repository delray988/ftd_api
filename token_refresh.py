#!/bin/python

"""
Take an access token and a refresh token as input
to refresh the token for further operations
"""

import requests
import pdb
import sys

#read the contents of the text file containing the refresh token
#and define it to the ref_token variable
with open("refresh_token.txt", 'r') as file:
   ref_token = file.read().replace('\n', '')

#define the token api endpoint
URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'
#define the payload as a dictionary object containing the refresh token
payload = '{{"grant_type": "refresh_token", "refresh_token": "{}"}}'.format(ref_token)
#Ensure the server knows we are sending JSON formatted data and expect JSON format back
headers = {"Content-type": "application/json", "Accept": "applications/json"}

#pdb.set_trace()

#disable warnings
requests.packages.urllib3.disable_warnings()
#the "verify=False" is to turn off SSL CA verification
response = requests.post(URL, data=payload, headers=headers, verify=False)

if response.status_code == 200:
   #retrieve the access token from the json response and define it in the below variable
   access_token = response.json().get('access_token')
   #write the access token to a file for reuse 
   ##using the 'with' statement as a context manager to close the file after write
   with open("access_token.txt", "w") as text_file:
      print("{}".format(access_token), file=text_file)

   #retrieve the refresh token from the json response and define it in the below variable
   ref_token = response.json().get('refresh_token')
   #write the refresh token to a text file for reuse 
   #using the 'with' statement as a context manager to close the file after write
   with open("refresh_token.txt", "w") as text_file:
      print("{}".format(ref_token), file=text_file)

else:
   #if there is a different http response code print the code
   #along with retrieving the returned server error message for further troubleshooting
   print("HTTP ERROR: {}".format(response.status_code))
   print("Server Message: {}".format(response.json().get('message')))

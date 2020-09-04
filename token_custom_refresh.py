#!/bin/python

"""
Take an access token and a refresh token as input
to refresh the token for further operations
"""

import requests
import pdb
import sys
import re
import shutil
import os

#Scan the current directories that may contain custom tokens 
#All custom token directories will end in '_token'
#Print to screen and give the user an input dialog to type name of custom token directory
print("Searching for tokens to refresh ...")
with os.scandir('./') as entries:
   token_count = 0
   for entry in entries:
      if re.search(r'_token\b', str(entry)) is not None: 
         print(str(entry.name).rstrip('_token'))
         token_count = 1
      else:
         pass

#Request user input based on which custom token s\he wants to refresh
#set the path for the custom token's directory and read the
#refresh token stored in 'refresh_token.txt' 
if token_count != 0:
   token_name=input("Enter one of the names printed above: ")
   ct_dir= '/{}_token'.format(token_name)
   path = os.getcwd() + ct_dir
   ref_file_path = path + '/refresh_token.txt'
   with open(ref_file_path, 'r') as file:
      ref_token = file.read().replace('\n', '')

   #define the token api endpoint
   URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'
   #define the payload as a dictionary object containing the refresh token
   payload = '{{"grant_type": "refresh_token", "refresh_token": "{}"}}'.format(ref_token)
   #Ensure the server knows we are sending JSON formatted data and accept only JSON format back
   headers = {"Content-type": "application/json", "Accept": "applications/json"}

   #disable warnings
   requests.packages.urllib3.disable_warnings()
   #the "verify=False" is to turn off SSL CA verification
   response = requests.post(URL, data=payload, headers=headers, verify=False)

   if response.status_code == 200:
      #retrieve the access token from the json responsee
      #and define the custom_token variable
      custom_token = response.json().get('access_token')
      #write the custom token to the custom_token.txt file
      #using the 'with' statement as a context manager to close the file after write
      ct_file_path = path + '/custom_token.txt'
      with open(ct_file_path, "w") as text_file:
         print("{}".format(custom_token), file=text_file)

      #retrieve the refresh token from the json response and define it in the below variable
      ref_token = response.json().get('refresh_token')
      #write the refresh token to a text file for reuse 
      #using the 'with' statement as a context manager to close the file after write
      rt_file_path = path + '/refresh_token.txt'
      with open(rt_file_path, "w") as text_file:
         print("{}".format(ref_token), file=text_file)

   else:
      #if there is a different http response code print the code
      #along with retrieving the returned server error message for further troubleshooting
      print("HTTP ERROR: {}".format(response.status_code))
      print("Server Message: {}".format(response.json().get('message')))

else:
   print("There were no detected custom tokens")

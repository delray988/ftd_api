#!/bin/python

import sys
import requests

"""
Request the neccessary access token to make API calls
Call this script from the command line with three arugments in order of:
IP/HostName Username Password

TODO:write the tokens to the /tmp/ directory
"""

#if you are not sure of the api version you can substitute it for "latest"
#Use the first kwarg from the cmdline for the location of the ftd and build a URL
URL = 'https://' + sys.argv[1] + ':443/api/fdm/latest/fdm/token'
#passing the payload off as a dictionary with the cmd line kwargs for username and password
payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(sys.argv[2], sys.argv[3])
#we are sending a payload in json format and expect the same response in json
headers = {"Content-Type": "application/json", "Accept": "application/json"}

#disable warnings
requests.packages.urllib3.disable_warnings()
#the "verify=False" is to turn off SSL CA verification
response = requests.post(URL, data=payload, headers=headers, verify=False)

if response.status_code == 200:

   #retrieve the access token from the json response and define it in the below variable
   access_token = response.json().get('access_token')
   #write the access token to a file for reuse
   #using the 'with' statement as a context manager to close the file after write
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
   print("Server Error: {}".format(response.json().get('message')))

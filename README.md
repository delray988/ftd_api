# ftd_api
Firepower Threat Defense Rest API scripts

This repository contains independent scripts for working with the FTD REST API OAUTH tokens.

The token request, refresh and revoke scripts are to be called as "$ python3 token_request.py "ftd ip_address" "username" "password"
while the other scripts just requre the "ftd ip_address" parameter

The token handler script contains a single function to handle requesting, refreshing and revoking of the access token. Experiment with it in the interpreter:
>>>import token_handler
>>>token_handler.access_token('request', '<ip/hostname>') #request an access token and write it to file along with refresh token in seperate file
>>>token_handler.access_token('refresh', '<ip/hostname>') #refresh the access token
>>>token_handler.access_token('revoke', '<ip/hostname>') #revoke the access token

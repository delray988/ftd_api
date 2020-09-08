import requests

def access_token(action, ftd, payload=None):
   """
   action is either request,refresh or revoke
   ftd is the ip/hostname of your FTD
   """
   #define the URL by concatenating the IP or hostname of the ftd
   #supplied during the function call with the token context URL
   URL ='https://' + ftd + ':443/api/fdm/latest/fdm/token'
   #define in our headers that we are sending JSON formatted data and expect JSON format back
   headers = {"Content-Type": "application/json", "Accept": "application/json"}

   #Logic for the three token actions to take upon calling this function
   if action == 'request': #if action is 'request' follow the below logic
      #request the username and password to request a password-grant token
      username = input('Username: ')
      password = input('Password: ')
      #craft the payload based on the input requested by the user
      request_payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(username, password)
      #payload to be sent in the POST
      payload = request_payload

   elif action == 'refresh': #if action is 'refresh' follow the below logic
      try: #try to open refresh_token.txt file
         with open("refresh_token.txt", 'r') as file:
            ref_token = file.read().replace('\n', '')
         #craft the refresh payload based on the contents in the refresh_token.txt file
         refresh_payload = '{{"grant_type": "refresh_token", "refresh_token": "{}"}}'.format(ref_token)
         #payload to be sent in the POST
         payload = refresh_payload
      except: #if there is an error print to screen the below message
         print('Error finding refresh_token.txt file, please request an access token')

   elif action == 'revoke': #if action is 'revoke' follow the below logic
      try: #try to open access_token.txt file
         with open('access_token.txt', "r") as file:
            access_token = file.read().replace('\n', '')
         #craft the revoke payload based on the contents in the access_token.txt file
         revoke_payload = '{{"grant_type": "revoke_token", \
         "access_token": "{}", \
         "token_to_revoke": "{}"}}'.format(access_token, access_token)
         #payload to be sent in the POST
         payload = revoke_payload
      except: #if there is an error print to screen the below message
         print('Error finding access_token.txt file, please request an access token')
   else: #if none of the actions were 'request', 'refresh', or 'revoke' print to screen the below message
      print("please use 'request', 'refresh' or 'revoke' for the action")

   #Logic to be executed if the user chose an acceptable action and a payload was crafted
   if payload != None:
      #disable warnings
      requests.packages.urllib3.disable_warnings()
      #craft the HTTP POST with the payload based based on the chosen action and diable SSL verification
      response = requests.post(URL, payload, headers=headers, verify=False)
      #Logic to be executed if there is a valid response
      if response.status_code==200:
         #check the response for the access_token and refresh_token 
         if response.json().get('access_token') != None and response.json().get('refresh_token') != None:
            #use the json() decoder to get the access token from the response
            access_token = response.json().get('access_token')
            #write the access token to the access_token.txt file
            with open("access_token.txt", "w") as text_file:
               print("{}".format(access_token), file=text_file)
            #use the json() decoder to get the refresh token from the response
            ref_token = response.json().get('refresh_token')
            #write the refresh token to the refresh_token.txt file
            with open("refresh_token.txt", "w") as text_file:
               print("{}".format(ref_token), file=text_file)

         #if there were no tokens in the response, then logic states we revoked a token
         #when revoking a token you only get an "ok" message and status_code of 200 in the response
         elif response.json().get('message') == 'OK':
            print('token revoked successfully')
      else: #if any other status code is returned print to screen along with a more detailed server message for troubleshooting
         print("HTTP ERROR: {}".format(response.status_code))
         print("Server Error: {}".format(response.json().get('message')))
   else: #if no payload was crafted pass on this entire block of logic
      pass

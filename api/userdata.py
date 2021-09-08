import json
import random
import string
import discord
import requests
from urllib.parse import quote
from pydactyl import PterodactylClient
from requests.exceptions import HTTPError

"""
Creates Pterodactyl users and checks
if they exist. If they don't, it makes an account
Make a pull request if you think anything can be improved.
"""


with open('settings.json', 'r') as cfg:
    settings = json.load(cfg)
    discordsettings = settings["discord"]
    pterosettings = settings["pterodactyl"]


clientID = discordsettings['application_id']
clientSecret = discordsettings['secret_key']
redirectURI = discordsettings['redirect_uri']

pteroURL = pterosettings['url']
pteroAppKey = pterosettings['key']


with open('api\\users.json') as usrs:
    users = json.load(usrs)

def checkIfUserExists(discordEmail):
    url = f"{pteroURL}/api/application/users?filter{str(quote(f'={discordEmail}'))}"
    headers = {
        "Authorization": f"Bearer {pteroAppKey}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers).json()['data']
    i = 0
    for i in range(len(response)):
        emailtester = response[i]['attributes']['email']
        if emailtester == discordEmail:
            response = response[i]['attributes']
            break
        else:
            i += 1
    return response

def create_user(discordUsername, discordEmail, discordUserID):

    # Main function #

    userdataHeaders = {
        "Authorization": f"Bearer {pteroAppKey}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    

    makeUser = '{"discordEmail": "'+str(discordEmail)+'","username": "'+str(discordUsername)+'","first_name": "'+str(discordUsername)+'","last_name": "'+str(discordUserID)+'", "password": "changeme123"}'


    userdataResponse = requests.request('POST', url=f'{pteroURL}/api/application/users', data=makeUser, headers=userdataHeaders)
    print(userdataResponse)
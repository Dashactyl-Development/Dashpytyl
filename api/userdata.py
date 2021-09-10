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
    

def create_user(discordUsername, discordEmail, discordUserID, discorddic):

    # Main function #

    url = pteroURL+'/api/application/users'
    headers = {
        "Authorization": f"Bearer {pteroAppKey}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
    }

    payload = '{"email": "'+str(discordEmail)+'","username": "'+str(discordUserID)+'","first_name": "'+str(discordUsername)+'","last_name": "'+str(discorddic)+'"}'

    response = requests.request('POST', url, data=payload, headers=headers)
    print(response.text)
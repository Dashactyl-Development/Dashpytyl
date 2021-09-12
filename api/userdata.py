import json
import random
import string
import discord
import requests
from urllib.parse import quote
from pydactyl import PterodactylClient
from requests.exceptions import HTTPError
import sqlite3
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
    }

    payload = '{"email": "'+str(discordEmail)+'","username": "'+str(discordUserID)+'","first_name": "'+str(discordUsername)+'","last_name": "'+str(discorddic)+'"}'

    requests.request('POST', url, data=payload, headers=headers)
    headers2 = {
    "Authorization": f"Bearer {pteroAppKey}",
    "Accept": "application/json",
    "Content-Type": "application/json"
    }
    data2=requests.get(f"{pteroURL}/api/application/users?filter[email]{str(f'={discordEmail}')}", headers=headers2)
    response = data2.json()
    if data2.status_code == 200:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT id FROM main WHERE username = {discordUserID}")
        result = cursor.fetchone()
        for i in response["data"]:
            id = i["attributes"]["id"]
        if result == None:
            sql = (f"INSERT INTO main(id, username) VALUES (?, ?)")
            val = (id, discordUserID)
            cursor.execute(sql,val)
        else:
            pass
        db.commit()
        cursor.close()
        db.close()
    else:
        pass

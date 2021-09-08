import json

"""
Python config file.
This file is used by every single other file in
this project, just for convenience.
It gets config data and user data from `settings.json` and `users.json`, and assigns
them to Pythonic variables
Make a pull request if you think anything can be improved.
"""

with open('settings.json', 'r') as cfg:
    settings = json.load(cfg)
    discordsettings = settings["discord"]
    pterosettings = settings["pterodactyl"]

clientID = discordsettings['application_id']
clientSecret = discordsettings['secret_key']
redirectURI = discordsettings['redirect_uri']

pteroURL = pterosettings['URL']
pteroAppKey= pterosettings['key']

with open('api\\users.json') as usrs:
    users = json.load(usrs)
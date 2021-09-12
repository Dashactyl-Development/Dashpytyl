import json

with open('settings.json', 'r') as cfg:
    settings = json.load(cfg);discordsettings = settings["discord"];pterosettings = settings["pterodactyl"];websettings = settings["website"]

clientID = discordsettings['application_id']
clientSecret = discordsettings['secret_key']
redirectURI = discordsettings['redirect_uri']

pteroURL = pterosettings['url']
pteroAppKey= pterosettings['key']

webport = websettings['port']

with open('api\\users.json') as usrs:
    users = json.load(usrs)

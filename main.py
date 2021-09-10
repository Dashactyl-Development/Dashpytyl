import os
import sys
import requests

from api import configfile, userdata
from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session ,requires_authorization, Unauthorized
from pydactyl import PterodactylClient

app = Quart(__name__)

app.config["SECRET_KEY"] = "somdomethingslmafo"
app.config["DISCORD_CLIENT_ID"] = configfile.discordsettings["application_id"]   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = configfile.discordsettings["secret_key"]   # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = configfile.discordsettings["redirect_uri"]  
pteroapplication = PterodactylClient(configfile.pteroURL, configfile.pteroAppKey)
discord = DiscordOAuth2Session(app)



@app.route("/")
async def home():
    if not await discord.authorized:
        return await render_template('index.html')
    else:
        user = await discord.fetch_user()
        #try:
            
        headers = {
        "Authorization": f"Bearer {configfile.pteroAppKey}",
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        data=requests.get(f"{configfile.pteroURL}/api/client/account?filter{str(f'={user.email}')}", headers=headers)
        print(data)
        if data == 401:
            return await render_template("dashboard.html", username=user.name, userdicr=user.discriminator, userid=user.id, usermail=user.email)
        else:    
            return redirect(url_for('createuser'))

@app.route("/login")
async def login():
	return await discord.create_session()

@app.route('/callback')
async def callback():
    await discord.callback()
    return redirect(url_for('home'))

@app.route('/create')
@requires_authorization
async def createuser():
    user = await discord.fetch_user()
    userdata.create_user(user.name, user.email, user.id, user.discriminator)
    return await render_template("dashboard.html", user=user, panellink=configfile.pteroURL)

if __name__ == "__main__":
	app.run(debug=True,port=8080)

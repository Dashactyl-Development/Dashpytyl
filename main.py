import os
import sys
import requests
import logging
from flask.logging import default_handler


from api import configfile, userdata
from flask import Flask, render_template, request, session, redirect, url_for
from flask_discord import DiscordOAuth2Session ,requires_authorization, Unauthorized
from pydactyl import PterodactylClient

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config["SECRET_KEY"] = configfile.discordsettings["secret_key"]
app.config["DISCORD_CLIENT_ID"] = configfile.discordsettings["application_id"]   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = configfile.discordsettings["secret_key"]   # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = configfile.discordsettings["redirect_uri"]  
pteroapplication = PterodactylClient(configfile.pteroURL, configfile.pteroAppKey)
discord = DiscordOAuth2Session(app)

app.logger.removeHandler(default_handler)

@app.route("/")
def home():
    if discord.authorized:
        user = discord.fetch_user()
        #try:
            
        headers = {
        "Authorization": f"Bearer {configfile.pteroAppKey}",
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        data=requests.get(f"{configfile.pteroURL}/api/application/users?filter[email]{str(f'={user.email}')}", headers=headers)
        if data.status_code == 200:
            return render_template("dashboard.html",user=user,panellink=configfile.pteroURL)
        else:
            print("Doing this")
            return redirect(url_for('createuser'))       
    else:
        return render_template('index.html')
@app.route("/login")
def login():
	return discord.create_session()

@app.route('/callback')
def callback():
    discord.callback()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():

    discord.revoke()

    return redirect(url_for('home'))

@app.route('/create')
@requires_authorization
def createuser():
    user = discord.fetch_user()
    userdata.create_user(user.name, user.email, user.id, user.discriminator)
    return render_template("dashboard.html", user=user, panellink=configfile.pteroURL)

if __name__ == "__main__":
	app.run(debug=True,port=5000)

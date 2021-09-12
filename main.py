import os
import re
import sys
import requests
import logging
from flask.logging import default_handler
import sqlite3
import db

db.db_create()
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


def add(id,username):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM main WHERE username = {username}")
    result = cursor.fetchone()
    if result == None:
        sql = (f"INSERT INTO main(id, username) VALUES (?, ?)")
        val = (id, username)
        cursor.execute(sql,val)
    else:
        pass
    db.commit()
    cursor.close()
    db.close()


  

@app.route("/")
def home():
    if discord.authorized:
        user = discord.fetch_user()
        headers = {
        "Authorization": f"Bearer {configfile.pteroAppKey}",
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT id FROM main WHERE username = {user.id}")
        result = cursor.fetchone()
        if result != None:
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


@app.route('/dashboard')
@requires_authorization
def dash():
    user = discord.fetch_user()
    return render_template("dashboard.html", user=user, panellink=configfile.pteroURL)

@app.route('/create')
@requires_authorization
def createuser():
    user = discord.fetch_user()
    userdata.create_user(user.name, user.email, user.id, user.discriminator)
    return render_template("dashboard.html", user=user, panellink=configfile.pteroURL)

@app.route('/servers/new')
@requires_authorization
def createserver():
    user = discord.fetch_user()
    return render_template("create.html", user=user, panellink=configfile.pteroURL)    

if __name__ == "__main__":
	app.run(debug=True,port=configfile.webport)
